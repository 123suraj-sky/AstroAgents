Yes — **we should make that decision now**, because it affects how we design the benchmark and evaluation system.

After checking the current NASA/MAST resources, I think we can **lock #2 without deciding an arbitrary exact number of objects yet**.

### Why

NASA's Kepler archive gives us several complementary products:

* **DR25 light curves** — our primary observational data. ([NASA Exoplanet Archive][1])
* **TCE catalog** — signals identified by Kepler's transit-search pipeline. ([NASA Exoplanet Archive][1])
* **KOI catalog** — vetted planetary candidates and false positives. ([NASA Exoplanet Archive][2])
* **Injected/simulated light curves** — extremely useful for evaluation because the injected signal is known ground truth. NASA specifically describes these as being used to measure detection efficiency and evaluate the pipeline. ([NASA Exoplanet Archive][1])
* **MAST/Astroquery** — lets us retrieve individual Kepler observations programmatically rather than downloading the enormous archive. ([MAST][3])

The full Kepler light-curve collection is close to **3 TB**, so we'll absolutely use a curated subset rather than downloading everything. ([NASA Exoplanet Archive][4])

## 🔒 #2 Dataset — LOCKED

Our data strategy will be:

```text
                    NASA KEPLER
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
    Real Light Curves   KOI/TCE      Simulated
          │             Metadata      Injections
          │                │             │
          └────────────────┼─────────────┘
                           ↓
                  AstroAgents Dataset
                           │
              ┌────────────┴────────────┐
              ↓                         ↓
       Research Dataset          Evaluation Dataset
```

### Research Dataset

**Real Kepler DR25 light curves**

Used by the agents to investigate signals.

### Metadata

We'll associate relevant **KIC/KOI/TCE information** where available.

### Evaluation Dataset

We'll use **known/controlled cases**, including appropriate Kepler simulated/injected data, to test whether the system can detect and characterize signals correctly.

Crucially, the agents won't receive the hidden ground-truth labels during evaluation.

---

### What we are *not* locking yet

We don't need to decide:

> "Exactly 2,000 objects."

right now.

We'll determine the exact number and composition **when we implement the dataset preparation pipeline**, based on:

* signal availability
* computational cost
* class balance
* evaluation requirements
* storage requirements

That is an implementation detail, not a fundamental architecture decision.

So:

**#1 Scientific Problem → ✅ LOCKED**
**#2 Dataset → ✅ LOCKED**

We can now move to **#3: defining the exact research workflow and responsibilities of each agent.**

[1]: https://exoplanetarchive.ipac.caltech.edu/docs/Kepler_Data_Products_Overview.html?utm_source=chatgpt.com "Kepler Data Products Overview"
[2]: https://exoplanetarchive.ipac.caltech.edu/docs/PurposeOfKOITable.html?utm_source=chatgpt.com "Kepler Objects of Interest (KOI) Activity Tables"
[3]: https://archive.stsci.edu/missions-and-data/kepler?utm_source=chatgpt.com "KEPLER | MAST"
[4]: https://exoplanetarchive.ipac.caltech.edu/bulk_data_download/?utm_source=chatgpt.com "Bulk Data Download"
