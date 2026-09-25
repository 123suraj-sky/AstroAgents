Perfect. That gives us a much more interesting and concrete project.

## 🔭 #1 Scientific Problem — LOCKED

**Domain:** Astronomical signals / light curves
**Approach:** Open-ended scientific investigation — Option C

### Final problem statement

> **AstroAgents is a multi-agent AI research system that investigates astronomical light-curve data to identify statistically interesting or anomalous signals, analyze their characteristics using computational tools, compare findings against existing scientific knowledge, generate and challenge possible hypotheses, and produce an evidence-backed research report.**

### In simpler terms

A light curve is essentially:

```text
Time ────────────────→

Brightness
   │
   │  • •
   │ •   •
   │•     •
   │       •
   │        • •
   └──────────────────
```

The system looks at how an astronomical object's brightness changes over time.

It might discover something like:

```text
Normal signal
      ↓
Mostly stable brightness

Interesting signal
      ↓
Periodic variation

Anomalous signal
      ↓
Unexpected pattern
```

The agents then investigate **why that signal is interesting**.

---

## What AstroAgents will actually investigate

The system could look for patterns such as:

* Periodic brightness variations
* Transit-like dips
* Sudden brightness changes
* Irregular variability
* Unusual periodicity
* Outliers compared with similar objects
* Potentially interesting signal shapes

The system **doesn't declare a discovery** merely because it finds an anomaly.

Instead:

```text
Interesting signal
       ↓
Statistical validation
       ↓
Signal characterization
       ↓
Literature comparison
       ↓
Possible explanations
       ↓
Critic challenges explanation
       ↓
Additional analysis if necessary
       ↓
Evidence-backed conclusion
```

That's exactly where our multi-agent architecture becomes useful.

---

## Example investigation

A researcher asks:

> **"Find unusual periodic signals in this dataset and investigate their possible causes."**

AstroAgents could do:

```text
Research Manager
       ↓
Data Agent
       ↓
Detect candidate signals
       ↓
Signal Analysis Agent
       ↓
Calculate period / amplitude / significance
       ↓
Literature Agent
       ↓
Search for similar signal patterns
       ↓
Hypothesis Agent
       ↓
Generate possible explanations
       ↓
Critic Agent
       ↓
Challenge explanations
       ↓
Data Agent
       ↓
Perform additional test
       ↓
Evaluation Agent
       ↓
Final Research Report
```

---

## One important principle

We'll keep three things separate:

### Observation

> "The signal has a periodic variation of X days."

### Interpretation

> "This pattern is consistent with a transit-like signal."

### Hypothesis

> "One possible explanation is an orbiting body."

The system must **never silently turn a hypothesis into a fact**.

That distinction will actually become one of our **guardrail and evaluation requirements** later.

---

### Status

**#1 Scientific Problem: ✅ LOCKED**

```text
Project:        AstroAgents
Domain:         Astronomical signals / light curves
Approach:       Open-ended scientific investigation
Primary goal:   Find and investigate interesting/anomalous signals
```

Now we're ready for **#2 — choosing the actual dataset**. This is an important decision because the dataset needs to support both **real scientific analysis and measurable agent evaluation**.
