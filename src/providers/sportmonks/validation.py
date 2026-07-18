from __future__ import annotations

import re
from pathlib import Path


class SportmonksValidationError(ValueError):
    """Raised when local Sportmonks transform input fails a safety check."""


def validate_payload_shape(payload: object) -> dict:
    """Validate the top-level object and data list."""
    if not isinstance(payload, dict):
        raise SportmonksValidationError("Payload must be an object.")
    if "data" not in payload:
        raise SportmonksValidationError("Payload must contain a data list.")
    if not isinstance(payload["data"], list):
        raise SportmonksValidationError("Payload data must be a list.")
    return payload


def validate_scope(
    record: dict,
    *,
    expected_team_id: int,
    expected_season_id: int,
) -> None:
    """Validate a squad record against the explicitly selected scope."""
    if not isinstance(record, dict):
        raise SportmonksValidationError("Each payload data record must be an object.")
    if record.get("player_id") is None:
        raise SportmonksValidationError("Record player_id is required.")
    if record.get("team_id") != expected_team_id:
        raise SportmonksValidationError("Record team_id does not match expected scope.")
    if record.get("season_id") != expected_season_id:
        raise SportmonksValidationError("Record season_id does not match expected scope.")


def validate_no_token_text(value: str) -> None:
    """Reject text that appears to expose a credential."""
    text = str(value)
    unsafe_patterns = [
        r"\bsportmonks_api_token\b",
        r"\bapi_token\b",
        r"\bauthorization\s*:\s*bearer\b",
    ]
    if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in unsafe_patterns):
        raise SportmonksValidationError("Credential-like text is not allowed.")


def validate_safe_input_path(path: Path) -> Path:
    """Validate an explicit local file path without reading its content."""
    candidate = Path(path).expanduser()
    path_text = str(candidate)
    validate_no_token_text(path_text)

    if "://" in path_text:
        raise SportmonksValidationError("Input must be an explicit local file path.")
    if any(part.lower() == ".env" for part in candidate.parts):
        raise SportmonksValidationError("Environment files are not valid input.")
    if re.search(
        r"(^|[\\/._-])(api[_-]?key|token|secret)([\\/._-]|$)",
        path_text,
        flags=re.IGNORECASE,
    ):
        raise SportmonksValidationError("Credential-like input paths are not allowed.")
    if not candidate.exists():
        raise SportmonksValidationError("Input path does not exist.")
    if not candidate.is_file():
        raise SportmonksValidationError("Input path must be a file.")

    return candidate.resolve()
