from pathlib import Path
from unittest.mock import MagicMock, patch

from tangram.dataset.download import (
    build_arg_parser,
    download_kilogram_svgs,
    download_single_svg,
    get_available_svg_names,
)


def test_get_available_svg_names_embedded():
    names = get_available_svg_names(fetch_remote=False)
    assert len(names) == 1013
    assert all(name.endswith(".svg") for name in names)
    assert "page1-1.svg" in names


def test_download_single_svg_mocked(tmp_path: Path):
    fake_svg = b"<svg><polygon id='1' points='0,0 1,1 0,1'/></svg>"
    mock_resp = MagicMock()
    mock_resp.read.return_value = fake_svg
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        # 1. Premier téléchargement
        status, _msg = download_single_svg("sample.svg", tmp_path)
        assert status == "downloaded"
        assert (tmp_path / "sample.svg").exists()
        assert (tmp_path / "sample.svg").read_bytes() == fake_svg

        # 2. Deuxième appel sans force -> doit être skipped
        status, _msg = download_single_svg("sample.svg", tmp_path, force=False)
        assert status == "skipped"

        # 3. Troisième appel avec force=True -> doit re-télécharger
        status, _msg = download_single_svg("sample.svg", tmp_path, force=True)
        assert status == "downloaded"


def test_download_kilogram_svgs_limit(tmp_path: Path):
    fake_svg = b"<svg></svg>"
    mock_resp = MagicMock()
    mock_resp.read.return_value = fake_svg
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        results = download_kilogram_svgs(
            limit=5,
            output_dir=tmp_path,
            verbose=False,
        )
        assert len(results["downloaded"]) == 5
        assert len(results["skipped"]) == 0
        assert len(results["failed"]) == 0
        assert len(list(tmp_path.glob("*.svg"))) == 5


def test_arg_parser():
    parser = build_arg_parser()
    args = parser.parse_args(["-n", "10", "--output-dir", "custom/dir", "--shuffle", "-f"])
    assert args.limit == 10
    assert args.output_dir == "custom/dir"
    assert args.shuffle is True
    assert args.force is True
