from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

from src.planner import ChipWisePlanner
from src.schema import FEATURES
from src.simulate import _latent_injury

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def latent_for_frame(df: pd.DataFrame) -> np.ndarray:
    return _latent_injury(
        df["ethanol_pct"].to_numpy(),
        df["exposure_h"].to_numpy(),
        df["flow_ul_h"].to_numpy(),
        df["endotoxin_ng_ml"].to_numpy(),
    )


def make_observation(row: pd.Series, rng: np.random.Generator, idx: int) -> dict:
    y = float(_latent_injury(row.ethanol_pct, row.exposure_h, row.flow_ul_h, row.endotoxin_ng_ml))
    y = float(np.clip(y + rng.normal(0, 0.02), 0, 1))
    return {
        "experiment_id": f"BENCH-{idx:03d}",
        "ethanol_pct": float(row.ethanol_pct),
        "exposure_h": float(row.exposure_h),
        "flow_ul_h": float(row.flow_ul_h),
        "endotoxin_ng_ml": float(row.endotoxin_ng_ml),
        "injury_score": y,
    }


def rmse_on_grid(train: pd.DataFrame, grid: pd.DataFrame, truth: np.ndarray) -> float:
    model = ChipWisePlanner(random_state=42).fit(train)
    pred = model.predict(grid).mean
    return float(mean_squared_error(truth, pred) ** 0.5)


def choose_uncertainty(train: pd.DataFrame, grid: pd.DataFrame) -> pd.Series:
    model = ChipWisePlanner(random_state=42).fit(train)
    tested = set(map(tuple, train[FEATURES].round(6).to_numpy()))
    mask = [tuple(np.round(row, 6)) not in tested for row in grid[FEATURES].to_numpy()]
    pool = grid.loc[mask].reset_index(drop=True)
    pred = model.predict(pool)
    interior = 1.0 - 0.15 * np.abs(pool["ethanol_pct"].to_numpy() - 0.10) / 0.10
    score = pred.std * np.clip(interior, 0.75, 1.0)
    return pool.iloc[int(np.argmax(score))]


def choose_random(train: pd.DataFrame, grid: pd.DataFrame, rng: np.random.Generator) -> pd.Series:
    tested = set(map(tuple, train[FEATURES].round(6).to_numpy()))
    mask = [tuple(np.round(row, 6)) not in tested for row in grid[FEATURES].to_numpy()]
    pool = grid.loc[mask].reset_index(drop=True)
    return pool.iloc[int(rng.integers(0, len(pool)))]


def run(seed: int, strategy: str, n_initial: int = 12, steps: int = 8) -> list[dict]:
    rng = np.random.default_rng(seed)
    grid = ChipWisePlanner().candidate_grid()
    truth = latent_for_frame(grid)
    init_idx = rng.choice(len(grid), size=n_initial, replace=False)
    rows = [make_observation(grid.iloc[i], rng, j + 1) for j, i in enumerate(init_idx)]
    train = pd.DataFrame(rows)
    records = []
    for step in range(steps + 1):
        records.append({
            "seed": seed,
            "strategy": strategy,
            "acquisitions": step,
            "n_experiments": len(train),
            "grid_rmse": rmse_on_grid(train, grid, truth),
        })
        if step == steps:
            break
        if strategy == "uncertainty":
            nxt = choose_uncertainty(train, grid)
        else:
            nxt = choose_random(train, grid, rng)
        train = pd.concat([train, pd.DataFrame([make_observation(nxt, rng, len(train) + 1)])], ignore_index=True)
    return records


def main() -> None:
    records = []
    for seed in [3, 7, 11, 19, 23]:
        for strategy in ["uncertainty", "random"]:
            records.extend(run(seed, strategy))
    df = pd.DataFrame(records)
    df.to_csv(OUT / "active_learning_benchmark.csv", index=False)

    agg = df.groupby(["strategy", "acquisitions"])["grid_rmse"].agg(["mean", "std"]).reset_index()
    start = agg[agg["acquisitions"] == 0].set_index("strategy")["mean"]
    end = agg[agg["acquisitions"] == agg["acquisitions"].max()].set_index("strategy")["mean"]
    summary = {
        "seeds": 5,
        "initial_experiments": 12,
        "acquisition_steps": 8,
        "metric": "RMSE against the known synthetic latent response over the declared candidate grid",
        "uncertainty_start_rmse": round(float(start["uncertainty"]), 4),
        "uncertainty_end_rmse": round(float(end["uncertainty"]), 4),
        "random_start_rmse": round(float(start["random"]), 4),
        "random_end_rmse": round(float(end["random"]), 4),
        "uncertainty_reduction_pct": round(float((start["uncertainty"] - end["uncertainty"]) / start["uncertainty"] * 100), 1),
        "random_reduction_pct": round(float((start["random"] - end["random"]) / start["random"] * 100), 1),
        "important_note": "Synthetic benchmark only; demonstrates acquisition behaviour, not wet-lab efficiency or biological validity."
    }
    (OUT / "active_learning_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    for strategy, part in agg.groupby("strategy"):
        plt.plot(part["n_experiments"] if "n_experiments" in part else part["acquisitions"] + 12, part["mean"], marker="o", label=strategy)
    plt.xlabel("Number of experiments")
    plt.ylabel("Grid RMSE")
    plt.title("Synthetic active-learning benchmark (mean over 5 seeds)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "active_learning_curve.png", dpi=160)
    plt.close()

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
