from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

from src.planner import ChipWisePlanner
from src.schema import validate_experiments

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="ChipWise", layout="wide")
st.title("ChipWise — OoC Experiment Planner")
st.caption("Uncertainty-aware prototype. Synthetic quantitative data; public-study metadata for grounding. Not a clinical model.")

df = pd.read_csv(ROOT / "data" / "synthetic_liver_chip.csv")
validate_experiments(df)
planner = ChipWisePlanner().fit(df)

c1, c2, c3, c4 = st.columns(4)
ethanol = c1.slider("Ethanol (%)", 0.0, 0.20, 0.08, 0.01)
hours = c2.slider("Exposure (h)", 24, 72, 48, 12)
flow = c3.slider("Flow (µL/h)", 20, 40, 30, 5)
endotoxin = c4.slider("Endotoxin (ng/mL)", 0.0, 1.0, 0.0, 0.25)

query = pd.DataFrame([{"ethanol_pct":ethanol,"exposure_h":hours,"flow_ul_h":flow,"endotoxin_ng_ml":endotoxin}])
p = planner.predict(query)
st.metric("Predicted injury score", f"{p.mean[0]:.3f}", help="0–1 synthetic demonstration endpoint")
st.metric("Model uncertainty (SD)", f"{p.std[0]:.3f}")

st.subheader("Next informative experiments")
recs = planner.recommend(8)
st.dataframe(recs, use_container_width=True)

st.subheader("Observed synthetic design space")
fig = px.scatter(df, x="ethanol_pct", y="injury_score", size="exposure_h", color="endotoxin_ng_ml", hover_data=["flow_ul_h", "experiment_id"], labels={"ethanol_pct":"Ethanol (%)","injury_score":"Synthetic injury score"})
st.plotly_chart(fig, use_container_width=True)

st.subheader("Evidence anchors")
anchors = pd.read_csv(ROOT / "data" / "anchor_studies.csv")
st.dataframe(anchors[["study_id","organ_system","perturbation","design_summary","data_accession"]], use_container_width=True)
