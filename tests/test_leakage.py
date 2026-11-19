"""The tests that make the agent honest.

test_no_forbidden_features is the single most valuable test in this repo:
casual + registered == cnt exactly, so any model handed those columns
scores R^2 = 1.0 and looks brilliant while having learned nothing.
"""
import pandas as pd
import pytest

from src.config import FORBIDDEN, TARGET
from src.features import build_features, encode_weather, feature_columns
from src.ingest import load_raw


@pytest.fixture(scope="module")
def feats():
    return build_features(load_raw())


def test_leakage_identity_holds(feats):
    """Documents *why* casual and registered are forbidden."""
    assert (feats.casual + feats.registered == feats[TARGET]).all()


def test_no_forbidden_features(feats):
    """Guards the gate, not the data: feature_columns() excludes FORBIDDEN by
    construction, so this cannot discover a *new* leaky column. What it
    catches is someone editing feature_columns() or FORBIDDEN -- which is
    exactly the fault the Step 7 hook demonstrates."""
    cols = set(feature_columns(feats))
    assert not (cols & FORBIDDEN), f"forbidden columns in feature set: {cols & FORBIDDEN}"


def test_lags_are_true_calendar_lags(feats):
    """cnt_lag_1 for date d must equal cnt on d-1, in calendar days."""
    by_date = feats.set_index("dteday")[TARGET]
    checked = 0
    for date, lag in feats.set_index("dteday").cnt_lag_1.items():
        prev = date - pd.Timedelta(days=1)
        if prev in by_date.index:
            assert lag == pytest.approx(by_date[prev]), f"bad lag at {date.date()}"
            checked += 1
    assert checked > 600, "too few rows actually verified"


def test_lag_is_not_the_target(feats):
    assert not (feats.cnt_lag_1 == feats[TARGET]).all()


def test_rolling_mean_excludes_today(feats):
    """cnt_roll_7 must be the mean of the 7 calendar days *before* today."""
    by_date = feats.set_index("dteday")[TARGET]
    date = feats.dteday.iloc[200]
    window = [date - pd.Timedelta(days=k) for k in range(1, 8)]
    if all(d in by_date.index for d in window):
        expected = sum(by_date[d] for d in window) / 7
        assert feats.set_index("dteday").cnt_roll_7[date] == pytest.approx(expected)


def test_no_missing_values(feats):
    assert feats[feature_columns(feats)].isna().sum().sum() == 0


def test_dates_are_sorted_and_unique(feats):
    assert feats.dteday.is_monotonic_increasing
    assert feats.dteday.is_unique


def test_unknown_weather_labels_raise():
    with pytest.raises(ValueError, match="unmapped weather labels"):
        encode_weather(pd.Series(["GOOD", "MISTY", "BAD", "UNSEEN"]))


def test_yesterdays_temperature_demand_interaction(feats):
    raw = load_raw().set_index("dteday")
    date = pd.Timestamp("2011-06-15")
    yesterday = pd.Timestamp("2011-06-14")
    expected = raw.loc[yesterday, "temp"] * raw.loc[yesterday, TARGET]
    actual = feats.set_index("dteday").loc[date, "temp_demand_lag_1"]
    assert actual == pytest.approx(expected)

    # Same-day input changes must not change the feature for that day.
    changed = load_raw()
    changed.loc[changed.dteday == date, ["temp", TARGET]] = 999999
    rebuilt = build_features(changed).set_index("dteday")
    assert rebuilt.loc[date, "temp_demand_lag_1"] == pytest.approx(expected)


def test_model_features_do_not_restate_target(feats):
    """Catch renamed target copies and arithmetic aliases in the model inputs."""
    from itertools import combinations
    import numpy as np

    columns = feature_columns(feats)
    target = feats[TARGET].to_numpy(dtype=float)
    for size in (1, 2, 3):
        for subset in combinations(columns, size):
            matrix = np.column_stack([feats[list(subset)].to_numpy(dtype=float),
                                      np.ones(len(feats))])
            coefficients, *_ = np.linalg.lstsq(matrix, target, rcond=None)
            residual = np.max(np.abs(matrix @ coefficients - target))
            assert residual >= 1e-6, f"target restated by model features: {subset}"
