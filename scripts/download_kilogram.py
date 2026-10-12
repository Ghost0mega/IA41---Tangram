#!/usr/bin/env python3
"""Script pratique pour telecharger les SVG du dataset KiloGram.

Exemples d'utilisation :
    python scripts/download_kilogram.py -n 10
    python scripts/download_kilogram.py -n 20 --shuffle
    python scripts/download_kilogram.py --names page1-1 page2-189
    python scripts/download_kilogram.py -o data/puzzles_svg
"""

import sys
from pathlib import Path

# Permet d'importer tangram meme si le package n'a pas ete installe avec pip install -e .
project_root = Path(__file__).resolve().parent.parent
src_dir = project_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from tangram.dataset.download import main

if __name__ == "__main__":
    sys.exit(main())
