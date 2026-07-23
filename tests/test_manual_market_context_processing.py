from __future__ import annotations

import csv
import inspect
import io
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pytest

import src.manual_market_context_processing as processing
from src.manual_market_context_processing import (
    ALLOWED_SOURCE_TYPES,
    CANONICAL_COLUMNS,
    DIAGNOSTIC_COLUMNS,
    INPUT_CONTRACT_VERSION,
    OBSERVATION_COLUMNS,
    PROCESSING_POLICY_VERSION,
    REJECTED_ROW_COLUMNS,
    REQUIRED_COLUMNS,
    STAGE_NAME,
    STRUCTURAL_REQUIRED_VALUES,
    ManualMarketContextProcessingResult,
    process_reviewed_market_context,
)


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "manual_market_context"
INGESTED_AT = datetime(2026, 7, 23, 10, 0, tzinfo=timezone.utc)

BASE_ROW = {
    "schema_version": INPUT_CONTRACT_VERSION,
    "local_record_id": "synthetic-record-001",
    "player": "Player Alpha",
    "team": "Team Red",
    "league": "Synthetic League",
    "season": "2024",
    "source_name": "Synthetic Review",
    "source_type": "internal-reviewed",
    "reviewed_at": "2026-07-22T10:00:00Z",
    "reviewer": "reviewer-alpha",
}


def _write_csv(
    tmp_path: Path,
    rows: list[dict[str, object]],
    *,
    columns: tuple[str, ...] | list[str] = REQUIRED_COLUMNS,
    name: str = "input.csv",
    delimiter: str = ",",
) -> Path:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=list(columns),
        delimiter=delimiter,
        lineterminator="\n",
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(rows)
    path = tmp_path / name
    path.write_text(output.getvalue(), encoding="utf-8", newline="")
    return path


def _process(path: Path, **kwargs) -> ManualMarketContextProcessingResult:
    return process_reviewed_market_context(path, ingested_at=INGESTED_AT, **kwargs)


def _row(**changes: object) -> dict[str, object]:
    return {**BASE_ROW, **changes}


def _codes(result: ManualMarketContextProcessingResult) -> list[str]:
    return result.diagnostics["diagnostic_code"].tolist()


def test_public_constants_match_the_approved_stage_a_contract():
    assert INPUT_CONTRACT_VERSION == "manual-market-context-input-v1"
    assert PROCESSING_POLICY_VERSION == "manual-market-context-policy-v1"
    assert STAGE_NAME == "A"
    assert CANONICAL_COLUMNS == (
        "schema_version",
        "local_record_id",
        "player",
        "team",
        "league",
        "season",
        "age",
        "date_of_birth",
        "age_reference_date",
        "market_value_eur",
        "contract_end_date",
        "salary_value",
        "salary_currency",
        "salary_period",
        "jersey_number",
        "position",
        "value_date",
        "market_value_value_date",
        "salary_value_date",
        "contract_value_date",
        "source_name",
        "source_url",
        "source_type",
        "source_reference",
        "reviewed_at",
        "reviewer",
        "confidence",
        "notes",
        "is_estimated",
        "review_status",
        "review_notes",
    )
    assert REQUIRED_COLUMNS == (
        "schema_version",
        "local_record_id",
        "player",
        "team",
        "league",
        "season",
        "source_name",
        "source_type",
        "reviewed_at",
        "reviewer",
    )
    assert STRUCTURAL_REQUIRED_VALUES == (
        "local_record_id",
        "player",
        "team",
        "league",
        "season",
        "source_name",
        "source_type",
        "reviewed_at",
        "reviewer",
    )
    assert ALLOWED_SOURCE_TYPES == (
        "official-public",
        "provider-public",
        "manual-reference",
        "internal-reviewed",
        "other-reviewed",
    )


def test_only_the_eleven_approved_stage_a_diagnostic_codes_are_declared():
    expected_codes = {
        "MCV100_UNSUPPORTED_SCHEMA_VERSION",
        "MCV101_MISSING_REQUIRED_COLUMN",
        "MCV102_DUPLICATE_HEADER",
        "MCV103_UNKNOWN_COLUMN",
        "MCV104_INVALID_ENCODING",
        "MCV105_INVALID_DELIMITER",
        "MCV200_MISSING_REQUIRED_VALUE",
        "MCV201_DUPLICATE_LOCAL_RECORD_ID",
        "MCV202_INVALID_SEASON",
        "MCV203_INVALID_REVIEWED_AT",
        "MCV204_INVALID_SOURCE_TYPE",
    }
    declared_codes = {
        value
        for name, value in vars(processing).items()
        if name.startswith("MCV") and isinstance(value, str)
    }

    assert declared_codes == expected_codes
    source = inspect.getsource(processing)
    forbidden_codes = {
        "MCV100_" + "INVALID_SCHEMA_VERSION",
        "MCV102_" + "DUPLICATE_COLUMN",
    }
    assert forbidden_codes.isdisjoint(declared_codes)
    assert all(code not in source for code in forbidden_codes)


def test_public_api_requires_explicit_path_and_keyword_only_controls():
    signature = inspect.signature(process_reviewed_market_context)

    assert signature.parameters["input_path"].default is inspect.Parameter.empty
    assert signature.parameters["ingested_at"].kind is inspect.Parameter.KEYWORD_ONLY
    assert signature.parameters["strict"].kind is inspect.Parameter.KEYWORD_ONLY
    assert signature.parameters["strict"].default is True


def test_missing_path_propagates_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        _process(tmp_path / "missing.csv")


def test_path_access_happens_before_strict_validation(tmp_path):
    with pytest.raises(FileNotFoundError):
        _process(tmp_path / "missing.csv", strict=False)


def test_strict_false_is_rejected_with_exact_message(tmp_path):
    path = _write_csv(tmp_path, [BASE_ROW])

    with pytest.raises(ValueError, match="^strict=False is not approved for Stage A$"):
        _process(path, strict=False)


def test_naive_ingested_at_is_rejected_with_exact_message(tmp_path):
    path = _write_csv(tmp_path, [BASE_ROW])

    with pytest.raises(ValueError, match="^ingested_at must be timezone-aware$"):
        process_reviewed_market_context(
            path,
            ingested_at=datetime(2026, 7, 23, 10, 0),
        )


def test_timezone_aware_ingested_at_is_accepted(tmp_path):
    path = _write_csv(tmp_path, [BASE_ROW])

    result = process_reviewed_market_context(
        path,
        ingested_at=datetime(2026, 7, 23, 12, 0).astimezone(),
    )

    assert result.file_outcome == "accepted"


def test_processing_does_not_print(tmp_path, capsys):
    path = _write_csv(tmp_path, [BASE_ROW])

    _process(path)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_valid_minimal_fixture_is_accepted():
    result = _process(FIXTURE_DIR / "valid_minimal.csv")

    assert result.file_outcome == "accepted"
    assert result.file_summary["total_rows"] == 1
    assert result.file_summary["accepted_rows"] == 1
    assert result.file_summary["rejected_rows"] == 0
    assert result.diagnostics.empty


@pytest.mark.parametrize(
    ("payload", "expected_code"),
    [
        (b"\xef\xbb\xbfschema_version\n", "MCV104_INVALID_ENCODING"),
        (b"\xff\xfe\x00\x00", "MCV104_INVALID_ENCODING"),
    ],
)
def test_invalid_utf8_or_bom_rejects_without_fallback(tmp_path, payload, expected_code):
    path = tmp_path / "encoding.csv"
    path.write_bytes(payload)

    result = _process(path)

    assert result.file_outcome == "rejected"
    assert _codes(result) == [expected_code]
    assert result.file_summary["total_rows"] == 0
    assert result.rejected_rows.empty


@pytest.mark.parametrize("payload", [b"", b" \t\r\n  \n"])
def test_empty_or_whitespace_only_file_reports_all_required_headers(tmp_path, payload):
    path = tmp_path / "empty.csv"
    path.write_bytes(payload)

    result = _process(path)

    assert result.file_outcome == "rejected"
    assert _codes(result) == ["MCV101_MISSING_REQUIRED_COLUMN"] * len(
        REQUIRED_COLUMNS
    )
    assert result.diagnostics["field_name"].tolist() == list(REQUIRED_COLUMNS)
    assert "MCV105_INVALID_DELIMITER" not in _codes(result)
    assert result.file_summary["total_rows"] == 0
    assert result.file_summary["accepted_rows"] == 0
    assert result.file_summary["rejected_rows"] == 0
    assert result.rejected_rows.empty


@pytest.mark.parametrize("delimiter", [";", "\t"])
def test_alternate_delimiter_is_rejected_before_row_parsing(tmp_path, delimiter):
    path = _write_csv(tmp_path, [BASE_ROW], delimiter=delimiter)

    result = _process(path)

    assert result.file_outcome == "rejected"
    assert _codes(result) == ["MCV105_INVALID_DELIMITER"]
    assert result.file_summary["total_rows"] == 0
    assert result.rejected_rows.empty


@pytest.mark.parametrize("quoted_value", ["Synthetic; Review", "Synthetic\tReview"])
def test_alternate_delimiter_inside_quoted_value_is_not_a_false_positive(
    tmp_path, quoted_value
):
    path = _write_csv(tmp_path, [_row(source_name=quoted_value)])

    result = _process(path)

    assert result.file_outcome == "accepted"
    assert result.diagnostics.empty


def test_duplicate_header_names_are_reported_once_per_name_lexically(tmp_path):
    header = (
        "schema_version,local_record_id,player,team,league,season,"
        "source_name,source_type,reviewed_at,reviewer,team,player\n"
    )
    path = tmp_path / "duplicates.csv"
    path.write_text(header, encoding="utf-8", newline="")

    result = _process(path)

    assert _codes(result) == [
        "MCV102_DUPLICATE_HEADER",
        "MCV102_DUPLICATE_HEADER",
    ]
    assert result.diagnostics["field_name"].tolist() == ["player", "team"]
    assert result.file_summary["total_rows"] == 0


def test_missing_columns_follow_canonical_required_order(tmp_path):
    columns = tuple(
        column for column in REQUIRED_COLUMNS if column not in {"player", "season"}
    )
    path = _write_csv(tmp_path, [], columns=columns)

    result = _process(path)

    assert _codes(result) == [
        "MCV101_MISSING_REQUIRED_COLUMN",
        "MCV101_MISSING_REQUIRED_COLUMN",
    ]
    assert result.diagnostics["field_name"].tolist() == ["player", "season"]


def test_unknown_columns_are_reported_lexically(tmp_path):
    columns = (*REQUIRED_COLUMNS, "zeta_extra", "alpha_extra")
    path = _write_csv(tmp_path, [], columns=columns)

    result = _process(path)

    assert _codes(result) == [
        "MCV103_UNKNOWN_COLUMN",
        "MCV103_UNKNOWN_COLUMN",
    ]
    assert result.diagnostics["field_name"].tolist() == [
        "alpha_extra",
        "zeta_extra",
    ]


def test_missing_and_unknown_columns_are_reported_together_in_phase_order(tmp_path):
    columns = tuple(column for column in REQUIRED_COLUMNS if column != "team") + (
        "unexpected",
    )
    path = _write_csv(tmp_path, [], columns=columns)

    result = _process(path)

    assert _codes(result) == [
        "MCV101_MISSING_REQUIRED_COLUMN",
        "MCV103_UNKNOWN_COLUMN",
    ]
    assert result.diagnostics["field_name"].tolist() == ["team", "unexpected"]


def test_header_names_are_case_sensitive_and_not_normalized(tmp_path):
    columns = tuple("Player" if column == "player" else column for column in REQUIRED_COLUMNS)
    path = _write_csv(tmp_path, [], columns=columns)

    result = _process(path)

    assert _codes(result) == [
        "MCV101_MISSING_REQUIRED_COLUMN",
        "MCV103_UNKNOWN_COLUMN",
    ]
    assert result.diagnostics["field_name"].tolist() == ["player", "Player"]


def test_file_header_errors_prevent_row_diagnostics(tmp_path):
    columns = tuple(column for column in REQUIRED_COLUMNS if column != "player")
    path = _write_csv(tmp_path, [_row(season="invalid")], columns=columns)

    result = _process(path)

    assert set(result.diagnostics["scope"]) == {"file"}
    assert result.rejected_rows.empty


@pytest.mark.parametrize("invalid_version", ["", " ", "v2", " manual-market-context-input-v1 "])
def test_invalid_schema_version_rejects_file_without_row_validation(
    tmp_path, invalid_version
):
    path = _write_csv(
        tmp_path,
        [_row(schema_version=invalid_version, season="invalid")],
    )

    result = _process(path)

    assert result.file_outcome == "rejected"
    assert _codes(result) == ["MCV100_UNSUPPORTED_SCHEMA_VERSION"]
    assert result.diagnostics.loc[0, "field_name"] == "schema_version"
    assert result.file_summary["total_rows"] == 1
    assert result.file_summary["accepted_rows"] == 0
    assert result.file_summary["rejected_rows"] == 0
    assert result.rejected_rows.empty


def test_distinct_invalid_schema_tokens_emit_once_in_safe_lexical_order(tmp_path):
    path = _write_csv(
        tmp_path,
        [
            _row(local_record_id="one", schema_version="z-version"),
            _row(local_record_id="two", schema_version=""),
            _row(local_record_id="three", schema_version="a-version"),
            _row(local_record_id="four", schema_version="z-version"),
        ],
    )

    result = _process(path)

    assert _codes(result) == ["MCV100_UNSUPPORTED_SCHEMA_VERSION"] * 3
    assert result.diagnostics["raw_value"].tolist() == [
        "<empty>",
        "a-version",
        "z-version",
    ]


def test_long_distinct_schema_versions_do_not_collapse_and_are_deterministic(tmp_path):
    shared_prefix = "schema-" + ("x" * 200)
    rows = [
        _row(local_record_id="one", schema_version=f"{shared_prefix}-beta"),
        _row(local_record_id="two", schema_version=f"{shared_prefix}-alpha"),
    ]
    first_path = _write_csv(tmp_path, rows, name="schema-first.csv")
    second_path = _write_csv(
        tmp_path,
        list(reversed(rows)),
        name="schema-second.csv",
    )

    first = _process(first_path)
    second = _process(second_path)

    assert _codes(first) == ["MCV100_UNSUPPORTED_SCHEMA_VERSION"] * 2
    assert len(first.diagnostics) == 2
    assert first.diagnostics["raw_value"].map(len).le(160).all()
    pd.testing.assert_frame_equal(first.diagnostics, second.diagnostics)


@pytest.mark.parametrize("field_name", STRUCTURAL_REQUIRED_VALUES)
@pytest.mark.parametrize("missing_value", ["", "  \t "])
def test_missing_structural_required_values_emit_mcv200_only(
    tmp_path, field_name, missing_value
):
    path = _write_csv(tmp_path, [_row(**{field_name: missing_value})])

    result = _process(path)

    assert result.file_outcome == "accepted"
    assert _codes(result) == ["MCV200_MISSING_REQUIRED_VALUE"]
    assert result.diagnostics.loc[0, "field_name"] == field_name
    assert result.file_summary["rejected_rows"] == 1


@pytest.mark.parametrize(
    ("field_name", "specific_code"),
    [
        ("season", "MCV202_INVALID_SEASON"),
        ("reviewed_at", "MCV203_INVALID_REVIEWED_AT"),
        ("source_type", "MCV204_INVALID_SOURCE_TYPE"),
    ],
)
def test_missing_value_precedence_suppresses_field_specific_diagnostic(
    tmp_path, field_name, specific_code
):
    path = _write_csv(tmp_path, [_row(**{field_name: ""})])

    result = _process(path)

    assert _codes(result) == ["MCV200_MISSING_REQUIRED_VALUE"]
    assert specific_code not in _codes(result)


def test_independent_row_errors_are_all_reported_in_canonical_field_order(tmp_path):
    path = _write_csv(
        tmp_path,
        [_row(player="", season="invalid", source_type="bad", reviewed_at="naive")],
    )

    result = _process(path)

    assert result.diagnostics["field_name"].tolist() == [
        "player",
        "season",
        "source_type",
        "reviewed_at",
    ]
    assert _codes(result) == [
        "MCV200_MISSING_REQUIRED_VALUE",
        "MCV202_INVALID_SEASON",
        "MCV204_INVALID_SOURCE_TYPE",
        "MCV203_INVALID_REVIEWED_AT",
    ]


@pytest.mark.parametrize(
    "invalid_season",
    ["2024.0", "2024/25", "2024-25", " 2024 ", "season-2024"],
)
def test_populated_invalid_season_emits_mcv202(tmp_path, invalid_season):
    path = _write_csv(tmp_path, [_row(season=invalid_season)])

    result = _process(path)

    assert _codes(result) == ["MCV202_INVALID_SEASON"]


def test_exact_four_digit_season_is_valid(tmp_path):
    path = _write_csv(tmp_path, [_row(season="2024")])

    result = _process(path)

    assert result.diagnostics.empty


@pytest.mark.parametrize(
    "valid_reviewed_at",
    [
        "2026-07-22T10:00:00Z",
        "2026-07-22T10:00:00+02:00",
        "2026-07-22T10:00:00.123456-03:30",
    ],
)
def test_valid_reviewed_at_requires_iso_datetime_with_timezone(
    tmp_path, valid_reviewed_at
):
    path = _write_csv(tmp_path, [_row(reviewed_at=valid_reviewed_at)])

    result = _process(path)

    assert result.diagnostics.empty


@pytest.mark.parametrize(
    "invalid_reviewed_at",
    [
        "2026-07-22",
        "2026-07-22T10:00:00",
        "2026-07-22T10:00:00+99:00",
        " 2026-07-22T10:00:00Z ",
        "not-a-date",
    ],
)
def test_populated_invalid_reviewed_at_emits_mcv203(tmp_path, invalid_reviewed_at):
    path = _write_csv(tmp_path, [_row(reviewed_at=invalid_reviewed_at)])

    result = _process(path)

    assert _codes(result) == ["MCV203_INVALID_REVIEWED_AT"]


@pytest.mark.parametrize("valid_source_type", ALLOWED_SOURCE_TYPES)
def test_allowed_source_types_are_exactly_accepted(tmp_path, valid_source_type):
    path = _write_csv(tmp_path, [_row(source_type=valid_source_type)])

    result = _process(path)

    assert result.diagnostics.empty


@pytest.mark.parametrize(
    "invalid_source_type",
    ["Official-Public", " official-public", "official-public ", "official", "unknown"],
)
def test_invalid_source_type_emits_mcv204(tmp_path, invalid_source_type):
    path = _write_csv(tmp_path, [_row(source_type=invalid_source_type)])

    result = _process(path)

    assert _codes(result) == ["MCV204_INVALID_SOURCE_TYPE"]


def test_structural_row_error_fixture_reports_expected_independent_errors():
    result = _process(FIXTURE_DIR / "structural_row_errors.csv")

    assert result.file_outcome == "accepted"
    assert result.file_summary["total_rows"] == 4
    assert result.file_summary["accepted_rows"] == 0
    assert result.file_summary["rejected_rows"] == 4
    assert sorted(_codes(result)) == sorted(
        [
            "MCV200_MISSING_REQUIRED_VALUE",
            "MCV202_INVALID_SEASON",
            "MCV203_INVALID_REVIEWED_AT",
            "MCV204_INVALID_SOURCE_TYPE",
        ]
    )


def test_duplicate_local_record_ids_reject_every_implicated_row():
    result = _process(FIXTURE_DIR / "duplicate_local_record_ids.csv")

    assert result.file_outcome == "accepted"
    assert result.file_summary["total_rows"] == 2
    assert result.file_summary["accepted_rows"] == 0
    assert result.file_summary["rejected_rows"] == 2
    assert result.file_summary["duplicate_groups"] == 0
    assert _codes(result) == [
        "MCV201_DUPLICATE_LOCAL_RECORD_ID",
        "MCV201_DUPLICATE_LOCAL_RECORD_ID",
    ]
    assert result.rejected_rows["local_record_id"].tolist() == [
        "synthetic-duplicate-001",
        "synthetic-duplicate-001",
    ]


def test_missing_local_record_id_is_not_grouped_as_duplicate(tmp_path):
    path = _write_csv(
        tmp_path,
        [
            _row(local_record_id="", player="Player Alpha"),
            _row(local_record_id="", player="Player Beta"),
        ],
    )

    result = _process(path)

    assert _codes(result) == [
        "MCV200_MISSING_REQUIRED_VALUE",
        "MCV200_MISSING_REQUIRED_VALUE",
    ]
    assert "MCV201_DUPLICATE_LOCAL_RECORD_ID" not in _codes(result)


def test_no_matching_duplicate_id_does_not_reject_rows(tmp_path):
    path = _write_csv(
        tmp_path,
        [
            _row(local_record_id="one"),
            _row(local_record_id="two", player="Player Beta"),
        ],
    )

    result = _process(path)

    assert result.file_summary["accepted_rows"] == 2
    assert result.rejected_rows.empty


def test_result_and_output_dataframes_have_exact_public_schemas(tmp_path):
    path = _write_csv(tmp_path, [_row(player="")])

    result = _process(path)

    assert isinstance(result, ManualMarketContextProcessingResult)
    assert result.accepted_observations.columns.tolist() == list(OBSERVATION_COLUMNS)
    assert result.review_required_observations.columns.tolist() == list(
        OBSERVATION_COLUMNS
    )
    assert result.rejected_rows.columns.tolist() == list(REJECTED_ROW_COLUMNS)
    assert result.diagnostics.columns.tolist() == list(DIAGNOSTIC_COLUMNS)
    assert result.accepted_observations.empty
    assert result.review_required_observations.empty
    assert "field_sort_rank" not in result.diagnostics.columns


def test_result_dataclass_is_frozen(tmp_path):
    result = _process(_write_csv(tmp_path, [BASE_ROW]))

    with pytest.raises(FrozenInstanceError):
        result.file_outcome = "rejected"


def test_each_call_returns_independent_dataframes(tmp_path):
    path = _write_csv(tmp_path, [BASE_ROW])

    first = _process(path)
    second = _process(path)

    assert first.accepted_observations is not second.accepted_observations
    assert first.review_required_observations is not second.review_required_observations
    assert first.rejected_rows is not second.rejected_rows
    assert first.diagnostics is not second.diagnostics


def test_summary_has_exact_fields_in_deterministic_order(tmp_path):
    result = _process(_write_csv(tmp_path, [_row(player="")]))

    assert list(result.file_summary) == [
        "input_contract_version",
        "policy_version",
        "stage",
        "file_outcome",
        "total_rows",
        "accepted_rows",
        "accepted_with_warning_rows",
        "partially_accepted_rows",
        "review_required_rows",
        "rejected_rows",
        "accepted_observations",
        "review_required_observations",
        "rejected_field_observations",
        "diagnostics_by_severity",
        "diagnostics_by_code",
        "duplicate_groups",
        "conflict_groups",
        "current_observations",
        "stale_observations",
        "unknown_freshness_observations",
        "not_applicable_observations",
        "future_invalid_observations",
        "market_value_zero_observation_count",
        "effective_eligible_observation_count",
    ]
    assert result.file_summary["input_contract_version"] == INPUT_CONTRACT_VERSION
    assert result.file_summary["policy_version"] == PROCESSING_POLICY_VERSION
    assert result.file_summary["stage"] == STAGE_NAME
    assert result.file_summary["diagnostics_by_severity"] == {"error": 1}
    assert result.file_summary["diagnostics_by_code"] == {
        "MCV200_MISSING_REQUIRED_VALUE": 1
    }
    assert result.file_summary["duplicate_groups"] == 0
    assert result.file_summary["conflict_groups"] == 0
    assert result.file_summary["accepted_observations"] == 0
    assert result.file_summary["effective_eligible_observation_count"] == 0


def test_rejected_rows_contain_only_rejected_rows_with_safe_identity(tmp_path):
    path = _write_csv(
        tmp_path,
        [
            _row(local_record_id="accepted"),
            _row(
                local_record_id="rejected",
                player="Player\nUnsafe",
                season="invalid",
            ),
        ],
    )

    result = _process(path)

    assert result.file_summary["accepted_rows"] == 1
    assert len(result.rejected_rows) == 1
    rejected = result.rejected_rows.iloc[0]
    assert rejected["local_record_id"] == "rejected"
    assert rejected["row_outcome"] == "rejected"
    assert rejected["primary_diagnostic_code"] == "MCV202_INVALID_SEASON"
    assert rejected["diagnostic_count"] == 1
    assert "\n" not in rejected["safe_row_reference"]
    assert "\\n" in rejected["safe_row_reference"]


def test_diagnostic_raw_value_is_bounded_and_escapes_newlines(tmp_path):
    invalid = ("bad\nvalue" * 100)
    path = _write_csv(tmp_path, [_row(source_type=invalid)])

    result = _process(path)

    raw_value = result.diagnostics.loc[0, "raw_value"]
    assert "\n" not in raw_value
    assert "\\n" in raw_value
    assert len(raw_value) <= 160


def test_diagnostic_order_is_zero_based_consecutive_after_final_sort(tmp_path):
    path = _write_csv(
        tmp_path,
        [
            _row(local_record_id="b", player="", season="invalid"),
            _row(local_record_id="a", source_type="bad", reviewed_at="naive"),
        ],
    )

    result = _process(path)

    assert result.diagnostics["diagnostic_order"].tolist() == [0, 1, 2, 3]
    assert result.diagnostics["local_record_id"].tolist() == ["a", "a", "b", "b"]
    assert result.diagnostics["field_name"].tolist() == [
        "source_type",
        "reviewed_at",
        "player",
        "season",
    ]


def test_equivalent_reordered_rows_produce_identical_public_outputs(tmp_path):
    rows = [
        _row(local_record_id="b", player="", season="invalid"),
        _row(local_record_id="a", source_type="bad"),
        _row(local_record_id="c"),
    ]
    first_path = _write_csv(tmp_path, rows, name="first.csv")
    second_path = _write_csv(tmp_path, list(reversed(rows)), name="second.csv")

    first = _process(first_path)
    second = _process(second_path)

    pd.testing.assert_frame_equal(first.diagnostics, second.diagnostics)
    pd.testing.assert_frame_equal(first.rejected_rows, second.rejected_rows)
    assert first.file_summary == second.file_summary


def test_long_distinct_row_ids_use_full_internal_identity_for_ordering(tmp_path):
    shared_prefix = "record-" + ("x" * 200)
    rows = [
        _row(local_record_id=f"{shared_prefix}-beta", season="invalid"),
        _row(local_record_id=f"{shared_prefix}-alpha", season="invalid"),
    ]
    first_path = _write_csv(tmp_path, rows, name="rows-first.csv")
    second_path = _write_csv(
        tmp_path,
        list(reversed(rows)),
        name="rows-second.csv",
    )

    first = _process(first_path)
    second = _process(second_path)

    pd.testing.assert_frame_equal(first.diagnostics, second.diagnostics)
    pd.testing.assert_frame_equal(first.rejected_rows, second.rejected_rows)
    assert first.file_summary == second.file_summary
    expected_ids = [
        f"{shared_prefix}-alpha",
        f"{shared_prefix}-beta",
    ]
    assert first.rejected_rows["local_record_id"].tolist() == expected_ids
    assert first.diagnostics["local_record_id"].tolist() == expected_ids
    assert all(not value.endswith("...") for value in expected_ids)
    assert set(first.diagnostics["local_record_id"]) == set(
        first.rejected_rows["local_record_id"]
    )


def test_rejected_rows_use_full_diagnostic_signature_as_final_tiebreaker(tmp_path):
    duplicate_id = "synthetic-shared-record"
    rows = [
        _row(
            local_record_id=duplicate_id,
            source_type="invalid-source",
        ),
        _row(
            local_record_id=duplicate_id,
            source_type="invalid-source",
            reviewed_at="naive-review-time",
        ),
    ]
    first_path = _write_csv(tmp_path, rows, name="tie-first.csv")
    second_path = _write_csv(
        tmp_path,
        list(reversed(rows)),
        name="tie-second.csv",
    )

    first = _process(first_path)
    second = _process(second_path)

    assert first.rejected_rows["primary_diagnostic_code"].tolist() == [
        "MCV201_DUPLICATE_LOCAL_RECORD_ID",
        "MCV201_DUPLICATE_LOCAL_RECORD_ID",
    ]
    assert first.rejected_rows["diagnostic_count"].tolist() == [2, 3]
    assert first.rejected_rows["safe_row_reference"].nunique() == 1
    pd.testing.assert_frame_equal(first.diagnostics, second.diagnostics)
    pd.testing.assert_frame_equal(first.rejected_rows, second.rejected_rows)
    assert first.file_summary == second.file_summary


def test_file_diagnostic_phase_order_is_deterministic(tmp_path):
    columns = tuple(
        column for column in REQUIRED_COLUMNS if column not in {"player", "season"}
    ) + ("zeta", "alpha")
    path = _write_csv(tmp_path, [], columns=columns)

    result = _process(path)

    assert result.diagnostics["diagnostic_code"].tolist() == [
        "MCV101_MISSING_REQUIRED_COLUMN",
        "MCV101_MISSING_REQUIRED_COLUMN",
        "MCV103_UNKNOWN_COLUMN",
        "MCV103_UNKNOWN_COLUMN",
    ]
    assert result.diagnostics["field_name"].tolist() == [
        "player",
        "season",
        "alpha",
        "zeta",
    ]


def test_all_stage_a_diagnostics_are_errors_with_approved_scopes(tmp_path):
    path = _write_csv(tmp_path, [_row(player="", season="invalid")])

    result = _process(path)

    assert set(result.diagnostics["severity"]) == {"error"}
    assert set(result.diagnostics["scope"]) == {"row"}
    assert result.diagnostics["conflict_group_id"].isna().all()
    assert result.diagnostics["field_outcome"].isna().all()
