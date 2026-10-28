"""Acceso compatible al menú principal actualizado."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from algoritmo.main import main

if __name__ == "__main__":
    main()
