import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports" / "generated"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
SAMPLE_DATA_PATH = DATA_DIR / "sample_players.csv"
DATABASE_PATH = DATA_DIR / "football_scout.db"
PLAYERS_TABLE = "players"
EXTERNAL_PROVIDER_URL = os.getenv("EXTERNAL_PROVIDER_URL", "")
EXTERNAL_PROVIDER_NAME = os.getenv("EXTERNAL_PROVIDER_NAME", "generic")
DATA_SOURCE_PRIORITY = ("sqlite", "external", "csv")
MARKET_CONTEXT_ENV_VAR = "FOOTBALL_SCOUT_MARKET_CONTEXT_CSV"
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "")
API_FOOTBALL_BASE_URL = os.getenv("API_FOOTBALL_BASE_URL", "https://v3.football.api-sports.io")
API_FOOTBALL_TIMEOUT_SECONDS = int(os.getenv("API_FOOTBALL_TIMEOUT_SECONDS", "15"))
REPORT_TEMPLATE_PATH = TEMPLATES_DIR / "scouting_report.html"


def get_market_context_csv_path(value: str | Path | None = None) -> Path | None:
    raw_value = os.getenv(MARKET_CONTEXT_ENV_VAR, "") if value is None else str(value)
    if not raw_value or not str(raw_value).strip():
        return None
    path = Path(str(raw_value).strip())
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path

RADAR_METRICS = [
    "goals_per90",
    "assists_per90",
    "xg_per90",
    "xa_per90",
    "key_passes_per90",
    "progressive_passes_per90",
    "progressive_carries_per90",
    "completed_dribbles_per90",
    "duels_won_per90",
    "recoveries_per90",
    "interceptions_per90",
]
