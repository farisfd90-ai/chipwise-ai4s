from __future__ import annotations

from dataclasses import dataclass
import itertools
import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, RBF, WhiteKernel
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .schema import FEATURES, TARGET, validate_experiments


@dataclass
class Prediction:
    mean: np.ndarray
    std: np.ndarray


class ChipWisePlanner:
    def __init__(self, random_state: int = 42):
        kernel = ConstantKernel(1.0, (0.1, 10.0)) * RBF(length_scale=np.ones(len(FEATURES)), length_scale_bounds=(0.1, 20.0)) + WhiteKernel(noise_level=0.02, noise_level_bounds=(1e-4, 0.2))
        self.model = Pipeline([
            ("scale", StandardScaler()),
            ("gp", GaussianProcessRegressor(kernel=kernel, normalize_y=True, random_state=random_state, n_restarts_optimizer=2)),
        ])
        self._train: pd.DataFrame | None = None

    def fit(self, df: pd.DataFrame) -> "ChipWisePlanner":
        validate_experiments(df)
        self._train = df.copy()
        self.model.fit(df[FEATURES], df[TARGET])
        return self

    def predict(self, df_or_array) -> Prediction:
        if self._train is None:
            raise RuntimeError("fit must be called first")
        if isinstance(df_or_array, pd.DataFrame):
            X = df_or_array[FEATURES]
        else:
            X = df_or_array
        scaler = self.model.named_steps["scale"]
        gp = self.model.named_steps["gp"]
        Xs = scaler.transform(X)
        mean, std = gp.predict(Xs, return_std=True)
        return Prediction(mean=np.clip(mean, 0, 1), std=np.maximum(std, 1e-6))

    def candidate_grid(self) -> pd.DataFrame:
        grids = {
            "ethanol_pct": np.round(np.linspace(0.0, 0.20, 21), 3),
            "exposure_h": [24.0, 36.0, 48.0, 60.0, 72.0],
            "flow_ul_h": [20.0, 25.0, 30.0, 35.0, 40.0],
            "endotoxin_ng_ml": [0.0, 0.25, 0.5, 1.0],
        }
        return pd.DataFrame(list(itertools.product(*grids.values())), columns=grids.keys())

    def recommend(self, n: int = 5) -> pd.DataFrame:
        if self._train is None:
            raise RuntimeError("fit must be called first")
        cand = self.candidate_grid()
        # Avoid exact repeats of already-tested feature combinations.
        tested = set(map(tuple, self._train[FEATURES].round(6).to_numpy()))
        mask = [tuple(np.round(row, 6)) not in tested for row in cand[FEATURES].to_numpy()]
        cand = cand.loc[mask].reset_index(drop=True)
        pred = self.predict(cand)
        # Primary acquisition = epistemic uncertainty. A small interior bonus avoids selecting only domain corners.
        interior = 1.0 - 0.15 * np.abs(cand["ethanol_pct"].to_numpy() - 0.10) / 0.10
        score = pred.std * np.clip(interior, 0.75, 1.0)
        out = cand.copy()
        out["predicted_injury"] = pred.mean
        out["uncertainty_sd"] = pred.std
        out["acquisition_score"] = score
        return out.sort_values(["acquisition_score", "uncertainty_sd"], ascending=False).head(n).reset_index(drop=True)
