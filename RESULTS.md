# Reproducible results

All results below come from the checked-in synthetic benchmark and are reproduced by the repository scripts. They are software/model-behaviour results, **not biological validation**.

## Held-out prediction benchmark

Dataset: 52 synthetic liver-chip experiments; fixed 75/25 split (39 train / 13 test).

| Metric | Value |
|---|---:|
| MAE | 0.0267 |
| RMSE | 0.0350 |
| R² | 0.9550 |
| 95% model-interval coverage | 1.0000 |

Source: `outputs/metrics.json`, reproduced with `python evaluate.py`.

## Active-learning benchmark

Five random seeds. Each simulation begins with 12 experiments and adds 8 conditions.

| Strategy | Start grid RMSE | Final grid RMSE | Reduction |
|---|---:|---:|---:|
| Uncertainty-guided | 0.0501 | 0.0256 | 48.9% |
| Random acquisition | 0.0501 | 0.0342 | 31.9% |

Source: `outputs/active_learning_summary.json` and `outputs/active_learning_benchmark.csv`, reproduced with `python benchmark_active_learning.py`.

The benchmark compares model error against the known latent response of the disclosed synthetic simulator. It does not estimate wet-lab cost savings.

## Example anchor predictions

At 48 h, 30 µL/h flow, and no endotoxin:

| Ethanol | Predicted synthetic injury | Predictive SD |
|---:|---:|---:|
| 0.00% | 0.0513 | 0.0364 |
| 0.08% | 0.2030 | 0.0351 |
| 0.16% | 0.4373 | 0.0353 |

Source: `outputs/anchor_predictions.csv`.

## Continuous integration

GitHub Actions installs the declared dependencies, runs the tests, reproduces held-out evaluation, and regenerates recommendations on Ubuntu/Python 3.11. The first public CI run completed successfully.
