import pandas as pd
from src.simulate import generate
from src.schema import validate_experiments
from src.planner import ChipWisePlanner


def test_generated_data_validates():
    df = generate(42)
    validate_experiments(df)
    assert len(df) == 52


def test_recommendations_are_unseen_and_bounded():
    df = generate(42)
    planner = ChipWisePlanner().fit(df)
    recs = planner.recommend(10)
    assert len(recs) == 10
    assert recs["ethanol_pct"].between(0, 0.20).all()
    assert recs["predicted_injury"].between(0, 1).all()
    tested = set(map(tuple, df[["ethanol_pct","exposure_h","flow_ul_h","endotoxin_ng_ml"]].round(6).to_numpy()))
    assert all(tuple(row) not in tested for row in recs[["ethanol_pct","exposure_h","flow_ul_h","endotoxin_ng_ml"]].round(6).to_numpy())
