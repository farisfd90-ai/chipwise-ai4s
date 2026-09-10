from __future__ import annotations

import pandas as pd

FEATURES = ["ethanol_pct", "exposure_h", "flow_ul_h", "endotoxin_ng_ml"]
TARGET = "injury_score"
REQUIRED = ["experiment_id", *FEATURES, TARGET]

BOUNDS = {
    "ethanol_pct": (0.0, 0.20),
    "exposure_h": (12.0, 96.0),
    "flow_ul_h": (10.0, 60.0),
    "endotoxin_ng_ml": (0.0, 2.0),
    "injury_score": (0.0, 1.0),
}


def validate_experiments(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if df["experiment_id"].duplicated().any():
        raise ValueError("experiment_id must be unique")
    for col, (lo, hi) in BOUNDS.items():
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"{col} must be numeric")
        bad = ~df[col].between(lo, hi)
        if bad.any():
            vals = df.loc[bad, col].tolist()[:5]
            raise ValueError(f"{col} outside [{lo}, {hi}]: {vals}")
