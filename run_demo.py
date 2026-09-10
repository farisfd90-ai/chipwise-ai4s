from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.planner import ChipWisePlanner
from src.schema import validate_experiments

ROOT = Path(__file__).resolve().parent


def main() -> None:
    df = pd.read_csv(ROOT / "data" / "synthetic_liver_chip.csv")
    validate_experiments(df)
    planner = ChipWisePlanner().fit(df)
    recs = planner.recommend(5)
    (ROOT / "outputs").mkdir(exist_ok=True)
    recs.to_csv(ROOT / "outputs" / "next_experiments.csv", index=False)

    anchors = pd.DataFrame([
        {"ethanol_pct": 0.00, "exposure_h": 48.0, "flow_ul_h": 30.0, "endotoxin_ng_ml": 0.0},
        {"ethanol_pct": 0.08, "exposure_h": 48.0, "flow_ul_h": 30.0, "endotoxin_ng_ml": 0.0},
        {"ethanol_pct": 0.16, "exposure_h": 48.0, "flow_ul_h": 30.0, "endotoxin_ng_ml": 0.0},
    ])
    pred = planner.predict(anchors)
    anchors["predicted_injury"] = pred.mean
    anchors["uncertainty_sd"] = pred.std
    anchors.to_csv(ROOT / "outputs" / "anchor_predictions.csv", index=False)

    print("\nAnchor-condition predictions (synthetic model):")
    print(anchors.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nTop next-experiment recommendations:")
    print(recs.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nSaved outputs/anchor_predictions.csv and outputs/next_experiments.csv")


if __name__ == "__main__":
    main()
