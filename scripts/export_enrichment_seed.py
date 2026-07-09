from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_cleaning import clean_player_data
from src.data_sources import load_players_data_with_metadata
from src.features import add_per90_metrics, add_position_percentiles
from src.opportunity import find_market_opportunities
from src.scoring import add_profile_scores


DEFAULT_OUTPUT_PATH = Path("data/enrichment/player_market_context_laliga_2024_reviewed.local.csv")
ENRICHMENT_SEED_COLUMNS = [
    "player",
    "team",
    "league",
    "season",
    "age",
    "market_value_eur",
    "contract_end_date",
    "source",
    "source_url",
    "confidence",
    "notes",
]
IDENTITY_COLUMNS = ["player", "team", "league", "season"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export a local market context enrichment seed CSV for manual review."
    )
    parser.add_argument("--top-n", type=int, default=25, help="Number of opportunities to export.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output CSV path. Defaults to a gitignored .local.csv in data/enrichment/.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite output if it already exists.")
    parser.add_argument(
        "--positions",
        nargs="*",
        default=None,
        help="Optional positions to include before ranking.",
    )
    parser.add_argument(
        "--min-minutes",
        type=int,
        default=900,
        help="Minimum minutes for Opportunity Finder.",
    )
    parser.add_argument("--max-age", type=int, default=None, help="Optional maximum effective age.")
    parser.add_argument(
        "--max-market-value",
        type=float,
        default=None,
        help="Optional maximum effective market value in euros.",
    )
    return parser


def prepare_opportunity_data(raw: pd.DataFrame) -> pd.DataFrame:
    cleaned = clean_player_data(raw)
    featured = add_per90_metrics(cleaned)
    percentiles = add_position_percentiles(featured)
    return add_profile_scores(percentiles)


def build_enrichment_seed_df(opportunities: pd.DataFrame, top_n: int | None = None) -> pd.DataFrame:
    seed = pd.DataFrame(columns=ENRICHMENT_SEED_COLUMNS)
    if opportunities.empty:
        return seed

    missing_columns = [column for column in IDENTITY_COLUMNS if column not in opportunities.columns]
    if missing_columns:
        raise ValueError(f"Missing identity columns for enrichment seed: {', '.join(missing_columns)}")

    identity = opportunities.loc[:, IDENTITY_COLUMNS].copy()
    identity = identity.drop_duplicates(subset=IDENTITY_COLUMNS, keep="first")
    if top_n is not None:
        identity = identity.head(top_n)

    for column in ENRICHMENT_SEED_COLUMNS:
        if column not in identity.columns:
            identity[column] = ""

    return identity.loc[:, ENRICHMENT_SEED_COLUMNS].reset_index(drop=True)


def write_enrichment_seed_csv(
    df: pd.DataFrame,
    output_path: str | Path,
    force: bool = False,
) -> int:
    path = Path(output_path)
    if path.exists() and not force:
        raise FileExistsError(f"Output file already exists: {path}. Use --force to overwrite.")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
    return int(len(df))


def main() -> None:
    args = build_parser().parse_args()
    raw, metadata = load_players_data_with_metadata()
    prepared = prepare_opportunity_data(raw)
    opportunities = find_market_opportunities(
        prepared,
        positions=args.positions,
        max_age=args.max_age,
        min_minutes=args.min_minutes,
        max_market_value=args.max_market_value,
        top_n=args.top_n,
    )
    seed = build_enrichment_seed_df(opportunities, top_n=args.top_n)
    rows_written = write_enrichment_seed_csv(seed, args.output, force=args.force)

    print("Enrichment seed export")
    print("----------------------")
    print(f"Source: {metadata.get('source', 'unknown')}")
    print(f"Source rows: {metadata.get('row_count', len(raw))}")
    print(f"Top N requested: {args.top_n}")
    print(f"Opportunities found: {len(opportunities)}")
    print(f"Rows written: {rows_written}")
    print(f"Output: {args.output}")
    print("Enrichment fields left empty for manual review.")


if __name__ == "__main__":
    main()
