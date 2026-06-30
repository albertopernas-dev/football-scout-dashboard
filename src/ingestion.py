from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


def load_csv_to_sqlite(csv_path: str | Path, database_path: str | Path, table_name: str) -> int:
    source = Path(csv_path)
    if not source.exists():
        raise FileNotFoundError(f"CSV file not found: {source}")

    data = pd.read_csv(source)
    target = Path(database_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(target) as connection:
        data.to_sql(table_name, connection, index=False, if_exists="replace")
    return len(data)
