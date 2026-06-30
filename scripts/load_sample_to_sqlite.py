from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DATABASE_PATH, PLAYERS_TABLE, SAMPLE_DATA_PATH
from src.ingestion import load_csv_to_sqlite


def main() -> None:
    row_count = load_csv_to_sqlite(SAMPLE_DATA_PATH, DATABASE_PATH, PLAYERS_TABLE)
    print(f"CSV: {SAMPLE_DATA_PATH}")
    print(f"SQLite DB: {DATABASE_PATH}")
    print(f"Table: {PLAYERS_TABLE}")
    print(f"Rows loaded: {row_count}")


if __name__ == "__main__":
    main()
