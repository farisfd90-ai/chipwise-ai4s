# ChipWise — Uncertainty-Aware Experiment Planner for Organ-on-a-Chip

ChipWise is a reproducible prototype for the **AI + Organ-on-a-Chip Open Innovation Challenge** in the 5th Pazhou Algorithm Competition. It turns completed Organ-on-a-Chip (OoC) experiment records into an uncertainty-aware recommendation for the **next experiment to run**.

Instead of presenting a single confident prediction, ChipWise closes the loop:

**standardize experiments → model response + uncertainty → rank untested conditions → run the next experiment → update the model**

The current demonstration focuses on liver-chip exposure design. Its quantitative endpoint data are deliberately synthetic and reproducible. Public OoC studies are kept in a separate evidence catalog so the project can demonstrate provenance without misrepresenting literature measurements as training labels.

> **Scope:** research decision-support prototype only. It is not a clinical model, not a validated digital twin, and not a substitute for wet-lab validation or scientific judgment.

## Why this problem matters

OoC studies can be expensive, low-throughput, heterogeneous, and difficult to combine across experiments. In small-data settings, a model that reports only a point estimate can create false confidence. A useful research system should expose what it knows, what it does not know, and which measurement would reduce uncertainty most.

ChipWise therefore emphasizes five properties:

1. **Structured metadata** — invalid or out-of-range records fail fast.
2. **Small-data uncertainty** — Gaussian Process Regression returns a response estimate and predictive uncertainty.
3. **Active experiment selection** — untested conditions are ranked by an uncertainty-based acquisition score.
4. **Provenance separation** — public-study metadata and synthetic quantitative labels are clearly separated.
5. **Reproducibility** — the full synthetic dataset, evaluation, figures, recommendations, benchmark, and tests can be regenerated locally.

## Current results

Held-out evaluation on the fixed-seed synthetic benchmark (52 experiments; 39 train / 13 test):

| Metric | Result |
|---|---:|
| MAE | 0.0267 |
| RMSE | 0.0350 |
| R² | 0.9550 |
| 95% interval coverage | 1.0000 |

These metrics measure recovery of the disclosed synthetic response surface only. They are **not evidence of biological validity**.

A separate five-seed active-learning simulation starts with 12 experiments and acquires 8 more. Mean grid RMSE falls from **0.0501 → 0.0256 (48.9% reduction)** with uncertainty-guided selection, compared with **0.0501 → 0.0342 (31.9% reduction)** for random acquisition. This is also a synthetic benchmark; it demonstrates the acquisition logic, not wet-lab efficiency.

## Quick start

Python 3.10+ is recommended.

```bash
python -m pip install -r requirements.txt
python run_demo.py
python evaluate.py
python -m pytest -q
```

Interactive demo:

```bash
streamlit run app.py
```

## Reproduce everything

```bash
python run_all.py
```

`run_all.py` regenerates the synthetic dataset, evaluates the model, produces recommendation outputs and figures, runs the active-learning benchmark, and executes the test suite.

## Key files

```text
.
├── app.py                         # Streamlit demonstration
├── run_all.py                     # one-command reproducibility entry point
├── run_demo.py                    # recommendations + anchor-condition predictions
├── evaluate.py                    # held-out synthetic evaluation
├── benchmark_active_learning.py   # uncertainty vs random acquisition benchmark
├── make_figures.py                # result figures
├── requirements.txt
├── TECHNICAL_REPORT.md
├── KAGGLE_WRITEUP_DRAFT.md
├── DEMO_VIDEO_SCRIPT.md
├── AI_ASSISTANCE.md
├── CITATIONS.md
├── THIRD_PARTY.md
├── data/
│   ├── anchor_studies.csv         # public-study provenance metadata
│   └── synthetic_liver_chip.csv   # generated quantitative demo data
├── outputs/
│   ├── metrics.json
│   ├── active_learning_summary.json
│   ├── active_learning_benchmark.csv
│   ├── active_learning_curve.png
│   ├── dose_response.png
│   ├── uncertainty_map.png
│   ├── anchor_predictions.csv
│   └── next_experiments.csv
├── src/
│   ├── schema.py
│   ├── simulate.py
│   └── planner.py
└── tests/
    └── test_core.py
```

## Input schema

Core controllable variables in the current liver-chip demo:

| Field | Meaning | Demonstration bounds |
|---|---|---:|
| `ethanol_pct` | ethanol concentration (%) | 0.00–0.20 |
| `exposure_h` | exposure duration (h) | 12–96 validation bounds; candidate grid 24–72 |
| `flow_ul_h` | perfusion flow (µL/h) | 10–60 validation bounds; candidate grid 20–40 |
| `endotoxin_ng_ml` | endotoxin/LPS level (ng/mL) | 0–2 validation bounds; candidate grid 0–1 |
| `injury_score` | synthetic normalized response | 0–1 |

## Public evidence anchors

The project includes public OoC study metadata, including human Liver-Chip alcohol exposure (GSE175396), patient-derived Liver-on-Chips exposed to DILI-related compounds (GSE188541), pancreas–liver microfluidic co-culture (GSE214764), liver MPS NASH modelling (GSE168285), and several lung/gut-liver chip studies.

See [`CITATIONS.md`](CITATIONS.md) and [`data/anchor_studies.csv`](data/anchor_studies.csv). These sources ground the use case and metadata design; their quantitative measurements are **not copied into the synthetic training dataset**.

## Scientific limitations

- Quantitative endpoint labels are synthetic.
- The `injury_score` is a software demonstration endpoint, not a validated biomarker.
- Gaussian Process uncertainty is model uncertainty under the declared design space, not a guarantee of experimental error bounds.
- The simulator is intentionally simple and does not establish causal biology.
- No donor, lab, batch, sex, genotype, device-manufacturing, or cross-platform effects are modeled.
- Recommendations must be reviewed by domain experts before any wet-lab use.

A scientifically stronger next phase would replace or augment synthetic labels with licensed real OoC endpoint data, add donor/lab/device hierarchies, and validate transfer across independent experiments.

## Competition and AI-use transparency

The challenge permits public, literature, simulated, and synthetic data when provenance, assumptions, licensing, and limitations are documented. It also permits AI tools when their use is disclosed. See [`AI_ASSISTANCE.md`](AI_ASSISTANCE.md), [`THIRD_PARTY.md`](THIRD_PARTY.md), and the technical report.

Competition page: https://www.aicompetition-pz.com/topic_detail/26

## License

Project code and original documentation are released under the MIT License. Public datasets, papers, databases, and third-party software retain their own terms and licenses.
