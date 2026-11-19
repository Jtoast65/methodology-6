# Seeded faults

The feature's named-date test was committed before its implementation. This was the real failing run against the original feature builder.


```text
F                                                                        [100%]
=================================== FAILURES ===================================
________________ test_yesterdays_temperature_demand_interaction ________________

self = Index(['instant', 'season', 'yr', 'mnth', 'holiday', 'weekday', 'temp',
       'atemp', 'hum', 'windspeed', 'casual', ...kday', 'month_sin', 'month_cos',
       'weather_severity', 'cnt_lag_1', 'cnt_lag_7', 'cnt_roll_7'],
      dtype='str')
key = 'temp_demand_lag_1'

    def get_loc(self, key):
        """
        Get integer location, slice or boolean mask for requested label.
    
        Parameters
        ----------
        key : label
            The key to check its location if it is present in the index.
    
        Returns
        -------
        int if unique index, slice if monotonic index, else mask
            Integer location, slice or boolean mask.
    
        See Also
        --------
        Index.get_slice_bound : Calculate slice bound that corresponds to
            given label.
        Index.get_indexer : Computes indexer and mask for new index given
            the current index.
        Index.get_non_unique : Returns indexer and masks for new index given
            the current index.
        Index.get_indexer_for : Returns an indexer even when non-unique.
    
        Examples
        --------
        >>> unique_index = pd.Index(list("abc"))
        >>> unique_index.get_loc("b")
        1
    
        >>> monotonic_index = pd.Index(list("abbc"))
        >>> monotonic_index.get_loc("b")
        slice(1, 3, None)
    
        >>> non_monotonic_index = pd.Index(list("abcb"))
        >>> non_monotonic_index.get_loc("b")
        array([False,  True, False,  True])
        """
        casted_key = self._maybe_cast_indexer(key)
        try:
>           return self._engine.get_loc(casted_key)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.venv/lib/python3.13/site-packages/pandas/core/indexes/base.py:3641: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
pandas/_libs/index.pyx:168: in pandas._libs.index.IndexEngine.get_loc
    ???
pandas/_libs/index.pyx:197: in pandas._libs.index.IndexEngine.get_loc
    ???
pandas/_libs/hashtable_class_helper.pxi:7668: in pandas._libs.hashtable.PyObjectHashTable.get_item
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

>   ???
E   KeyError: 'temp_demand_lag_1'

pandas/_libs/hashtable_class_helper.pxi:7676: KeyError

The above exception was the direct cause of the following exception:

feats =         dteday  instant  season  ...  cnt_lag_1 cnt_lag_7   cnt_roll_7
0   2011-01-10     10.0  WINTER  ...      822.0...    1787.0  1530.142857
713 2012-12-31    731.0  WINTER  ...     1796.0     920.0  1531.428571

[714 rows x 28 columns]

    def test_yesterdays_temperature_demand_interaction(feats):
        raw = load_raw().set_index("dteday")
        date = pd.Timestamp("2011-06-15")
        yesterday = pd.Timestamp("2011-06-14")
        expected = raw.loc[yesterday, "temp"] * raw.loc[yesterday, TARGET]
>       actual = feats.set_index("dteday").loc[date, "temp_demand_lag_1"]
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/test_leakage.py:79: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.13/site-packages/pandas/core/indexing.py:1199: in __getitem__
    return self.obj._get_value(*key, takeable=self._takeable)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.13/site-packages/pandas/core/frame.py:4489: in _get_value
    series = self._get_item(col)
             ^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.13/site-packages/pandas/core/frame.py:4969: in _get_item
    loc = self.columns.get_loc(item)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = Index(['instant', 'season', 'yr', 'mnth', 'holiday', 'weekday', 'temp',
       'atemp', 'hum', 'windspeed', 'casual', ...kday', 'month_sin', 'month_cos',
       'weather_severity', 'cnt_lag_1', 'cnt_lag_7', 'cnt_roll_7'],
      dtype='str')
key = 'temp_demand_lag_1'

    def get_loc(self, key):
        """
        Get integer location, slice or boolean mask for requested label.
    
        Parameters
        ----------
        key : label
            The key to check its location if it is present in the index.
    
        Returns
        -------
        int if unique index, slice if monotonic index, else mask
            Integer location, slice or boolean mask.
    
        See Also
        --------
        Index.get_slice_bound : Calculate slice bound that corresponds to
            given label.
        Index.get_indexer : Computes indexer and mask for new index given
            the current index.
        Index.get_non_unique : Returns indexer and masks for new index given
            the current index.
        Index.get_indexer_for : Returns an indexer even when non-unique.
    
        Examples
        --------
        >>> unique_index = pd.Index(list("abc"))
        >>> unique_index.get_loc("b")
        1
    
        >>> monotonic_index = pd.Index(list("abbc"))
        >>> monotonic_index.get_loc("b")
        slice(1, 3, None)
    
        >>> non_monotonic_index = pd.Index(list("abcb"))
        >>> non_monotonic_index.get_loc("b")
        array([False,  True, False,  True])
        """
        casted_key = self._maybe_cast_indexer(key)
        try:
            return self._engine.get_loc(casted_key)
        except KeyError as err:
            if isinstance(casted_key, slice) or (
                isinstance(casted_key, abc.Iterable)
                and any(isinstance(x, slice) for x in casted_key)
            ):
                raise InvalidIndexError(key) from err
>           raise KeyError(key) from err
E           KeyError: 'temp_demand_lag_1'

.venv/lib/python3.13/site-packages/pandas/core/indexes/base.py:3648: KeyError
=========================== short test summary info ============================
FAILED tests/test_leakage.py::test_yesterdays_temperature_demand_interaction
1 failed in 1.49s
```

The following controlled demonstrations are executed by Codex. Hook invocations are explicit replays of PostToolUse JSON payloads, labeled accordingly. Each repair restores saved original bytes in one deterministic restoration. These are zero Claude Code repair turns. Live Claude Code repetitions are recorded separately when available.


## 1. Forbidden column in the model inputs

Exact replacement


```text
- return [c for c in numeric if c not in excluded]
+ return [c for c in numeric if c not in excluded] + ["casual"]
```

Real test output, exit 1


```text
F                                                                        [100%]
=================================== FAILURES ===================================
__________________________ test_no_forbidden_features __________________________
tests/test_leakage.py:31: in test_no_forbidden_features
    assert not (cols & FORBIDDEN), f"forbidden columns in feature set: {cols & FORBIDDEN}"
E   AssertionError: forbidden columns in feature set: {'casual'}
E   assert not ({'atemp', 'casual', 'cnt_lag_1', 'cnt_lag_7', 'cnt_roll_7', 'dayofweek', ...} & {'casual', 'cnt', 'cnt_2d_bfr', 'days_since_2011', 'instant', 'registered', ...})
=========================== short test summary info ============================
FAILED tests/test_leakage.py::test_no_forbidden_features - AssertionError: fo...
1 failed in 0.91s
```

PostToolUse payload replay, exit 2. The following is hook stderr.


```text
Leakage tests failed after editing /Users/joeysandoval/Documents/Codex/2026-11-16/https-dsc-capstone-org-2026-27/outputs/bikeshare-open/src/features.py:
feats =         dteday  instant  season  ...  cnt_lag_7   cnt_roll_7 temp_demand_lag_1
0   2011-01-10     10.0  WINTER  ...   ...    5238.818991
713 2012-12-31    731.0  WINTER  ...      920.0  1531.428571       7227.375196

[714 rows x 29 columns]

    def test_no_forbidden_features(feats):
        """Guards the gate, not the data: feature_columns() excludes FORBIDDEN by
        construction, so this cannot discover a *new* leaky column. What it
        catches is someone editing feature_columns() or FORBIDDEN -- which is
        exactly the fault the Step 7 hook demonstrates."""
        cols = set(feature_columns(feats))
>       assert not (cols & FORBIDDEN), f"forbidden columns in feature set: {cols & FORBIDDEN}"
E       AssertionError: forbidden columns in feature set: {'casual'}
E       assert not ({'atemp', 'casual', 'cnt_lag_1', 'cnt_lag_7', 'cnt_roll_7', 'dayofweek', ...} & {'casual', 'cnt', 'cnt_2d_bfr', 'days_since_2011', 'instant', 'registered', ...})

tests/test_leakage.py:31: AssertionError
=========================== short test summary info ============================
FAILED tests/test_leakage.py::test_no_forbidden_features - AssertionError: fo...
1 failed, 9 passed in 0.83s
```

Repaired by restoring the original expression. One restoration, zero Claude turns.


```text
..........                                                               [100%]
10 passed in 0.77s
```


## 2. Rolling mean includes the current target

Exact replacement


```text
- out[TARGET].shift(1).rolling(LAG_WARMUP).mean()
+ out[TARGET].rolling(LAG_WARMUP).mean()
```

Real test output, exit 1


```text
F                                                                        [100%]
=================================== FAILURES ===================================
_______________________ test_rolling_mean_excludes_today _______________________
tests/test_leakage.py:57: in test_rolling_mean_excludes_today
    assert feats.set_index("dteday").cnt_roll_7[date] == pytest.approx(expected)
E   assert np.float64(4389.0) == 4414.857142857143 ± 0.00441486
E     
E     comparison failed
E     Obtained: 4389.0
E     Expected: 4414.857142857143 ± 0.00441486
=========================== short test summary info ============================
FAILED tests/test_leakage.py::test_rolling_mean_excludes_today - assert np.fl...
1 failed in 0.60s
```

PostToolUse payload replay, exit 2. The following is hook stderr.


```text
Leakage tests failed after editing /Users/joeysandoval/Documents/Codex/2026-11-16/https-dsc-capstone-org-2026-27/outputs/bikeshare-open/src/features.py:
[714 rows x 29 columns]

    def test_rolling_mean_excludes_today(feats):
        """cnt_roll_7 must be the mean of the 7 calendar days *before* today."""
        by_date = feats.set_index("dteday")[TARGET]
        date = feats.dteday.iloc[200]
        window = [date - pd.Timedelta(days=k) for k in range(1, 8)]
        if all(d in by_date.index for d in window):
            expected = sum(by_date[d] for d in window) / 7
>           assert feats.set_index("dteday").cnt_roll_7[date] == pytest.approx(expected)
E           assert np.float64(4389.0) == 4414.857142857143 ± 0.00441486
E             
E             comparison failed
E             Obtained: 4389.0
E             Expected: 4414.857142857143 ± 0.00441486

tests/test_leakage.py:57: AssertionError
=========================== short test summary info ============================
FAILED tests/test_leakage.py::test_rolling_mean_excludes_today - assert np.fl...
1 failed, 9 passed in 0.79s
```

Repaired by restoring the original expression. One restoration, zero Claude turns.


```text
..........                                                               [100%]
10 passed in 0.74s
```


## 3. Weather encoder silently accepts an unknown label

Exact replacement


```text
-     if unknown:
        raise ValueError(f"unmapped weather labels: {sorted(unknown)}")

+
```

Real test output, exit 1


```text
F                                                                        [100%]
=================================== FAILURES ===================================
______________________ test_unknown_weather_labels_raise _______________________
tests/test_leakage.py:70: in test_unknown_weather_labels_raise
    with pytest.raises(ValueError, match="unmapped weather labels"):
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   Failed: DID NOT RAISE ValueError
=========================== short test summary info ============================
FAILED tests/test_leakage.py::test_unknown_weather_labels_raise - Failed: DID...
1 failed in 0.59s
```

PostToolUse payload replay, exit 2. The following is hook stderr.


```text
Leakage tests failed after editing /Users/joeysandoval/Documents/Codex/2026-11-16/https-dsc-capstone-org-2026-27/outputs/bikeshare-open/src/features.py:
.......F..                                                               [100%]
=================================== FAILURES ===================================
______________________ test_unknown_weather_labels_raise _______________________

    def test_unknown_weather_labels_raise():
>       with pytest.raises(ValueError, match="unmapped weather labels"):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE ValueError

tests/test_leakage.py:70: Failed
=========================== short test summary info ============================
FAILED tests/test_leakage.py::test_unknown_weather_labels_raise - Failed: DID...
1 failed, 9 passed in 0.78s
```

Repaired by restoring the original expression. One restoration, zero Claude turns.


```text
..........                                                               [100%]
10 passed in 0.82s
```


## 4. Bash copy into raw data

Ran cp from a saved CSV plus one newline into data/raw/bike_daily.csv. The Edit|Write matcher excludes Bash, so Claude would not invoke the hook. An explicit Bash-payload replay also exits 0 with empty stdout/stderr.


```text
cp exit 0
hook replay exit 0
hook stdout/stderr: <empty>
```

The implemented SHA-256 check in load_raw makes make data detect this change. It detects a byte change even though the extra newline would leave parsed values unchanged. The original file is restored immediately after the demonstration.


```text
python -m src.ingest
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/Users/joeysandoval/Documents/Codex/2026-11-16/https-dsc-capstone-org-2026-27/outputs/bikeshare-open/src/ingest.py", line 39, in <module>
    df = load_raw()
  File "/Users/joeysandoval/Documents/Codex/2026-11-16/https-dsc-capstone-org-2026-27/outputs/bikeshare-open/src/ingest.py", line 27, in load_raw
    raise ValueError(f"raw data hash mismatch: {actual_hash}; expected {RAW_SHA256}")
ValueError: raw data hash mismatch: 8b19181406f2d6599f3cb5bd73ce3e81b5883599ca00badcfdb2f7e17c9dded7; expected a6bed1577f6e4de56dcfae6d8315985073cc0ad3446c8c99ed60c86a0b5ad9dc
make: *** [data] Error 1
```

Restored exact original raw bytes and reran the suite.


```text
python -m pytest tests/ -q
..................                                                       [100%]
18 passed in 2.65s
```

## Live /seed-fault repetition

On 2026-11-18, qwen3.5:9b via Claude Code invoked /seed-fault for the weather guard. It removed the guard with Edit. The following blocking-error attachment was captured from the actual Claude Code session 0b999367-1732-473e-8f2d-ec9bb03bf417. This was automatic hook feedback, rather than the payload replays above.

```text
[${CLAUDE_PROJECT_DIR}/.claude/hooks/check_leakage.sh]: Leakage tests failed after editing /Users/joeysandoval/Documents/Codex/2026-11-16/https-dsc-capstone-org-2026-27/outputs/bikeshare-open/src/features.py:
.......F..                                                               [100%]
=================================== FAILURES ===================================
______________________ test_unknown_weather_labels_raise _______________________

    def test_unknown_weather_labels_raise():
>       with pytest.raises(ValueError, match="unmapped weather labels"):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE ValueError

tests/test_leakage.py:70: Failed
=========================== short test summary info ============================
FAILED tests/test_leakage.py::test_unknown_weather_labels_raise - Failed: DID...
1 failed, 9 passed in 1.13s
```

The next repair used one Edit call to restore the exact guard. The subsequent real pytest output was

```text
..........                                                               [100%]
10 passed in 1.03s
```

Repair count was one Claude Code repair edit/turn for the code restoration. The model later made a malformed documentation Edit call missing file_path. Codex stopped that documentation attempt after the source had been restored and transcribed the actual hook attachment here.
