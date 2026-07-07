import pandas as pd

from src.market_context import summarize_market_context_diagnostics


def players_df():
    return pd.DataFrame(
        [
            {
                "player": "Matched Player",
                "team": "Test FC",
                "league": "Test League",
                "season": 2024,
            },
            {
                "player": "Unmatched Player",
                "team": "Other FC",
                "league": "Test League",
                "season": 2024,
            },
        ]
    )


def market_context_df():
    return pd.DataFrame(
        [
            {
                "player": "Matched Player",
                "team": "Test FC",
                "league": "Test League",
                "season": 2024,
                "age": 24,
                "market_value_eur": 1_500_000,
                "contract_end_date": "2026-06-30",
                "source": "manual_review",
                "source_url": "https://example.com/matched",
                "confidence": "high",
                "notes": "synthetic matched row",
            },
            {
                "player": "Context Only",
                "team": "Missing FC",
                "league": "Test League",
                "season": 2024,
                "age": "",
                "market_value_eur": "",
                "contract_end_date": "",
                "source": "manual_review",
                "source_url": "",
                "confidence": "low",
                "notes": "synthetic unmatched row",
            },
        ]
    )


def test_summarize_market_context_diagnostics_calculates_coverage():
    diagnostics = summarize_market_context_diagnostics(players_df(), market_context_df())

    coverage = diagnostics["coverage"]

    assert coverage["row_count"] == 2
    assert coverage["matched_count"] == 1
    assert coverage["matched_pct"] == 50.0
    assert coverage["age_known_count"] == 1
    assert coverage["market_value_known_count"] == 1
    assert coverage["contract_known_count"] == 1
    assert coverage["high_confidence_count"] == 1


def test_summarize_market_context_diagnostics_preserves_validation_errors():
    diagnostics = summarize_market_context_diagnostics(
        players_df(),
        market_context_df(),
        validation_errors=["Row 2: age must be valid."],
    )

    assert diagnostics["validation_errors"] == ["Row 2: age must be valid."]


def test_summarize_market_context_diagnostics_reports_duplicates():
    duplicated_context = pd.concat([market_context_df().iloc[[0]], market_context_df().iloc[[0]]])

    diagnostics = summarize_market_context_diagnostics(players_df(), duplicated_context)

    assert diagnostics["duplicate_count"] == 2
    assert len(diagnostics["duplicate_rows"]) == 2


def test_summarize_market_context_diagnostics_returns_matched_examples():
    diagnostics = summarize_market_context_diagnostics(players_df(), market_context_df())

    examples = diagnostics["matched_examples"]

    assert examples["player"].tolist() == ["Matched Player"]
    assert examples.loc[0, "market_context_confidence"] == "high"


def test_summarize_market_context_diagnostics_returns_unmatched_enrichment_examples():
    diagnostics = summarize_market_context_diagnostics(players_df(), market_context_df())

    examples = diagnostics["unmatched_enrichment_examples"]

    assert examples["player"].tolist() == ["Context Only"]
    assert examples.iloc[0]["team"] == "Missing FC"
