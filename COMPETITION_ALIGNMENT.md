# Competition alignment

Official challenge page: https://www.aicompetition-pz.com/topic_detail/26

The challenge evaluation weights are:

| Dimension | Weight | ChipWise evidence |
|---|---:|---|
| Technical innovation | 30% | uncertainty-aware small-data model + active next-experiment selection + provenance/data-standardization layer |
| Completion and effectiveness | 25% | runnable CLI + Streamlit demo + deterministic outputs + tests + active-learning benchmark |
| Practical value | 20% | targets expensive sequential OoC experiment planning and reduction of redundant measurements |
| Solution completeness | 15% | problem, data, method, implementation, experiments, results, reproduction, citations, licensing, limitations |
| Interpretability and trustworthiness | 10% | predictive uncertainty, visible acquisition score, explicit synthetic-data labeling, limitations, provenance separation |

## Required submission components

- Public demo video: prepared in `DEMO_VIDEO_SCRIPT.md`; final public video link still needs to be inserted.
- Public code repository: this repository.
- Technical report: `TECHNICAL_REPORT.md` and condensed Kaggle draft.
- Optional runnable demo: Streamlit application in `app.py` (local execution currently guaranteed; public deployment optional).
