# ChipWise — Technical Report

## 1. Executive summary

ChipWise is an uncertainty-aware decision-support prototype for organ-on-a-chip (OoC) experimentation. The current demonstration focuses on liver-chip exposure design. It standardizes experiment metadata, learns a response surface from completed experiments, quantifies predictive uncertainty, and recommends the next untested condition that is expected to be informative under the current model.

The objective is **not** to automate biological conclusions or claim a validated digital twin. The objective is to demonstrate a reproducible closed-loop approach for small-data experiment planning:

**standardize → model response + uncertainty → select next experiment → update evidence**

## 2. Problem definition

OoC experiments can vary by organ model, cell source, device, flow conditions, perturbation, concentration, exposure duration, readout, and laboratory protocol. Because sample counts are often small and experiments are expensive, a point prediction alone is not sufficient. A useful experiment-planning system should:

1. enforce consistent experiment records;
2. operate within a declared design space;
3. expose model uncertainty;
4. avoid repeating already-tested conditions;
5. recommend an informative next measurement rather than pretending the model is already certain;
6. preserve data provenance and assumptions.

The target user is an OoC researcher planning sequential experiments.

## 3. Data and provenance

### 3.1 Public evidence catalog

`data/anchor_studies.csv` contains public study metadata and GEO accessions spanning liver, lung, pancreas–liver, and gut–liver OoC/MPS systems. These sources are used as scientific/contextual anchors for the use case and metadata design.

Public-study quantitative measurements are **not copied into the synthetic training dataset**.

### 3.2 Synthetic quantitative dataset

The runnable prototype uses 52 generated liver-chip experiment records with four controllable inputs:

- ethanol concentration (%);
- exposure duration (hours);
- perfusion flow rate (µL/h);
- endotoxin level (ng/mL).

`src/simulate.py` implements the generator. It includes study-inspired anchor **conditions** corresponding to the public GSE175396 human Liver-Chip alcohol-exposure design. Endpoint values remain synthetic.

The latent simulator combines nonlinear contributions from dose, duration, deviation from nominal flow, endotoxin, and a dose/endotoxin interaction. Gaussian noise is added using a fixed seed. Secondary synthetic readouts (`ros_index`, `lipid_index`, `albumin_relative`) are generated for demonstration but the planner target is `injury_score`.

### 3.3 Privacy and ethics

No private patient records, personally identifiable information, or restricted clinical data are used.

## 4. Method

### 4.1 Schema validation

`src/schema.py` defines required fields and numerical bounds. Missing fields, nonnumeric model variables, duplicate experiment identifiers, and out-of-range values fail fast.

### 4.2 Gaussian Process model

`src/planner.py` uses a `StandardScaler` followed by Gaussian Process Regression with a Constant × RBF kernel plus a WhiteKernel noise term. The model returns both:

- posterior mean response estimate; and
- predictive standard deviation.

Gaussian Processes are a useful prototype choice for small structured datasets because uncertainty is directly available and smooth nonlinear relationships can be represented without a large neural model.

### 4.3 Candidate design space

The current candidate grid spans:

- ethanol: 0.00–0.20%;
- exposure: 24, 36, 48, 60, 72 h;
- flow: 20, 25, 30, 35, 40 µL/h;
- endotoxin: 0, 0.25, 0.5, 1.0 ng/mL.

Already-tested feature combinations are removed before ranking.

### 4.4 Acquisition strategy

The acquisition score is primarily predictive standard deviation. A mild interior-domain factor reduces pathological preference for the most extreme ethanol boundaries. The output is interpreted as:

> the most informative next experiment under the current model and declared design bounds.

It is explicitly **not** a treatment recommendation.

## 5. Implementation

Main entry points:

- `app.py` — interactive Streamlit UI;
- `run_all.py` — one-command complete reproducibility pipeline;
- `run_demo.py` — model fit, anchor predictions, next-experiment recommendations;
- `evaluate.py` — held-out synthetic benchmark;
- `benchmark_active_learning.py` — sequential uncertainty-vs-random acquisition benchmark;
- `make_figures.py` — dose-response and uncertainty visualizations;
- `src/simulate.py` — deterministic synthetic data generation.

No paid API is required to run the project.

## 6. Results

### 6.1 Held-out synthetic prediction

Using a fixed 75/25 split of 52 synthetic experiments (39 train / 13 held out), the current reproducible run produced:

| Metric | Result |
|---|---:|
| MAE | 0.0267 |
| RMSE | 0.0350 |
| R² | 0.9550 |
| 95% model-interval coverage | 1.0000 |

These values evaluate recovery of the disclosed synthetic response surface only. They are not evidence of biological, clinical, or wet-lab validity.

### 6.2 Sequential active-learning benchmark

To test the experiment-selection logic itself, a second synthetic benchmark was run across five random seeds. Each run starts with 12 randomly sampled conditions and adds 8 experiments using either uncertainty-guided acquisition or random acquisition.

The metric is RMSE against the known latent simulator response over the full declared candidate grid.

| Strategy | Start RMSE | RMSE after 8 acquisitions | Reduction |
|---|---:|---:|---:|
| Uncertainty-guided | 0.0501 | 0.0256 | 48.9% |
| Random | 0.0501 | 0.0342 | 31.9% |

This experiment demonstrates that the acquisition mechanism can reduce model error faster than random sampling in the controlled synthetic environment. It does **not** establish wet-lab savings.

### 6.3 Generated artifacts

The reproducibility pipeline writes:

- `outputs/metrics.json`;
- `outputs/anchor_predictions.csv`;
- `outputs/next_experiments.csv`;
- `outputs/active_learning_benchmark.csv`;
- `outputs/active_learning_summary.json`;
- `outputs/dose_response.png`;
- `outputs/uncertainty_map.png`;
- `outputs/active_learning_curve.png`.

## 7. Practical relevance to OoC

ChipWise targets three practical bottlenecks:

### Standardization
Comparable records are required before OoC data can become a reusable asset across iterative experiments.

### Small-data uncertainty
OoC experiments can be too costly for large training datasets. Exposing uncertainty is more responsible than presenting an unsupported confident prediction.

### Experiment selection
An active-learning loop can prioritize measurements expected to reduce uncertainty, potentially reducing redundant experimentation once validated with real data.

## 8. Interpretability and trustworthiness

Trustworthiness measures include:

- explicit predictive standard deviation;
- visible acquisition scores;
- declared input bounds;
- provenance catalog separate from synthetic labels;
- fixed-seed generation and reproducibility scripts;
- documented AI assistance;
- documented third-party dependencies and licenses;
- explicit limitations and no clinical claim.

## 9. Reproducibility

Python 3.10+ is recommended.

```bash
python -m pip install -r requirements.txt
python run_all.py
```

For the interactive interface:

```bash
streamlit run app.py
```

The complete pipeline regenerates the quantitative synthetic dataset, evaluates the model, produces recommendations and figures, runs the active-learning benchmark, and executes the test suite.

## 10. Limitations

1. Quantitative endpoint labels are synthetic.
2. `injury_score` is a demonstration endpoint, not a validated biomarker.
3. The model does not establish causality.
4. The acquisition function has only been benchmarked against random acquisition in simulation.
5. The candidate design space is manually bounded.
6. No cross-donor, cross-device, cross-lab, sex, genotype, manufacturing-batch, or external-cohort effects are modeled.
7. Predictive intervals are model-derived and should not be interpreted as guaranteed experimental error bars.
8. Recommendations require scientific review and prospective wet-lab validation.

## 11. Future work

A scientifically stronger implementation would:

- ingest appropriately licensed real OoC endpoint data;
- model donor/lab/device hierarchies;
- support multimodal imaging, omics, and sensor readouts;
- compare uncertainty sampling with expected improvement, information gain, and cost-aware acquisition;
- support constrained experiment feasibility rules;
- evaluate transfer across independent studies and device platforms;
- prospectively measure whether active selection reduces experimental cost.

## 12. AI assistance disclosure

OpenAI ChatGPT assisted with ideation, public-source research, architecture discussion, Python implementation, debugging, testing strategy, documentation drafting, competition-rule interpretation, and scientific-claim review. The runtime planner does not call ChatGPT or any proprietary LLM API. The entrant remains responsible for the submission, licensing, factual interpretation, and compliance.

See `AI_ASSISTANCE.md`, `THIRD_PARTY.md`, and `CITATIONS.md` for additional disclosure and provenance information.
