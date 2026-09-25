#5 — Tool Architecture

This is one of the most important parts of AstroAgents because **tool calling is a core requirement of the project**.

I recommend we design the tools in **5 categories**:

```text
                    AstroAgents Tools
                           │
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
   Data Tools        Scientific Tools    Astronomy Tools
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ↓
                  Literature Tools
                           │
                           ↓
                 Verification Tools
```

The key design rule:

> **The LLM does not directly execute Python, access files, query databases, or call external APIs. It requests a specific tool; the backend validates and executes it.**

---

# 5.1 Category A — Dataset / Data Tools

These tools let agents interact with the AstroAgents dataset.

### `get_dataset_info()`

Returns:

```json
{
  "dataset_id": "kepler_subset_v1",
  "targets": 5000,
  "features": 18,
  "source": "NASA Kepler DR25"
}
```

Used by:

* Research Manager
* Data Scientist

---

### `get_target_metadata(target_id)`

Example:

```text
get_target_metadata("KIC-123456")
```

Returns relevant metadata.

---

### `load_light_curve(target_id)`

Returns a reference to the light-curve data rather than dumping thousands of rows into the LLM context.

```json
{
  "target_id": "KIC-123456",
  "data_reference": "lc://123456",
  "observations": 18543,
  "time_range": "..."
}
```

This is important for both **performance and token efficiency**.

---

### `get_light_curve_summary(target_id)`

Instead of giving the agent the complete data:

```json
{
  "points": 18543,
  "missing_fraction": 0.012,
  "median_flux": 0.9982,
  "std_flux": 0.0041,
  "duration_days": 1450
}
```

This should be one of the most frequently used tools.

---

# 5.2 Category B — Scientific Analysis Tools

This is the heart of your tool-calling demonstration.

## `clean_light_curve()`

```text
clean_light_curve(
    target_id,
    remove_outliers=true,
    handle_missing=true
)
```

Returns a derived dataset reference.

---

## `normalize_light_curve()`

Normalizes flux measurements so different targets can be compared.

---

## `calculate_statistics()`

Returns things such as:

```text
mean
median
standard deviation
MAD
variance
min/max
quantiles
```

---

## `calculate_periodogram()`

This is an important astronomy tool.

```text
calculate_periodogram(
    target_id,
    method="lomb_scargle"
)
```

Astropy provides `LombScargle` specifically for detecting periodic signals in unevenly sampled observations. ([Astropy][1])

The tool could return:

```json
{
  "best_period_days": 3.72,
  "frequency": 0.269,
  "power": 0.81,
  "false_alarm_probability": 0.003
}
```

The LLM should **interpret these numbers**, not calculate them itself.

---

## `run_box_least_squares()`

This is especially useful for our transit-like signal investigation.

```text
run_box_least_squares(
    target_id,
    period_range=[0.5, 50],
    duration_range=[0.05, 0.5]
)
```

Astropy provides `BoxLeastSquares` as a time-series periodogram and its results include quantities such as transit depth, duration, transit time, and depth SNR. ([Astropy][2])

This gives us a nice distinction:

```text
Lomb-Scargle
     ↓
General periodic variability

Box Least Squares
     ↓
Transit-like periodic signals
```

---

# 5.3 Anomaly Detection Tools

## `detect_anomalies()`

Possible implementation:

```text
detect_anomalies(
    target_id,
    method="isolation_forest"
)
```

Later we can support:

```text
Isolation Forest
Local Outlier Factor
Robust statistical thresholds
Autoencoder
```

But for the MVP, I'd keep it simpler.

---

## `extract_signal_features()`

Returns:

```json
{
  "amplitude": 0.0042,
  "duration": 0.17,
  "snr": 11.8,
  "period": 3.72,
  "depth": 0.0031,
  "number_of_events": 27
}
```

This becomes the bridge between the Data Scientist and Signal Analyst.

---

# 5.4 Visualization Tools

These are interesting because the **agent can decide when visualization is useful**.

### `plot_light_curve()`

```text
plot_light_curve(target_id)
```

Returns a visualization reference.

### `plot_periodogram()`

```text
plot_periodogram(target_id)
```

### `plot_folded_light_curve()`

```text
plot_folded_light_curve(
    target_id,
    period=3.72
)
```

This could be particularly useful in the UI.

The agent doesn't need to receive the entire image as textual context. It can say:

```text
"Generate folded light curve to inspect whether
the periodic dips have consistent morphology."
```

Then the tool produces an artifact that appears in the research workspace.

---

# 5.5 Category C — Astronomy / MAST Tools

Since our primary dataset is Kepler, we should have a controlled interface to MAST.

MAST's `astroquery.mast` provides programmatic querying and retrieval of observational data, including Kepler data. ([MAST][3])

## `query_kepler_target()`

```text
query_kepler_target(
    target_id="KIC-123456"
)
```

Returns metadata/data availability.

---

## `retrieve_kepler_light_curve()`

```text
retrieve_kepler_light_curve(
    target_id,
    quarter=None
)
```

The tool retrieves the requested product and stores it in the AstroAgents data layer.

MAST's observation interface supports discovering products and downloading individual or multiple data products programmatically. ([astroquery][4])

### Important

I would **not allow the LLM to specify arbitrary URLs or filesystem paths**.

Instead:

```text
LLM
 ↓
retrieve_kepler_light_curve(KIC=123456)
 ↓
Guardrail
 ↓
MAST adapter
 ↓
download/cache
 ↓
validated dataset reference
```

---

# 5.6 Category D — Literature Tools

These belong primarily to the Literature Agent.

## `search_scientific_literature()`

```text
search_scientific_literature(
    query,
    max_results=10
)
```

---

## `retrieve_paper()`

```text
retrieve_paper(
    paper_id
)
```

---

## `search_knowledge_base()`

For our local RAG system:

```text
search_knowledge_base(
    query,
    top_k=5
)
```

---

## `retrieve_evidence()`

```text
retrieve_evidence(
    document_id,
    chunk_id
)
```

This is important because we eventually want citations to point to **specific evidence**, not simply:

> "According to some paper..."

---

## `verify_citation()`

This can become a powerful guardrail tool.

Input:

```json
{
  "claim": "Periodic variability of this type has been observed...",
  "source_id": "paper_123"
}
```

Output:

```json
{
  "supported": true,
  "support_strength": "direct",
  "evidence": "..."
}
```

---

# 5.7 Category E — Verification Tools

These are particularly valuable for the Critic Agent.

## `verify_numerical_result()`

Example:

```text
verify_numerical_result(
    calculation_id="calc_8392"
)
```

The system independently recomputes the result.

---

## `rerun_analysis()`

The Critic could request:

```text
rerun_analysis(
    analysis_id="analysis_42",
    independent_method=true
)
```

This lets us test whether the original result is robust.

---

## `compare_results()`

```text
compare_results(
    result_a="analysis_42",
    result_b="analysis_51"
)
```

Example:

```text
Original period:     3.72 days
Independent period:  3.71 days
Difference:          0.27%
```

---

# 5.8 Tool Permission Matrix

Now we can make the permissions concrete.

| Tool                   | Manager | Data | Signal | Literature | Hypothesis | Critic | Eval |
| ---------------------- | ------: | ---: | -----: | ---------: | ---------: | -----: | ---: |
| Dataset info           |       ✓ |    ✓ |        |            |            |        |    ✓ |
| Target metadata        |       ✓ |    ✓ |      ✓ |            |            |        |    ✓ |
| Load light curve       |         |    ✓ |        |            |            |      ✓ |    ✓ |
| Clean light curve      |         |    ✓ |        |            |            |      ✓ |      |
| Statistics             |         |    ✓ |        |            |            |      ✓ |    ✓ |
| Lomb-Scargle           |         |    ✓ |      ✓ |            |            |      ✓ |    ✓ |
| BLS                    |         |    ✓ |      ✓ |            |            |      ✓ |    ✓ |
| Anomaly detection      |         |    ✓ |        |            |            |      ✓ |    ✓ |
| Feature extraction     |         |    ✓ |      ✓ |            |            |      ✓ |      |
| Plot light curve       |         |    ✓ |      ✓ |            |            |      ✓ |      |
| MAST query             |       ✓ |    ✓ |      ✓ |            |            |        |      |
| MAST retrieval         |         |    ✓ |        |            |            |        |      |
| Literature search      |         |      |        |          ✓ |            |        |    ✓ |
| Paper retrieval        |         |      |        |          ✓ |            |        |      |
| RAG search             |         |      |      ✓ |          ✓ |          ✓ |      ✓ |    ✓ |
| Citation verification  |         |      |        |          ✓ |            |      ✓ |    ✓ |
| Numerical verification |         |      |        |            |            |      ✓ |    ✓ |
| Independent analysis   |         |      |        |            |            |      ✓ |    ✓ |
| Evaluation             |         |      |        |            |            |        |    ✓ |

This gives us a very clear security boundary.

---

# 5.9 Which Tools Are Actually LLM Tools?

This distinction is important.

We might have 25 backend functions, but **we don't need to expose all 25 directly to the LLM**.

For example:

```text
Backend
│
├── load_light_curve()
├── validate_light_curve()
├── normalize_flux()
├── calculate_statistics()
├── calculate_periodogram()
├── calculate_fap()
└── ...
```

The Data Scientist could see a smaller tool interface:

```text
analyze_light_curve()
```

which internally executes several deterministic functions.

But for demonstrating **tool selection**, I recommend exposing several meaningful tools individually:

```text
load_light_curve
calculate_periodogram
run_box_least_squares
detect_anomalies
extract_signal_features
plot_light_curve
```

Then the agent has to decide:

> "Which tool should I use next?"

That decision itself becomes something we can evaluate.

---

# 5.10 Tool Calling Example

Here's a realistic AstroAgents trajectory.

### User

> Find unusual periodic signals in the selected Kepler targets.

### Research Manager

```text
→ delegate to Data Scientist
```

### Data Scientist

```text
→ load_light_curve(KIC-123456)
```

Result:

```text
18,543 observations
```

Then:

```text
→ calculate_periodogram(KIC-123456)
```

Result:

```text
Best period = 3.72 days
Power = 0.81
```

Agent decides:

> This may contain significant periodic behavior. I should test whether the morphology is transit-like.

Then:

```text
→ run_box_least_squares(KIC-123456)
```

Result:

```text
Period = 3.71 days
Depth = 0.0031
Duration = 0.17 days
Depth SNR = 11.4
```

Signal Analyst receives the results.

Then:

```text
→ query_kepler_target(KIC-123456)
```

Literature Agent:

```text
→ search_scientific_literature(...)
→ retrieve_paper(...)
```

Hypothesis Agent:

```text
H1: transit-like phenomenon
H2: eclipsing binary
H3: stellar variability
H4: instrumental/systematic effect
```

Critic:

```text
→ verify_numerical_result()
→ independent_analysis()
```

Then the Critic might say:

```text
More analysis required.
Potential alternative explanation:
stellar variability.
```

And the workflow loops back.

**This is the kind of trace we want visible in your UI and observability system.**

---

# 5.11 Tool Guardrail Layer

Every tool should pass through the same gateway:

```text
              Agent
                │
                ↓
          Tool Request
                │
                ↓
       ┌─────────────────┐
       │ Tool Guardrail  │
       └────────┬────────┘
                ↓
        Permission Check
                ↓
       Parameter Validation
                ↓
         Resource Limits
                ↓
        Execute Tool
                ↓
        Validate Result
                ↓
         Return Result
```

For example, if an agent attempts:

```text
retrieve_kepler_light_curve(
    target_id="../../etc/passwd"
)
```

the request should never reach the filesystem.

Similarly:

```text
run_analysis(
    frequency_range=[0, infinity]
)
```

should be rejected because it violates resource constraints.

---

# 5.12 MVP Tool Set

I **wouldn't implement all 25 tools initially**.

For the MVP, I'd lock these **12 core tools**:

### Data

1. `get_target_metadata`
2. `load_light_curve`
3. `get_light_curve_summary`

### Scientific

4. `clean_light_curve`
5. `calculate_periodogram`
6. `run_box_least_squares`
7. `detect_anomalies`
8. `extract_signal_features`

### Astronomy

9. `query_kepler_target`

### Literature

10. `search_scientific_literature`
11. `retrieve_evidence`

### Verification

12. `verify_numerical_result`

Then add visualization tools as the UI develops:

```text
plot_light_curve
plot_periodogram
plot_folded_light_curve
```

---

## #5 — Locked Design

So the tool architecture becomes:

```text
                    AstroAgents
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
       Data Tools   Scientific Tools  Astronomy
          │              │              │
          └──────────────┼──────────────┘
                         ↓
                  Literature Tools
                         ↓
                 Verification Tools
                         │
                         ↓
                 Tool Guardrail
                         │
                         ↓
                    Execution
```

And the **12-tool MVP** is:

```text
1.  get_target_metadata
2.  load_light_curve
3.  get_light_curve_summary
4.  clean_light_curve
5.  calculate_periodogram
6.  run_box_least_squares
7.  detect_anomalies
8.  extract_signal_features
9.  query_kepler_target
10. search_scientific_literature
11. retrieve_evidence
12. verify_numerical_result
```

The scientific tools are not arbitrary LLM calculations: they wrap deterministic Python/Astropy code. For example, Astropy supports both Lomb–Scargle and Box Least Squares time-series analysis, which makes them appropriate foundations for the periodic/transit-like investigation. ([Astropy][1]) MAST/Astroquery provides the programmatic layer for retrieving Kepler observations and products. ([astroquery][4])

**#5 is now locked.**

[1]: https://docs.astropy.org/en/latest/timeseries/lombscargle.html?utm_source=chatgpt.com "Lomb-Scargle Periodograms — Astropy v8.1.0.dev630+g08d564fe9"
[2]: https://docs.astropy.org/en/latest/timeseries/ref_api.html?utm_source=chatgpt.com "Reference/API — Astropy v8.1.0.dev639+ge958a8438"
[3]: https://archive.stsci.edu/missions-and-data/kepler?utm_source=chatgpt.com "KEPLER | MAST"
[4]: https://astroquery.readthedocs.io/en/latest/mast/mast_obsquery.html?utm_source=chatgpt.com "Observation Queries — astroquery v0.4.12.dev748+g117fb2231"
