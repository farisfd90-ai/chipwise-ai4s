from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from src.planner import ChipWisePlanner
from src.schema import TARGET, validate_experiments

ROOT = Path(__file__).resolve().parent


def main() -> None:
    df = pd.read_csv(ROOT / "data" / "synthetic_liver_chip.csv")
    validate_experiments(df)
    train, test = train_test_split(df, test_size=0.25, random_state=42)
    planner = ChipWisePlanner(random_state=42).fit(train)
    pred = planner.predict(test)
    mae = mean_absolute_error(test[TARGET], pred.mean)
    rmse = mean_squared_error(test[TARGET], pred.mean) ** 0.5
    r2 = r2_score(test[TARGET], pred.mean)
    coverage95 = np.mean(
        (test[TARGET].to_numpy() >= pred.mean - 1.96 * pred.std)
        & (test[TARGET].to_numpy() <= pred.mean + 1.96 * pred.std)
    )
    metrics = {
        "n_total": int(len(df)),
        "n_train": int(len(train)),
        "n_test": int(len(test)),
        "mae": round(float(mae), 4),
        "rmse": round(float(rmse), 4),
        "r2": round(float(r2), 4),
        "coverage_95": round(float(coverage95), 4),
        "important_note": "Metrics are on synthetic data and demonstrate software behaviour, not biological validity.",
    }
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
