# ChipWise: Uncertainty-Aware Active Learning for Organ-on-a-Chip Experiments

## Demo video

**Public demo video:** `[FINAL PUBLIC VIDEO URL TO BE INSERTED BEFORE SUBMISSION]`

## Public code repository

https://github.com/farisfd90-ai/chipwise-ai4s

## Project summary

Organ-on-a-chip (OoC) experiments are information-rich but often expensive, low-throughput, and heterogeneous. In this setting, a model that returns only a point prediction can create false confidence. **ChipWise** is an uncertainty-aware experiment-planning prototype that turns completed OoC experiment records into a transparent recommendation for the **next experiment to run**.

The current liver-chip demonstration has four controllable inputs—ethanol concentration, exposure duration, perfusion flow, and endotoxin level. ChipWise validates the experimental schema, fits a Gaussian Process model, reports both predicted response and uncertainty, and ranks untested conditions using an active-learning acquisition score.

The quantitative benchmark is intentionally **synthetic and reproducible**. Public OoC studies are maintained separately as evidence/provenance anchors. No literature measurement is relabeled as a synthetic training observation, and no biological or clinical validation claim is made.

## 1. Problem and motivation

OoC research can generate rich biological readouts from relatively few experiments. The resulting small-data regime creates two practical problems:

1. experimental records need to be standardized before they can be reused; and
2. a researcher needs to know **where the model is uncertain**, not merely what it predicts.

ChipWise targets a closed-loop workflow:

**standardize → model response + uncertainty → select an informative untested condition → run experiment → update model**

This is an experiment-planning problem rather than a treatment-optimization problem.

## 2. Data and provenance

Two data layers are deliberately separated.

### Public evidence catalog

`data/anchor_studies.csv` records public OoC study metadata and NCBI GEO accessions spanning liver, lung, pancreas–liver, and gut–liver systems. These studies ground the use case and metadata design.

### Synthetic quantitative benchmark

`data/synthetic_liver_chip.csv` contains 52 generated liver-chip experiments. The generator is checked into `src/simulate.py` and uses a fixed seed. It includes study-inspired anchor **conditions** corresponding to a public human Liver-Chip alcohol-exposure design, while the quantitative endpoint values remain synthetic.

No patient-level, private, or restricted clinical data are used.

## 3. Method

ChipWise combines:

- strict schema and numerical-bound validation;
- standardized numeric inputs;
- Gaussian Process Regression for mean prediction and predictive standard deviation;
- a bounded candidate experiment grid;
- removal of already-tested conditions;
- uncertainty-guided acquisition with a mild interior-domain preference to avoid repeatedly selecting extreme boundaries;
- a Streamlit interface and reproducible command-line pipeline.

The recommended condition means **“most informative next experiment under the current model and declared design space”**, not “best treatment.”

## 4. Quantitative results

### Held-out synthetic prediction benchmark

Using a fixed 75/25 split of the 52-experiment synthetic dataset (39 train / 13 test):

| Metric | Result |
|---|---:|
| MAE | 0.0267 |
| RMSE | 0.0350 |
| R² | 0.9550 |
| 95% model-interval coverage | 1.0000 |

These values measure recovery of the disclosed synthetic response surface only. They are **not biological validation metrics**.

### Active-learning benchmark

A second experiment tests the actual planning idea over five random seeds. Each simulation starts with 12 experiments and acquires 8 additional conditions.

| Strategy | Start grid RMSE | Final grid RMSE | Reduction |
|---|---:|---:|---:|
| Uncertainty-guided | 0.0501 | 0.0256 | 48.9% |
| Random acquisition | 0.0501 | 0.0342 | 31.9% |

The evaluation target is the known latent function of the **synthetic simulator**, so this result demonstrates acquisition behavior under controlled conditions—not wet-lab efficiency.

## 5. What is innovative here?

ChipWise is intentionally not a generic chatbot. Its contribution is the combination of:

- a provenance-aware OoC experiment schema;
- calibrated small-data modeling with visible uncertainty;
- closed-loop active experiment selection;
- an auditable separation between public evidence and synthetic benchmark values;
- one-command reproducibility and runnable UI.

The design is compatible with future real OoC endpoint data without requiring the current prototype to overclaim a “digital twin.”

## 6. Practical value

With appropriately licensed real experimental measurements, the same workflow could help laboratories:

- reduce redundant experimental runs;
- identify poorly measured regions of a design space;
- prioritize the next informative experiment;
- preserve structured experimental metadata;
- compare uncertainty before committing wet-lab resources;
- build a continuously improving experimental dataset.

## 7. Interpretability and trustworthiness

Trustworthiness is treated as a product feature:

- prediction uncertainty is shown explicitly;
- acquisition scores are visible;
- input bounds are declared;
- data provenance is documented;
- synthetic values are labeled throughout;
- limitations are included in the interface, report, and repository;
- no proprietary API is required at runtime.

## 8. Reproducibility

```bash
python -m pip install -r requirements.txt
python run_all.py
```

Interactive interface:

```bash
streamlit run app.py
```

`run_all.py` regenerates the synthetic dataset, runs held-out evaluation, produces recommendations and figures, executes the active-learning benchmark, and runs the tests.

## 9. Limitations

- Quantitative endpoint labels are synthetic.
- The `injury_score` is a demonstration endpoint, not a validated biomarker.
- Model uncertainty is conditional on the current model and design space.
- No cross-donor, cross-device, cross-lab, sex, genotype, manufacturing-batch, or external-cohort effects are modeled.
- The simulator does not establish biological causality.
- Any real wet-lab recommendation requires domain-expert review and prospective validation.

## 10. Next steps

A scientifically stronger version would ingest licensed real OoC endpoint data, represent donor/lab/device hierarchies, support multimodal readouts, compare alternative acquisition functions, and prospectively test whether active selection reduces experimental cost while preserving scientific value.

## 11. AI assistance disclosure

OpenAI ChatGPT was used for ideation, public-source research, architecture discussion, coding assistance, debugging, testing strategy, documentation drafting, and claim-review. The entrant remains responsible for the submission. The runtime model itself does not call ChatGPT or a proprietary LLM API. Full disclosure is in `AI_ASSISTANCE.md`.
