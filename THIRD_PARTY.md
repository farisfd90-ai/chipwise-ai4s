# Third-party software and data-use notes

The project uses standard open-source Python libraries through `requirements.txt`. No dependency source code is copied into this repository.

| Package | Purpose | Upstream license (project-level) |
|---|---|---|
| NumPy | numerical arrays / simulation | BSD-3-Clause |
| pandas | tabular data | BSD-3-Clause |
| scikit-learn | Gaussian Process model / metrics | BSD-3-Clause |
| SciPy | scientific Python dependency | BSD-3-Clause |
| Matplotlib | static figures | Matplotlib license (PSF-compatible) |
| Streamlit | interactive demo | Apache-2.0 |
| Plotly | interactive visualization | MIT |
| pytest | tests | MIT |

Users should consult each upstream project for authoritative license text and transitive dependency terms.

## Public scientific sources

The project stores citation/accession metadata and source URLs only. Public-study quantitative measurements are not redistributed as the synthetic training labels. See `CITATIONS.md` and `data/anchor_studies.csv`.

## Project license

Project-authored code and documentation are distributed under the MIT License in `LICENSE`.
