# Bikeshare methodology report

## Results

The supplied mirror contains 728 observations spanning 2011-01-03 through 2012-12-31, with 2011-03-10 absent. Restoring the daily calendar before shifting and rolling leaves 714 complete rows. The temporal split contains 348 training rows in 2011, 182 validation rows in H1 2012, and 184 test rows in H2 2012. Models use the starter’s fixed settings and dependency pins. Python 3.13.1 satisfies those pins. `make all` regenerates both committed result files.

The candidate `temp_demand_lag_1` is yesterday’s temperature multiplied by yesterday’s demand. The named-date test for 2011-06-15 computes its expected value from 2011-06-14, and also checks that changing same-day inputs leaves it unchanged. The failing test precedes the implementation in git. “After” includes this single candidate. The final selected pipeline uses “Before” because ridge validation R² declined. All MAEs are measured in rides per day.

| Feature set | Model | Validation R² | Validation MAE | Test R² | Test MAE |
|---|---|---:|---:|---:|---:|
| Before | baseline_mean | -0.9318 | 2002.2 | -2.1441 | 2847.7 |
| Before | baseline_persistence | 0.4507 | 900.6 | 0.5099 | 840.1 |
| Before | ridge | 0.6475 | 832.9 | 0.5833 | 947.1 |
| Before | hgb | 0.2185 | 1296.6 | -0.4975 | 1972.6 |
| After | baseline_mean | -0.9318 | 2002.2 | -2.1441 | 2847.7 |
| After | baseline_persistence | 0.4507 | 900.6 | 0.5099 | 840.1 |
| After | ridge | 0.6041 | 864.5 | 0.3920 | 1169.5 |
| After | hgb | 0.2370 | 1284.5 | -0.4966 | 1982.1 |

The table is generated from `reports/metrics.json`, including its `feature_comparison` entries. The ordinary top-level model entries reproduce the final selected, untransformed pipeline. The complete raw CSV retains SHA-256 `a6bed1577f6e4de56dcfae6d8315985073cc0ad3446c8c99ed60c86a0b5ad9dc`.

## Headline finding

The invalid experiment can achieve R² = 1.000 because casual and registered riders sum exactly to total demand. Excluding those inputs and respecting time order gives final ridge test R² 0.5833 versus persistence 0.5099 and the mean baseline −2.1441. Gradient boosting reaches −0.4975 while still beating the mean baseline. The training target ranges from 431 to 6,043 rides, versus 22 to 8,714 on test; 56.52% of test days exceed the training maximum. Averaging training targets in tree leaves cannot extrapolate beyond that maximum. Ridge can extrapolate through its lag coefficients, though the small training sample and model settings also affect the comparison. These results condition on observed daily weather, as the starter does. Operational advance forecasts require weather forecasts available at issuance time and a new evaluation using those inputs.

The candidate changes ridge validation R² by −0.0434 and tree validation R² by +0.0185. The decision is to reject it for the final ridge model, using the predeclared ridge selection metric and 0.01 improvement threshold. That threshold is a practical reporting rule. It does not establish statistical significance.

## Exercise 4: target transformation

The single transformation experiment fits the same gradient booster to the daily change `cnt − cnt_lag_1`, then adds yesterday’s observed demand back to every prediction. It uses the fixed candidate feature set from the validation experiment. The reconstructed predictions are evaluated in original ride units. Validation R² improves from the candidate tree’s 0.2370 to 0.6329, and MAE falls from 1284.5 to 784.7. This approaches the selected ridge’s validation R² 0.6475 and improves on its MAE 832.9. At the fixed final evaluation, the transformed tree has test R² 0.5619 and MAE 891.2. The code and outputs are `src/train.py --target-change` and `reports/target-transformation.json`; the main metrics remain the untransformed comparison.

This transformation is defensible for a rolling one-day forecast because yesterday’s count is available when predicting today. It removes much of the growing demand level from the tree’s target and restores that level through a known input. It would require recursive prediction or newly observed counts for longer forecast horizons. It also adds an explicit persistence component, so the improvement should be described as a change to the prediction formulation. The feature and transformation choices were fixed from validation before final test scoring. The local agent subsequently ran training despite an instruction restricting its review to validation; this is recorded in DECISIONS.md. Later reruns check reproducibility, and did not change the choices.

## Exercise 5: ridge vs persistence

I favor persistence for a deployment decision led by typical absolute error. On test, ridge improves R² by 0.0734, from 0.5099 to 0.5833, but increases MAE by 107.0 rides per day, from 840.1 to 947.1, a 12.7% increase. On validation, ridge improves both metrics: R² 0.6475 versus 0.4507 and MAE 832.9 versus 900.6. The reversal in test MAE makes a deployment claim based solely on validation or R² unconvincing. Standardized ridge coefficients are largest for the seven-day demand mean (566.945 rides per standard deviation) and yesterday’s demand (361.641), showing substantial reliance on recent demand. Ridge would deserve consideration under an explicit squared-error cost, where its test metric wins. This preference assumes an MAE-led operational loss.

## Attribution

qwen3.5:9b via Ollama, built as bikeshare-coder with 65,536 context tokens, was used throughout the local Claude Code workflows. GPT-6 via Codex additionally implemented and verified this submission. The local model size stayed fixed. The original starter pipeline and its five decision lines come from the course.

Agent work includes the new feature and tests, raw-data checks, comparison and transformation code, controlled fault scripts and captured outputs, the new seed-fault skill, setup corrections, and this report. Codex implemented these components. Local Qwen reviewed the test-first commits through `/new-feature`, ran checks, and wrote an initial decision entry. Codex corrected its date and its unsupported description of the 0.01 threshold as a noise band. Fault evidence distinguishes explicit hook replays from live Claude Code feedback and reports actual repair methods.

Codex proposed the methodological decisions documented in `docs/DECISIONS.md`. Joseph Sandoval reviewed and adopted them on 2026-11-18.

- Predict total daily demand under the starter’s observed-weather assumption, and retain the three categories of excluded columns.
- Use the prescribed temporal split, the mean and persistence baselines, and validation for choosing features.
- Reject the temperature-demand interaction for ridge, and report the negative result.
- Interpret the residual-target transformation as a rolling one-day formulation and evaluate it separately.
- Prefer persistence under an MAE-led deployment cost.

The student reviewed and approved these agent-proposed decisions. The code and initial analysis remain attributed to the agents above. The real Agent SDK self-audit in reports/audit.jsonl reports leakage none, temporal validity true, baselines present, reproducibility true, and an empty findings list with high confidence. Its session called the identity tool on the actual selected features, ran make test, and ran make all. Codex independently verified a fresh checkout and exact metrics equality. The screening audit supports those mechanical checks; operational weather availability and the deployment loss define the scope of the interpretation. The teammate audit in docs/AUDIT.md reviews sfscott-ctrl/DSC180A-Methodology-6 at commit 1a862051ca58c17747bed9f10380861cae725561. The course leakage-auditor returned all five checks passing. Codex independently reproduced both metrics files and verified all 20 tests. The document preserves the verbatim reviewer output and the personal verdict drafted by Codex and reviewed and approved by Joseph Sandoval on 2026-11-18.
