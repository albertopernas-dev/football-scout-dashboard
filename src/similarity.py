from __future__ import annotations

import numpy as np
import pandas as pd


DEFAULT_SIMILARITY_FEATURES = [
    "goals_per90",
    "assists_per90",
    "xg_per90",
    "xa_per90",
    "shots_per90",
    "key_passes_per90",
    "progressive_passes_per90",
    "progressive_carries_per90",
    "completed_dribbles_per90",
    "duels_won_per90",
    "recoveries_per90",
    "interceptions_per90",
]

POSITION_SIMILARITY_FEATURES = {
    "FW": ["goals_per90", "xg_per90", "shots_per90", "assists_per90", "xa_per90", "completed_dribbles_per90"],
    "ST": ["goals_per90", "xg_per90", "shots_per90", "completed_dribbles_per90"],
    "LW": ["completed_dribbles_per90", "progressive_carries_per90", "xa_per90", "key_passes_per90", "goals_per90"],
    "RW": ["completed_dribbles_per90", "progressive_carries_per90", "xa_per90", "key_passes_per90", "goals_per90"],
    "MF": ["progressive_passes_per90", "key_passes_per90", "xa_per90", "recoveries_per90", "interceptions_per90"],
    "CM": ["progressive_passes_per90", "key_passes_per90", "xa_per90", "recoveries_per90", "interceptions_per90"],
    "DM": ["recoveries_per90", "interceptions_per90", "duels_won_per90", "progressive_passes_per90"],
    "DF": ["duels_won_per90", "recoveries_per90", "interceptions_per90", "progressive_passes_per90"],
    "CB": ["duels_won_per90", "recoveries_per90", "interceptions_per90", "progressive_passes_per90"],
    "FB": ["progressive_passes_per90", "progressive_carries_per90", "duels_won_per90", "interceptions_per90"],
}


def features_for_position(position: str) -> list[str]:
    key = str(position).upper().strip()
    return POSITION_SIMILARITY_FEATURES.get(key, DEFAULT_SIMILARITY_FEATURES)


def _cosine_similarity(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    safe = np.divide(matrix, norms, out=np.zeros_like(matrix, dtype=float), where=norms != 0)
    return safe @ safe.T


def find_similar_players(
    df: pd.DataFrame,
    player_name: str,
    top_n: int = 5,
    features: list[str] | tuple[str, ...] | None = None,
    same_position_only: bool = True,
) -> pd.DataFrame:
    if player_name not in df["player"].values:
        raise ValueError(f"Player not found: {player_name}")

    work = df.copy().reset_index(drop=True)
    target_idx = int(work.index[work["player"] == player_name][0])
    target_position = work.loc[target_idx, "position"] if "position" in work.columns else None
    candidate_features = features or features_for_position(target_position)
    selected_features = [feature for feature in candidate_features if feature in df.columns]
    if not selected_features:
        raise ValueError("No similarity features are available in the dataframe.")
    matrix = work[selected_features].apply(pd.to_numeric, errors="coerce").fillna(0).to_numpy(dtype=float)
    similarities = _cosine_similarity(matrix)[target_idx]

    result = work.copy()
    result["similarity"] = similarities.round(4)
    result = result[result["player"] != player_name]
    if same_position_only and target_position is not None:
        same_position = result[result["position"] == target_position]
        if not same_position.empty:
            result = same_position
    return result.sort_values("similarity", ascending=False).head(top_n).reset_index(drop=True)
