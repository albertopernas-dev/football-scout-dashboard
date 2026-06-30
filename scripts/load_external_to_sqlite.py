from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DATABASE_PATH, EXTERNAL_PROVIDER_URL, PLAYERS_TABLE
from src.ingestion import load_external_to_sqlite


def main() -> None:
    if not EXTERNAL_PROVIDER_URL:
        raise SystemExit("EXTERNAL_PROVIDER_URL is not defined. Set it before running external ingestion.")

    row_count = load_external_to_sqlite(EXTERNAL_PROVIDER_URL, DATABASE_PATH, PLAYERS_TABLE)
    print(f"URL: {EXTERNAL_PROVIDER_URL}")
    print(f"SQLite DB: {DATABASE_PATH}")
    print(f"Table: {PLAYERS_TABLE}")
    print(f"Rows loaded: {row_count}")


if __name__ == "__main__":
    main()
