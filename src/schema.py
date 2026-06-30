from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class ColumnSpec:
    name: str
    aliases: tuple[str, ...]
    required: bool = True
    numeric: bool = False


EXPECTED_COLUMNS = [
    ColumnSpec("player", ("player", "jugador", "nombre", "name")),
    ColumnSpec("age", ("age", "edad"), numeric=True),
    ColumnSpec("position", ("position", "posicion", "pos", "demarcacion")),
    ColumnSpec("team", ("team", "equipo", "club")),
    ColumnSpec("league", ("league", "liga", "competition", "competicion")),
    ColumnSpec("season", ("season", "temporada", "campaign"), required=False),
    ColumnSpec("minutes", ("minutes", "minutos", "mins", "min"), numeric=True),
    ColumnSpec("goals", ("goals", "goles", "g"), required=False, numeric=True),
    ColumnSpec("assists", ("assists", "asistencias", "a"), required=False, numeric=True),
    ColumnSpec("xg", ("xg", "expected goals", "goles esperados"), required=False, numeric=True),
    ColumnSpec("xa", ("xa", "expected assists", "asistencias esperadas"), required=False, numeric=True),
    ColumnSpec("shots", ("shots", "tiros", "remates"), required=False, numeric=True),
    ColumnSpec("key_passes", ("key passes", "key_passes", "pases clave"), required=False, numeric=True),
    ColumnSpec(
        "progressive_passes",
        ("progressive passes", "progressive_passes", "pases progresivos"),
        required=False,
        numeric=True,
    ),
    ColumnSpec(
        "progressive_carries",
        ("progressive carries", "progressive_carries", "conducciones progresivas"),
        required=False,
        numeric=True,
    ),
    ColumnSpec(
        "completed_dribbles",
        ("completed dribbles", "completed_dribbles", "regates completados"),
        required=False,
        numeric=True,
    ),
    ColumnSpec("duels_won", ("duels won", "duels_won", "duelos ganados"), required=False, numeric=True),
    ColumnSpec("recoveries", ("recoveries", "recuperaciones"), required=False, numeric=True),
    ColumnSpec("interceptions", ("interceptions", "intercepciones"), required=False, numeric=True),
    ColumnSpec(
        "market_value",
        ("market value", "market_value", "valor de mercado", "valor mercado"),
        required=False,
        numeric=True,
    ),
    ColumnSpec("contract_end", ("contract end", "contract_end", "fin contrato", "contrato hasta"), required=False),
]

REQUIRED_COLUMNS = tuple(spec.name for spec in EXPECTED_COLUMNS if spec.required)
NUMERIC_COLUMNS = tuple(spec.name for spec in EXPECTED_COLUMNS if spec.numeric)
STAT_COLUMNS = tuple(
    spec.name for spec in EXPECTED_COLUMNS if spec.numeric and spec.name not in {"age", "minutes", "market_value"}
)


def canonicalize_label(label: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(label))
    ascii_label = normalized.encode("ascii", "ignore").decode("ascii")
    compact = re.sub(r"[^a-zA-Z0-9]+", " ", ascii_label).strip().lower()
    return compact.replace(" ", "_")


def alias_map() -> dict[str, str]:
    aliases: dict[str, str] = {}
    for spec in EXPECTED_COLUMNS:
        aliases[canonicalize_label(spec.name)] = spec.name
        for alias in spec.aliases:
            aliases[canonicalize_label(alias)] = spec.name
    return aliases


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with Spanish/English aliases mapped to canonical names."""
    mapping = alias_map()
    renamed = {}
    used = set()
    for column in df.columns:
        canonical = mapping.get(canonicalize_label(column), canonicalize_label(column))
        if canonical in used:
            canonical = canonicalize_label(column)
        renamed[column] = canonical
        used.add(canonical)
    return df.rename(columns=renamed).copy()


def validate_required_columns(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
