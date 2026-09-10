from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.planner import ChipWisePlanner

ROOT = Path(__file__).resolve().parent


def main() -> None:
    df = pd.read_csv(ROOT / "data" / "synthetic_liver_chip.csv")
    planner = ChipWisePlanner().fit(df)
    (ROOT / "outputs").mkdir(exist_ok=True)

    x = np.linspace(0, 0.20, 101)
    query = pd.DataFrame({
        "ethanol_pct": x,
        "exposure_h": 48.0,
        "flow_ul_h": 30.0,
        "endotoxin_ng_ml": 0.0,
    })
    pred = planner.predict(query)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(x, pred.mean, label="GP mean")
    ax.fill_between(
        x,
        np.clip(pred.mean - 1.96 * pred.std, 0, 1),
        np.clip(pred.mean + 1.96 * pred.std, 0, 1),
        alpha=0.2,
        label="95% model interval",
    )
    obs = df[(df.exposure_h == 48) & (df.flow_ul_h == 30) & (df.endotoxin_ng_ml == 0)]
    ax.scatter(obs.ethanol_pct, obs.injury_score, label="Synthetic observations")
    ax.set_xlabel("Ethanol (%)")
    ax.set_ylabel("Synthetic injury score")
    ax.set_title("ChipWise dose-response slice (synthetic demonstration)")
    ax.legend()
    ax.set_ylim(0, 1)
    fig.tight_layout()
    fig.savefig(ROOT / "outputs" / "dose_response.png", dpi=180)
    plt.close(fig)

    ethanol = np.linspace(0, 0.2, 41)
    hours = np.linspace(24, 72, 41)
    grid = pd.DataFrame(
        [(e, h, 30.0, 0.0) for h in hours for e in ethanol],
        columns=["ethanol_pct", "exposure_h", "flow_ul_h", "endotoxin_ng_ml"],
    )
    grid_pred = planner.predict(grid)
    z = grid_pred.std.reshape(len(hours), len(ethanol))
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    image = ax.imshow(
        z,
        origin="lower",
        aspect="auto",
        extent=[ethanol.min(), ethanol.max(), hours.min(), hours.max()],
    )
    fig.colorbar(image, ax=ax, label="Predictive SD")
    ax.set_xlabel("Ethanol (%)")
    ax.set_ylabel("Exposure (h)")
    ax.set_title("Where the model is uncertain (synthetic demonstration)")
    fig.tight_layout()
    fig.savefig(ROOT / "outputs" / "uncertainty_map.png", dpi=180)
    plt.close(fig)
    print("wrote outputs/dose_response.png and outputs/uncertainty_map.png")


if __name__ == "__main__":
    main()
