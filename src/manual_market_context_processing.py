from __future__ import annotations

import csv
import io
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


INPUT_CONTRACT_VERSION = "manual-market-context-input-v1"
PROCESSING_POLICY_VERSION = "manual-market-context-policy-v1"
STAGE_NAME = "A"

CANONICAL_COLUMNS = (
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

REQUIRED_COLUMNS = (
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

STRUCTURAL_REQUIRED_VALUES = (
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

ALLOWED_SOURCE_TYPES = (
    "official-public",
    "provider-public",
    "manual-reference",
    "internal-reviewed",
    "other-reviewed",
)

MCV100_UNSUPPORTED_SCHEMA_VERSION = "MCV100_UNSUPPORTED_SCHEMA_VERSION"
MCV101_MISSING_REQUIRED_COLUMN = "MCV101_MISSING_REQUIRED_COLUMN"
MCV102_DUPLICATE_HEADER = "MCV102_DUPLICATE_HEADER"
MCV103_UNKNOWN_COLUMN = "MCV103_UNKNOWN_COLUMN"
MCV104_INVALID_ENCODING = "MCV104_INVALID_ENCODING"
MCV105_INVALID_DELIMITER = "MCV105_INVALID_DELIMITER"
MCV200_MISSING_REQUIRED_VALUE = "MCV200_MISSING_REQUIRED_VALUE"
MCV201_DUPLICATE_LOCAL_RECORD_ID = "MCV201_DUPLICATE_LOCAL_RECORD_ID"
MCV202_INVALID_SEASON = "MCV202_INVALID_SEASON"
MCV203_INVALID_REVIEWED_AT = "MCV203_INVALID_REVIEWED_AT"
MCV204_INVALID_SOURCE_TYPE = "MCV204_INVALID_SOURCE_TYPE"

OBSERVATION_COLUMNS = (
    "local_record_id",
    "player",
    "team",
    "league",
    "season",
    "field_name",
    "raw_value",
    "normalized_value",
    "effective_value_date",
    "freshness_status",
    "source_name",
    "source_type",
    "source_url",
    "source_reference",
    "reviewed_at",
    "reviewer",
    "confidence",
    "review_status",
    "field_outcome",
    "conflict_group_id",
    "effective_eligible",
)

REJECTED_ROW_COLUMNS = (
    "local_record_id",
    "player",
    "team",
    "league",
    "season",
    "row_outcome",
    "primary_diagnostic_code",
    "diagnostic_count",
    "safe_row_reference",
)

DIAGNOSTIC_COLUMNS = (
    "diagnostic_code",
    "severity",
    "scope",
    "message",
    "local_record_id",
    "field_name",
    "conflict_group_id",
    "raw_value",
    "normalized_value",
    "row_outcome",
    "field_outcome",
    "diagnostic_order",
)

_FILE_PHASE_ORDER = {
    MCV104_INVALID_ENCODING: 0,
    MCV105_INVALID_DELIMITER: 1,
    MCV102_DUPLICATE_HEADER: 2,
    MCV101_MISSING_REQUIRED_COLUMN: 3,
    MCV103_UNKNOWN_COLUMN: 4,
    MCV100_UNSUPPORTED_SCHEMA_VERSION: 5,
}
_CANONICAL_FIELD_RANK = {
    field_name: index for index, field_name in enumerate(CANONICAL_COLUMNS)
}
_SEASON_PATTERN = re.compile(r"^\d{4}$")
_REVIEWED_AT_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    r"(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
_MAX_SAFE_VALUE_LENGTH = 160
_MAX_ROW_REFERENCE_PART_LENGTH = 80
_STRUCTURAL_IDENTITY_FIELDS = (
    "local_record_id",
    "player",
    "team",
    "league",
    "season",
)


@dataclass(frozen=True)
class ManualMarketContextProcessingResult:
    file_outcome: str
    accepted_observations: pd.DataFrame
    review_required_observations: pd.DataFrame
    rejected_rows: pd.DataFrame
    diagnostics: pd.DataFrame
    file_summary: dict[str, object]


def process_reviewed_market_context(
    input_path: Path,
    *,
    ingested_at: datetime,
    strict: bool = True,
) -> ManualMarketContextProcessingResult:
    path = Path(input_path)
    with path.open("rb") as input_file:
        if not strict:
            raise ValueError("strict=False is not approved for Stage A")
        if not _is_timezone_aware(ingested_at):
            raise ValueError("ingested_at must be timezone-aware")
        payload = input_file.read()

    if payload.startswith(b"\xef\xbb\xbf"):
        return _file_rejected_result(
            [_diagnostic(MCV104_INVALID_ENCODING, "file")],
        )

    try:
        decoded_text = payload.decode("utf-8")
    except UnicodeDecodeError:
        return _file_rejected_result(
            [_diagnostic(MCV104_INVALID_ENCODING, "file")],
        )

    if not decoded_text.strip():
        diagnostics = [
            _diagnostic(
                MCV101_MISSING_REQUIRED_COLUMN,
                "file",
                field_name=field_name,
            )
            for field_name in REQUIRED_COLUMNS
        ]
        return _file_rejected_result(diagnostics)

    if _has_invalid_alternate_delimiter(decoded_text):
        return _file_rejected_result(
            [_diagnostic(MCV105_INVALID_DELIMITER, "file")],
        )

    header = _read_header(decoded_text)
    header_diagnostics = _validate_header(header)
    if header_diagnostics:
        return _file_rejected_result(header_diagnostics)

    rows_df = pd.read_csv(
        io.StringIO(decoded_text),
        dtype=str,
        keep_default_na=False,
        na_filter=False,
    )
    total_rows = len(rows_df)

    schema_diagnostics = _validate_schema_versions(rows_df)
    if schema_diagnostics:
        return _file_rejected_result(schema_diagnostics, total_rows=total_rows)

    row_diagnostics = _validate_rows(rows_df)
    sorted_diagnostics = _finalize_diagnostics(row_diagnostics)
    rejected_rows = _build_rejected_rows(rows_df, row_diagnostics)
    rejected_count = len(rejected_rows)
    accepted_count = total_rows - rejected_count
    file_outcome = "accepted"

    return ManualMarketContextProcessingResult(
        file_outcome=file_outcome,
        accepted_observations=_empty_observations(),
        review_required_observations=_empty_observations(),
        rejected_rows=rejected_rows,
        diagnostics=sorted_diagnostics,
        file_summary=_build_summary(
            file_outcome=file_outcome,
            total_rows=total_rows,
            accepted_rows=accepted_count,
            rejected_rows=rejected_count,
            diagnostics=sorted_diagnostics,
        ),
    )


def _is_timezone_aware(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() is not None


def _has_invalid_alternate_delimiter(decoded_text: str) -> bool:
    first_non_empty_line = next(
        line for line in decoded_text.splitlines() if line.strip()
    )
    comma_columns = next(csv.reader([first_non_empty_line], delimiter=","))
    if len(comma_columns) > 1:
        return False
    semicolon_columns = next(csv.reader([first_non_empty_line], delimiter=";"))
    if len(semicolon_columns) > 1:
        return True
    tab_columns = next(csv.reader([first_non_empty_line], delimiter="\t"))
    return len(tab_columns) > 1


def _read_header(decoded_text: str) -> list[str]:
    return next(csv.reader(io.StringIO(decoded_text), delimiter=","))


def _validate_header(header: list[str]) -> list[dict[str, Any]]:
    counts = Counter(header)
    duplicate_columns = sorted(
        field_name for field_name, count in counts.items() if count > 1
    )
    missing_columns = [
        field_name for field_name in REQUIRED_COLUMNS if field_name not in counts
    ]
    unknown_columns = sorted(
        field_name for field_name in counts if field_name not in CANONICAL_COLUMNS
    )

    diagnostics = [
        _diagnostic(
            MCV102_DUPLICATE_HEADER,
            "file",
            field_name=field_name,
        )
        for field_name in duplicate_columns
    ]
    diagnostics.extend(
        _diagnostic(
            MCV101_MISSING_REQUIRED_COLUMN,
            "file",
            field_name=field_name,
        )
        for field_name in missing_columns
    )
    diagnostics.extend(
        _diagnostic(
            MCV103_UNKNOWN_COLUMN,
            "file",
            field_name=field_name,
        )
        for field_name in unknown_columns
    )
    return diagnostics


def _validate_schema_versions(rows_df: pd.DataFrame) -> list[dict[str, Any]]:
    invalid_token_keys: set[tuple[int, str]] = set()
    for value in rows_df["schema_version"].tolist():
        if value == INPUT_CONTRACT_VERSION:
            continue
        if _is_missing(value):
            invalid_token_keys.add((0, ""))
        else:
            invalid_token_keys.add((1, str(value)))

    return [
        _diagnostic(
            MCV100_UNSUPPORTED_SCHEMA_VERSION,
            "file",
            field_name="schema_version",
            raw_value=token,
        )
        for _, token in sorted(invalid_token_keys)
    ]


def _validate_rows(
    rows_df: pd.DataFrame,
) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    duplicate_ids = _duplicate_local_record_ids(rows_df)

    for row_token, row in rows_df.iterrows():
        identity_sort_key = _row_identity_sort_key(row)
        original_local_record_id = row.get("local_record_id", "")
        local_record_id = (
            ""
            if _is_missing(original_local_record_id)
            else str(original_local_record_id)
        )
        for field_name in STRUCTURAL_REQUIRED_VALUES:
            raw_value = row.get(field_name, "")
            if _is_missing(raw_value):
                diagnostics.append(
                    _diagnostic(
                        MCV200_MISSING_REQUIRED_VALUE,
                        "row",
                        local_record_id=local_record_id,
                        field_name=field_name,
                        raw_value=raw_value,
                        row_token=int(row_token),
                        identity_sort_key=identity_sort_key,
                    )
                )

        season = row.get("season", "")
        if not _is_missing(season) and not _SEASON_PATTERN.fullmatch(season):
            diagnostics.append(
                _diagnostic(
                    MCV202_INVALID_SEASON,
                    "row",
                    local_record_id=local_record_id,
                    field_name="season",
                    raw_value=season,
                    row_token=int(row_token),
                    identity_sort_key=identity_sort_key,
                )
            )

        reviewed_at = row.get("reviewed_at", "")
        if not _is_missing(reviewed_at) and not _is_valid_reviewed_at(reviewed_at):
            diagnostics.append(
                _diagnostic(
                    MCV203_INVALID_REVIEWED_AT,
                    "row",
                    local_record_id=local_record_id,
                    field_name="reviewed_at",
                    raw_value=reviewed_at,
                    row_token=int(row_token),
                    identity_sort_key=identity_sort_key,
                )
            )

        source_type = row.get("source_type", "")
        if (
            not _is_missing(source_type)
            and source_type not in ALLOWED_SOURCE_TYPES
        ):
            diagnostics.append(
                _diagnostic(
                    MCV204_INVALID_SOURCE_TYPE,
                    "row",
                    local_record_id=local_record_id,
                    field_name="source_type",
                    raw_value=source_type,
                    row_token=int(row_token),
                    identity_sort_key=identity_sort_key,
                )
            )

        exact_local_record_id = row.get("local_record_id", "")
        if (
            not _is_missing(exact_local_record_id)
            and exact_local_record_id in duplicate_ids
        ):
            diagnostics.append(
                _diagnostic(
                    MCV201_DUPLICATE_LOCAL_RECORD_ID,
                    "row",
                    local_record_id=local_record_id,
                    field_name="local_record_id",
                    raw_value=exact_local_record_id,
                    row_token=int(row_token),
                    identity_sort_key=identity_sort_key,
                )
            )

    return diagnostics


def _duplicate_local_record_ids(rows_df: pd.DataFrame) -> set[str]:
    values = [
        value
        for value in rows_df["local_record_id"].tolist()
        if not _is_missing(value)
    ]
    counts = Counter(values)
    return {value for value, count in counts.items() if count > 1}


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    return str(value).strip() == ""


def _is_valid_reviewed_at(value: str) -> bool:
    if not _REVIEWED_AT_PATTERN.fullmatch(value):
        return False
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return False
    return _is_timezone_aware(parsed)


def _diagnostic(
    diagnostic_code: str,
    scope: str,
    *,
    local_record_id: str | None = None,
    field_name: str | None = None,
    raw_value: Any = None,
    row_token: int | None = None,
    identity_sort_key: tuple[str, ...] = (),
) -> dict[str, Any]:
    messages = {
        MCV100_UNSUPPORTED_SCHEMA_VERSION: "The schema version is not approved.",
        MCV101_MISSING_REQUIRED_COLUMN: "A required column is missing.",
        MCV102_DUPLICATE_HEADER: "A column name is duplicated.",
        MCV103_UNKNOWN_COLUMN: "An unknown column is present.",
        MCV104_INVALID_ENCODING: "The file must be UTF-8 without a BOM.",
        MCV105_INVALID_DELIMITER: "The file must use a comma delimiter.",
        MCV200_MISSING_REQUIRED_VALUE: "A structurally required value is missing.",
        MCV201_DUPLICATE_LOCAL_RECORD_ID: "The local record ID is duplicated.",
        MCV202_INVALID_SEASON: "Season must contain exactly four digits.",
        MCV203_INVALID_REVIEWED_AT: (
            "reviewed_at must be an ISO datetime with an explicit timezone."
        ),
        MCV204_INVALID_SOURCE_TYPE: "source_type is not an approved value.",
    }
    return {
        "diagnostic_code": diagnostic_code,
        "severity": "error",
        "scope": scope,
        "message": messages[diagnostic_code],
        "local_record_id": local_record_id,
        "field_name": field_name,
        "conflict_group_id": None,
        "raw_value": _safe_value(raw_value),
        "normalized_value": None,
        "row_outcome": "rejected" if scope == "row" else None,
        "field_outcome": None,
        "diagnostic_order": None,
        "_row_token": row_token,
        "_identity_sort_key": identity_sort_key,
        "_local_record_id_sort_value": (
            identity_sort_key[0] if identity_sort_key else ""
        ),
        "_raw_sort_value": _full_sort_value(raw_value),
    }


def _safe_value(value: Any, *, max_length: int = _MAX_SAFE_VALUE_LENGTH) -> str | None:
    if value is None:
        return None
    text = str(value)
    if not text.strip():
        return "<empty>"
    text = (
        text.replace("\\", "\\\\")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    if len(text) > max_length:
        return f"{text[: max_length - 3]}..."
    return text



def _full_sort_value(value: Any) -> str:
    return "" if value is None else str(value)


def _row_identity_sort_key(row: pd.Series) -> tuple[str, ...]:
    return tuple(
        _full_sort_value(row.get(field_name, ""))
        for field_name in _STRUCTURAL_IDENTITY_FIELDS
    )


def _diagnostic_sort_key(diagnostic: dict[str, Any]) -> tuple[Any, ...]:
    scope_rank = 0 if diagnostic["scope"] == "file" else 1
    code = diagnostic["diagnostic_code"]
    field_name = diagnostic["field_name"] or ""
    if scope_rank == 0:
        phase_rank = _FILE_PHASE_ORDER[code]
        if code == MCV101_MISSING_REQUIRED_COLUMN:
            field_rank = _CANONICAL_FIELD_RANK.get(field_name, len(CANONICAL_COLUMNS))
            lexical_field = ""
        elif code in {MCV102_DUPLICATE_HEADER, MCV103_UNKNOWN_COLUMN}:
            field_rank = len(CANONICAL_COLUMNS)
            lexical_field = field_name
        else:
            field_rank = _CANONICAL_FIELD_RANK.get(field_name, len(CANONICAL_COLUMNS))
            lexical_field = field_name
        return (
            scope_rank,
            phase_rank,
            field_rank,
            lexical_field,
            code,
            diagnostic["_raw_sort_value"],
        )

    canonical_rank = _CANONICAL_FIELD_RANK.get(field_name)
    return (
        scope_rank,
        diagnostic["_local_record_id_sort_value"],
        diagnostic["_identity_sort_key"],
        canonical_rank if canonical_rank is not None else len(CANONICAL_COLUMNS),
        "" if canonical_rank is not None else field_name,
        code,
        diagnostic["_raw_sort_value"],
    )


def _finalize_diagnostics(
    diagnostics: list[dict[str, Any]],
) -> pd.DataFrame:
    ordered = sorted(diagnostics, key=_diagnostic_sort_key)
    public_rows: list[dict[str, Any]] = []
    for diagnostic_order, diagnostic in enumerate(ordered):
        public_row = {
            column: diagnostic.get(column) for column in DIAGNOSTIC_COLUMNS
        }
        public_row["diagnostic_order"] = diagnostic_order
        public_rows.append(public_row)
    return pd.DataFrame(public_rows, columns=DIAGNOSTIC_COLUMNS)


def _build_rejected_rows(
    rows_df: pd.DataFrame,
    row_diagnostics: list[dict[str, Any]],
) -> pd.DataFrame:
    diagnostics_by_row: dict[int, list[dict[str, Any]]] = {}
    for diagnostic in row_diagnostics:
        row_token = diagnostic["_row_token"]
        diagnostics_by_row.setdefault(row_token, []).append(diagnostic)

    rejected: list[dict[str, Any]] = []
    for row_token, diagnostics in diagnostics_by_row.items():
        row = rows_df.loc[row_token]
        primary = min(diagnostics, key=_diagnostic_sort_key)
        rejected.append(
            {
                "local_record_id": row.get("local_record_id", ""),
                "player": row.get("player", ""),
                "team": row.get("team", ""),
                "league": row.get("league", ""),
                "season": row.get("season", ""),
                "row_outcome": "rejected",
                "primary_diagnostic_code": primary["diagnostic_code"],
                "diagnostic_count": len(diagnostics),
                "safe_row_reference": _safe_row_reference(row),
                "_diagnostic_sort_signature": (
                    _rejected_row_diagnostic_signature(diagnostics)
                ),
            }
        )

    rejected.sort(
        key=lambda row: (
            _full_sort_value(row["local_record_id"]),
            _full_sort_value(row["player"]),
            _full_sort_value(row["team"]),
            _full_sort_value(row["league"]),
            _full_sort_value(row["season"]),
            row["primary_diagnostic_code"],
            row["safe_row_reference"],
            row["_diagnostic_sort_signature"],
        )
    )
    return pd.DataFrame(rejected, columns=REJECTED_ROW_COLUMNS).reset_index(drop=True)


def _rejected_row_diagnostic_signature(
    diagnostics: list[dict[str, Any]],
) -> tuple[tuple[Any, ...], ...]:
    return tuple(
        sorted(
            (
                _CANONICAL_FIELD_RANK.get(
                    diagnostic["field_name"],
                    len(CANONICAL_COLUMNS),
                ),
                diagnostic["field_name"] or "",
                diagnostic["diagnostic_code"],
                diagnostic["_raw_sort_value"],
            )
            for diagnostic in diagnostics
        )
    )


def _safe_row_reference(row: pd.Series) -> str:
    parts = []
    for field_name in _STRUCTURAL_IDENTITY_FIELDS:
        safe_value = _safe_value(
            row.get(field_name, ""),
            max_length=_MAX_ROW_REFERENCE_PART_LENGTH,
        )
        parts.append(f"{field_name}={safe_value or '<empty>'}")
    return "|".join(parts)


def _empty_observations() -> pd.DataFrame:
    return pd.DataFrame(columns=OBSERVATION_COLUMNS)


def _file_rejected_result(
    diagnostics: list[dict[str, Any]],
    *,
    total_rows: int = 0,
) -> ManualMarketContextProcessingResult:
    finalized = _finalize_diagnostics(diagnostics)
    return ManualMarketContextProcessingResult(
        file_outcome="rejected",
        accepted_observations=_empty_observations(),
        review_required_observations=_empty_observations(),
        rejected_rows=pd.DataFrame(columns=REJECTED_ROW_COLUMNS),
        diagnostics=finalized,
        file_summary=_build_summary(
            file_outcome="rejected",
            total_rows=total_rows,
            accepted_rows=0,
            rejected_rows=0,
            diagnostics=finalized,
        ),
    )


def _build_summary(
    *,
    file_outcome: str,
    total_rows: int,
    accepted_rows: int,
    rejected_rows: int,
    diagnostics: pd.DataFrame,
) -> dict[str, object]:
    severity_counts = _sorted_counts(diagnostics, "severity")
    code_counts = _sorted_counts(diagnostics, "diagnostic_code")
    return {
        "input_contract_version": INPUT_CONTRACT_VERSION,
        "policy_version": PROCESSING_POLICY_VERSION,
        "stage": STAGE_NAME,
        "file_outcome": file_outcome,
        "total_rows": int(total_rows),
        "accepted_rows": int(accepted_rows),
        "accepted_with_warning_rows": 0,
        "partially_accepted_rows": 0,
        "review_required_rows": 0,
        "rejected_rows": int(rejected_rows),
        "accepted_observations": 0,
        "review_required_observations": 0,
        "rejected_field_observations": 0,
        "diagnostics_by_severity": severity_counts,
        "diagnostics_by_code": code_counts,
        "duplicate_groups": 0,
        "conflict_groups": 0,
        "current_observations": 0,
        "stale_observations": 0,
        "unknown_freshness_observations": 0,
        "not_applicable_observations": 0,
        "future_invalid_observations": 0,
        "market_value_zero_observation_count": 0,
        "effective_eligible_observation_count": 0,
    }


def _sorted_counts(dataframe: pd.DataFrame, column: str) -> dict[str, int]:
    if dataframe.empty:
        return {}
    counts = Counter(dataframe[column].dropna().tolist())
    return {key: int(counts[key]) for key in sorted(counts)}
