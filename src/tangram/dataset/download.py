#!/usr/bin/env python3
"""Module pour télécharger les fichiers SVG du dataset KiloGram.
FYI : le dataset KiloGram est sous licence CC BY-NC-SA 4.0 (usage non commercial).
Exemples d'utilisation :
    python -m tangram.dataset.download -n 10
    python -m tangram.dataset.download -n 20 --shuffle
    python -m tangram.dataset.download --names page1-1 page2-189
    python -m tangram.dataset.download -o data/puzzles_svg
    
La majorité du code de ce module à été générée par intelligence artificielle 
"""

import argparse
import json
import logging
import random
import sys
import urllib.error
import urllib.request
from pathlib import Path

logger = logging.getLogger("tangram.dataset.download")

KILOGRAM_REPO = "lil-lab/kilogram"
RAW_BASE_URL = "https://raw.githubusercontent.com/lil-lab/kilogram/main/dataset/tangrams-svg"
API_TREE_URL = "https://api.github.com/repos/lil-lab/kilogram/git/trees/main?recursive=1"
DEFAULT_OUTPUT_DIR = Path("data/raw_svg")
USER_AGENT = "IA41-Tangram-Downloader/1.0"


def _get_embedded_manifest() -> list[str]:
    """Charge la liste des SVGs embarquée localement comme solution de repli."""
    manifest_path = Path(__file__).parent / "manifest.json"
    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except (OSError, json.JSONDecodeError) as e:
            logger.warning("Impossible de lire le manifest local : %s", e)
    return []


def get_available_svg_names(fetch_remote: bool = False, timeout: float = 10.0) -> list[str]:
    """Récupère la liste de tous les fichiers SVG du dataset KiloGram.

    Par défaut, lit le manifest embarqué (instantané et sans limite de requêtes API).
    Si fetch_remote=True, interroge l'API GitHub pour obtenir la dernière arborescence.
    """
    if not fetch_remote:
        embedded = _get_embedded_manifest()
        if embedded:
            return embedded

    # Tentative via l'API GitHub Tree
    try:
        req = urllib.request.Request(API_TREE_URL, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
            tree = data.get("tree", [])
            svg_names = sorted(
                Path(item["path"]).name
                for item in tree
                if item.get("path", "").startswith("dataset/tangrams-svg/")
                and item.get("path", "").endswith(".svg")
            )
            if svg_names:
                return svg_names
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as err:
        logger.warning("Échec de la récupération distante via l'API GitHub : %s", err)

    # Repli sur le manifest local
    return _get_embedded_manifest()


def download_single_svg(
    filename: str,
    output_dir: Path,
    timeout: float = 10.0,
    force: bool = False,
) -> tuple[str, str]:
    """Télécharge un unique fichier SVG depuis le dépôt KiloGram.

    Retourne un tuple (statut, message) où statut vaut 'downloaded', 'skipped', ou 'failed'.
    """
    if not filename.endswith(".svg"):
        filename = f"{filename}.svg"

    destination = output_dir / filename
    if destination.exists() and destination.stat().st_size > 0 and not force:
        return "skipped", f"{filename} existe déjà (ignoré)."

    url = f"{RAW_BASE_URL}/{filename}"
    temp_destination = destination.with_suffix(".tmp")

    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read()

        # Écriture atomique dans un fichier temporaire puis renommage
        with open(temp_destination, "wb") as f:
            f.write(content)
        temp_destination.replace(destination)
        return "downloaded", f"{filename} téléchargé ({len(content)} octets)."
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        if temp_destination.exists():
            temp_destination.unlink(missing_ok=True)
        return "failed", f"Erreur lors du téléchargement de {filename} : {err}"


def download_kilogram_svgs(
    limit: int | None = None,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    shuffle: bool = False,
    seed: int | None = None,
    force: bool = False,
    names: list[str] | None = None,
    timeout: float = 10.0,
    verbose: bool = True,
) -> dict[str, list[str]]:
    """Télécharge un ensemble de fichiers SVG depuis le dataset KiloGram.

    Args:
        limit: Nombre maximal de SVGs à télécharger (None ou <= 0 = tous).
        output_dir: Dossier de destination pour les fichiers SVG.
        shuffle: Si True, mélange aléatoirement les fichiers avant sélection.
        seed: Graine optionnelle pour la reproductibilité du mélange aléatoire.
        force: Si True, re-télécharge les fichiers même s'ils existent déjà.
        names: Liste de noms de fichiers spécifiques à télécharger.
        timeout: Délai d'attente réseau par requête (en secondes).
        verbose: Si True, affiche la progression dans la console.

    Returns:
        Dictionnaire récapitulatif avec les listes des fichiers 'downloaded', 'skipped', 'failed'.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    if names:
        target_files = [n if n.endswith(".svg") else f"{n}.svg" for n in names]
    else:
        target_files = get_available_svg_names()

    if not target_files:
        raise RuntimeError("Aucun fichier SVG trouvé ou disponible dans le manifest.")

    if shuffle:
        rng = random.Random(seed)
        target_files = list(target_files)
        rng.shuffle(target_files)

    if limit is not None and limit > 0:
        target_files = target_files[:limit]

    total = len(target_files)
    results: dict[str, list[str]] = {
        "downloaded": [],
        "skipped": [],
        "failed": [],
    }

    if verbose:
        print("=== Téléchargement KiloGram Tangrams SVG ===")
        print(f"Cibles : {total} fichier(s) vers '{out_path}'")
        if force:
            print("Mode forcé : réécriture des fichiers existants.")
        print("-" * 50)

    for i, filename in enumerate(target_files, start=1):
        status, msg = download_single_svg(
            filename=filename,
            output_dir=out_path,
            timeout=timeout,
            force=force,
        )
        results[status].append(filename)

        if verbose:
            tag = {
                "downloaded": "[OK]",
                "skipped": "[SKIP]",
                "failed": "[FAIL]",
            }.get(status, "[?]")
            print(f"[{i:>4}/{total}] {tag} {filename}")
            if status == "failed":
                print(f"       -> {msg}")

    if verbose:
        print("-" * 50)
        print(
            f"Terminé : {len(results['downloaded'])} téléchargé(s), "
            f"{len(results['skipped'])} ignoré(s), "
            f"{len(results['failed'])} échec(s)."
        )

    return results


def build_arg_parser() -> argparse.ArgumentParser:
    """Construit l'analyseur d'arguments CLI."""
    parser = argparse.ArgumentParser(
        description="Télécharge les fichiers SVG de puzzles Tangram du dataset KiloGram."
    )
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=None,
        help="Nombre maximum de SVGs à télécharger (ex: 10, 50). Par défaut : tous (1013).",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Dossier de destination (par défaut : '{DEFAULT_OUTPUT_DIR}').",
    )
    parser.add_argument(
        "-s",
        "--shuffle",
        action="store_true",
        help="Mélanger aléatoirement la sélection de puzzles.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Graine aléatoire pour le mélange (reproductibilité).",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Forcer le re-téléchargement même si le fichier est déjà présent localement.",
    )
    parser.add_argument(
        "--names",
        nargs="+",
        help="Télécharger uniquement certains puzzles par nom (ex: page1-1 page2-189).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Timeout en secondes pour chaque requête réseau (défaut : 10.0).",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Désactiver l'affichage de la progression.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée en ligne de commande."""
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    try:
        results = download_kilogram_svgs(
            limit=args.limit,
            output_dir=args.output_dir,
            shuffle=args.shuffle,
            seed=args.seed,
            force=args.force,
            names=args.names,
            timeout=args.timeout,
            verbose=not args.quiet,
        )
        if results["failed"] and not results["downloaded"] and not results["skipped"]:
            return 1
        return 0
    except (RuntimeError, ValueError) as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
