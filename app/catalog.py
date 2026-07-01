import json
from pathlib import Path

CATALOG = None


def load_catalog():
    global CATALOG

    if CATALOG is not None:
        return CATALOG

    path = Path("data/shl_catalog.json")

    with open(path, encoding="utf-8") as f:
        CATALOG = json.load(f)

    return CATALOG