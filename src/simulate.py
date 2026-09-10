from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def _latent_injury(ethanol_pct, exposure_h, flow_ul_h, endotoxin_ng_ml):
    dose = ethanol_pct / 0.16
    duration = exposure_h / 48.0
    flow_penalty = ((flow_ul_h - 30.0) / 22.0) ** 2
    second_hit = endotoxin_ng_ml / 1.0
    z = -2.6 + 2.2*dose + 0.9*(duration-1.0) + 0.6*flow_penalty + 1.1*second_hit + 0.7*dose*second_hit
    return 1.0 / (1.0 + np.exp(-z))


def generate(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    # Include study-inspired anchor conditions: vehicle, 0.08%, 0.16% ethanol at 48h / 30 uL h.
    anchor_conditions = [
        (0.00, 48, 30, 0.0, 2),
        (0.08, 48, 30, 0.0, 3),
        (0.16, 48, 30, 0.0, 2),
    ]
    i = 0
    for e, h, f, lps, reps in anchor_conditions:
        for _ in range(reps):
            i += 1
            mu = _latent_injury(e, h, f, lps)
            injury = float(np.clip(mu + rng.normal(0, 0.025), 0, 1))
            rows.append(_row(i, e, h, f, lps, injury, rng, "study-inspired synthetic anchor"))

    # Space-filling synthetic experiments for demonstration of active learning.
    while len(rows) < 52:
        i += 1
        e = float(rng.choice([0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20]))
        h = float(rng.choice([24, 36, 48, 60, 72]))
        f = float(rng.choice([20, 25, 30, 35, 40]))
        lps = float(rng.choice([0.0, 0.25, 0.5, 1.0]))
        mu = _latent_injury(e, h, f, lps)
        injury = float(np.clip(mu + rng.normal(0, 0.035), 0, 1))
        rows.append(_row(i, e, h, f, lps, injury, rng, "fully synthetic"))
    return pd.DataFrame(rows)


def _row(i, e, h, f, lps, injury, rng, provenance):
    ros = float(np.clip(0.35 + 1.8*injury + rng.normal(0, 0.05), 0, 2.5))
    lipid = float(np.clip(0.8 + 1.1*injury + rng.normal(0, 0.04), 0, 2.2))
    albumin = float(np.clip(1.03 - 0.34*injury + rng.normal(0, 0.025), 0.45, 1.2))
    return {
        "experiment_id": f"SYN-{i:03d}",
        "organ": "liver",
        "ethanol_pct": e,
        "exposure_h": h,
        "flow_ul_h": f,
        "endotoxin_ng_ml": lps,
        "ros_index": ros,
        "lipid_index": lipid,
        "albumin_relative": albumin,
        "injury_score": injury,
        "provenance": provenance,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="data/synthetic_liver_chip.csv")
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    df = generate(args.seed)
    df.to_csv(out, index=False)
    print(f"wrote {len(df)} rows to {out}")


if __name__ == "__main__":
    main()
