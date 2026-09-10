# ChipWise — 4:30 demo video script

## 0:00–0:30 — Problem
Show the title and the evidence table.

Narration: “Organ-on-a-chip experiments are information-rich but usually small, expensive, and heterogeneous. The challenge is not only to predict an endpoint. It is to know where the model is uncertain and which experiment should be run next.”

## 0:30–1:05 — Provenance and data honesty
Show `anchor_studies.csv`, then `synthetic_liver_chip.csv`.

Narration: “ChipWise keeps public-study provenance separate from its quantitative demonstration data. The current response dataset is synthetic and reproducible. Study-inspired conditions are anchored to a public human Liver-Chip design, but no synthetic value is presented as a measured biological result.”

## 1:05–1:45 — Standardization
Show schema validation and the four design variables.

Narration: “Every experiment must pass a declared schema: concentration, duration, flow, endotoxin, and a response. This is a small step, but it is foundational if OoC data are to become reusable assets.”

## 1:45–2:35 — Prediction with uncertainty
Open the Streamlit app. Move ethanol from 0.00 to 0.08 to 0.16 while keeping 48 h and 30 microliters per hour.

Narration: “The Gaussian Process model returns both a predicted injury score and uncertainty. The point is not to hide uncertainty behind a single number.”

## 2:35–3:30 — Next experiment recommendation
Scroll to the ranked recommendation table.

Narration: “ChipWise searches untested conditions and prioritizes the ones with highest information value. The recommendation is not a treatment decision. It is a suggestion for the next wet-lab experiment most likely to reduce model uncertainty.”

## 3:30–4:05 — Reproducibility
Show terminal commands and output files.

Narration: “The entire dataset can be regenerated from a fixed seed. Evaluation and recommendations are produced by one-command scripts, with no paid API.”

## 4:05–4:30 — Value and limits
Show the limitations section in the technical report.

Narration: “This is a prototype, not a validated digital twin. The competition-ready idea is the closed loop: standardize experiments, model uncertainty, recommend the next measurement, and improve as real chip data accumulate.”
