from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_cleaning import clean_player_data
from src.data_sources import load_players_data_with_metadata
from src.features import add_per90_metrics, add_position_percentiles
from src.scoring import (
    GOALKEEPER_METRIC_WEIGHTS,
    PROFILE_SCORE_COLUMNS,
    PROFILE_WEIGHTS,
    add_profile_scores,
    is_goalkeeper_position,
    is_metric_informative,
)


SCORE_COLUMNS = (
    "overall_score",
    "sample_adjusted_overall_score",
    "market_opportunity_score",
    "sample_adjusted_market_opportunity_score",
)
DEFAULT_DISPLAY_COLUMNS = (
    "player",
    "team",
    "position",
    "league",
    "season",
    "minutes",
    "minutes_reliability_score",
    "minutes_sample_label",
    "is_minutes_qualified",
    "overall_score",
    "sample_adjusted_overall_score",
    "market_opportunity_score",
    "sample_adjusted_market_opportunity_score",
    *PROFILE_SCORE_COLUMNS,
)


def prepare_scores(raw: pd.DataFrame) -> pd.DataFrame:
    cleaned = clean_player_data(raw)
    featured = add_per90_metrics(cleaned)
    percentiles = add_position_percentiles(featured)
    return add_profile_scores(percentiles)


def scoring_input_columns() -> list[str]:
    columns = {metric for weights in PROFILE_WEIGHTS.values() for metric in weights}
    return sorted(columns)


def summarize_scoring_columns(
    df: pd.DataFrame,
    scoring_columns: Iterable[str] | None = None,
) -> dict[str, list[str]]:
    columns = list(scoring_columns or scoring_input_columns())
    available = [column for column in columns if column in df.columns]
    missing = [column for column in columns if column not in df.columns]
    percentile_available = [f"{column}_pct" for column in columns if f"{column}_pct" in df.columns]
    zero_only = [column for column in available if _is_zero_only(df[column])]
    used_by_scoring = [column for column in columns if is_metric_informative(df, column)]
    ignored_no_signal = [column for column in available if column not in used_by_scoring]
    return {
        "available": available,
        "missing": missing,
        "percentile_available": percentile_available,
        "zero_only": zero_only,
        "used_by_scoring": used_by_scoring,
        "ignored_no_signal": ignored_no_signal,
    }


def calculate_score_distribution(
    df: pd.DataFrame,
    score_columns: Iterable[str] = SCORE_COLUMNS,
) -> dict[str, dict[str, float]]:
    distribution: dict[str, dict[str, float]] = {}
    for column in score_columns:
        if column not in df.columns:
            continue
        values = pd.to_numeric(df[column], errors="coerce").dropna()
        if values.empty:
            distribution[column] = {
                "count": 0,
                "min": 0.0,
                "q25": 0.0,
                "median": 0.0,
                "q75": 0.0,
                "max": 0.0,
                "mean": 0.0,
            }
            continue
        distribution[column] = {
            "count": int(values.count()),
            "min": round(float(values.min()), 1),
            "q25": round(float(values.quantile(0.25)), 1),
            "median": round(float(values.median()), 1),
            "q75": round(float(values.quantile(0.75)), 1),
            "max": round(float(values.max()), 1),
            "mean": round(float(values.mean()), 1),
        }
    return distribution


def top_rankings(df: pd.DataFrame, score_column: str, n: int = 10) -> pd.DataFrame:
    if score_column not in df.columns:
        return pd.DataFrame()
    display_columns = [column for column in DEFAULT_DISPLAY_COLUMNS if column in df.columns]
    if score_column not in display_columns:
        display_columns.append(score_column)
    return (
        df.sort_values(score_column, ascending=False)
        .head(n)
        .loc[:, display_columns]
        .reset_index(drop=True)
    )


def top_rankings_by_position(
    df: pd.DataFrame,
    score_column: str = "overall_score",
    n: int = 10,
) -> dict[str, pd.DataFrame]:
    if "position" not in df.columns or score_column not in df.columns:
        return {}
    rankings = {}
    for position in sorted(df["position"].dropna().astype(str).unique()):
        position_df = df[df["position"].astype(str) == position]
        rankings[position] = top_rankings(position_df, score_column, n=n)
    return rankings


def find_low_minutes_in_top_rankings(
    df: pd.DataFrame,
    score_columns: Iterable[str] = SCORE_COLUMNS,
    top_n: int = 10,
    minutes_threshold: int = 300,
) -> dict[str, pd.DataFrame]:
    if "minutes" not in df.columns:
        return {}
    result = {}
    for score_column in score_columns:
        top = top_rankings(df, score_column, n=top_n)
        if top.empty:
            result[score_column] = top
            continue
        minutes = pd.to_numeric(top["minutes"], errors="coerce").fillna(0)
        result[score_column] = top[minutes < minutes_threshold].reset_index(drop=True)
    return result


def minutes_sample_distribution(df: pd.DataFrame) -> dict[str, int]:
    if "minutes_sample_label" not in df.columns:
        return {}
    counts = df["minutes_sample_label"].value_counts(dropna=False)
    return {str(label): int(count) for label, count in counts.items()}


def top_unqualified_count(df: pd.DataFrame, score_column: str, n: int = 10) -> int:
    if "is_minutes_qualified" not in df.columns or score_column not in df.columns:
        return 0
    top = df.sort_values(score_column, ascending=False).head(n)
    qualified = top["is_minutes_qualified"].fillna(False).astype(bool)
    return int((~qualified).sum())


def position_counts(df: pd.DataFrame) -> dict[str, int]:
    if "position" not in df.columns:
        return {}
    counts = df["position"].fillna("Unknown").astype(str).value_counts()
    return {str(position): int(count) for position, count in counts.items()}


def goalkeeper_diagnostics(df: pd.DataFrame) -> dict[str, object]:
    if "position" not in df.columns:
        goalkeepers = df.iloc[0:0]
    else:
        goalkeepers = df[df["position"].apply(is_goalkeeper_position)]
    available_gk_columns = [column for column in GOALKEEPER_METRIC_WEIGHTS if column in df.columns]
    informative_gk_metrics = [
        column for column in GOALKEEPER_METRIC_WEIGHTS if is_metric_informative(goalkeepers, column)
    ]
    return {
        "goalkeepers_count": len(goalkeepers),
        "available_gk_columns": available_gk_columns,
        "informative_gk_metrics": informative_gk_metrics,
        "goalkeepers": goalkeepers,
    }


def main() -> None:
    _configure_stdout()
    raw, metadata = load_players_data_with_metadata()
    df = prepare_scores(raw)

    print("Source metadata:")
    print(json.dumps(metadata, indent=2, ensure_ascii=False, default=str))
    print(f"\nRow count: {len(df)}")

    scoring_columns = summarize_scoring_columns(df)
    print("\nScoring columns:")
    print(f"- Available: {', '.join(scoring_columns['available']) or 'None'}")
    print(f"- Percentiles available: {', '.join(scoring_columns['percentile_available']) or 'None'}")
    print(f"- Missing: {', '.join(scoring_columns['missing']) or 'None'}")
    print(f"- Present but zero-only: {', '.join(scoring_columns['zero_only']) or 'None'}")
    print(f"- Used by scoring: {', '.join(scoring_columns['used_by_scoring']) or 'None'}")
    print(f"- Ignored, no signal: {', '.join(scoring_columns['ignored_no_signal']) or 'None'}")

    print("\nScore distribution:")
    print(json.dumps(calculate_score_distribution(df), indent=2, ensure_ascii=False))

    print("\nPosition counts:")
    for position, count in position_counts(df).items():
        print(f"- {position}: {count}")

    gk_diagnostics = goalkeeper_diagnostics(df)
    print("\nGoalkeeper diagnostics:")
    print(f"- Goalkeepers: {gk_diagnostics['goalkeepers_count']}")
    print(f"- Available GK columns: {', '.join(gk_diagnostics['available_gk_columns']) or 'None'}")
    print(f"- Informative GK metrics: {', '.join(gk_diagnostics['informative_gk_metrics']) or 'None'}")

    print("\nMinutes sample distribution:")
    sample_distribution = minutes_sample_distribution(df)
    if sample_distribution:
        for label, count in sample_distribution.items():
            print(f"- {label}: {count}")
    else:
        print("- No sample labels available.")

    print("\nUnqualified players in top 10:")
    for score_column in SCORE_COLUMNS:
        print(f"- {score_column}: {top_unqualified_count(df, score_column, n=10)}")

    for score_column in SCORE_COLUMNS:
        print(f"\nTop 10 {score_column}:")
        _print_dataframe(top_rankings(df, score_column, n=10))

    goalkeepers = gk_diagnostics["goalkeepers"]
    print("\nTop 10 goalkeepers by current scores:")
    for score_column in SCORE_COLUMNS:
        print(f"\nGoalkeepers - {score_column}:")
        _print_dataframe(top_rankings(goalkeepers, score_column, n=10))

    print("\nTop 10 overall_score by position:")
    for position, ranking in top_rankings_by_position(df, score_column="overall_score", n=10).items():
        print(f"\nPosition: {position}")
        _print_dataframe(ranking)

    print("\nLow-minute players in top rankings (threshold: <300 minutes):")
    for score_column, ranking in find_low_minutes_in_top_rankings(df).items():
        print(f"\n{score_column}:")
        _print_dataframe(ranking)


def _is_zero_only(series: pd.Series) -> bool:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return False
    return bool(values.eq(0).all())


def _configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _print_dataframe(df: pd.DataFrame) -> None:
    if df.empty:
        print("No rows.")
        return
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
