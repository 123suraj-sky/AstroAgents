## #3 — Exact Research Workflow & Agent Responsibilities

For **AstroAgents**, I recommend we make the workflow **agentic rather than a fixed pipeline**. This is important because your project is specifically about multi-agent systems, agentic workflows, tool calling, evaluation, and observability.

LangGraph is a good fit because its graph model supports shared state, conditional routing, parallel execution, and loops. ([GitHub][1])

### 3.1 High-level workflow

```text
                    ┌──────────────────────┐
                    │  Research Question   │
                    │   + Dataset/Targets  │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Research Manager      │
                    │ / Supervisor Agent    │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Data Scientist Agent │
                    │ Clean + Analyze Data │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Signal Analysis      │
                    │ Agent                │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Literature Agent     │
                    │ Search + RAG         │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Hypothesis Agent     │
                    │ Generate Explanations│
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Critic Agent         │
                    │ Challenge Findings   │
                    └──────────┬───────────┘
                               ↓
                       ┌───────┴────────┐
                       │ Evidence       │
                       │ sufficient?    │
                       └───┬────────┬───┘
                           │        │
                         NO│        │YES
                           ↓        ↓
                   More Analysis   Evaluation
                           │        │
                           └──→─────┘
                                    ↓
                           ┌─────────────────┐
                           │ Evaluation Agent│
                           └────────┬────────┘
                                    ↓
                           ┌─────────────────┐
                           │ Research Report │
                           └─────────────────┘
```

The important part is the **NO → More Analysis** loop.

For example:

> Critic: "The periodicity may be caused by an instrumental artifact."

The system shouldn't simply generate a report. It should route the case back to the Data/Signal agent:

```text
Critic
  ↓
Potential artifact detected
  ↓
Data Scientist
  ↓
Run additional quality/statistical tests
  ↓
Signal Analyst
  ↓
Re-evaluate signal
  ↓
Critic
```

That gives you a genuine **agentic loop** rather than:

```text
Agent A → Agent B → Agent C → done
```

---

# 3.2 Agent 1 — Research Manager

### Responsibility

The Research Manager is the **orchestrator/supervisor**.

It receives:

```text
Research Question
Dataset
Available targets/signals
Constraints
```

and decides what the investigation needs.

For example:

> "Investigate unusual periodic signals in this Kepler dataset."

The manager might create:

```text
Task 1:
Identify candidate anomalous signals.

Task 2:
Characterize their periodicity.

Task 3:
Check whether the signals resemble transit-like events.

Task 4:
Search literature for similar phenomena.

Task 5:
Generate possible explanations.

Task 6:
Challenge the explanations.
```

### It should NOT do

The Research Manager shouldn't perform scientific calculations itself.

It delegates.

### Important capability

It should be able to decide:

```text
Data analysis required?        → Data Agent
Signal characterization?      → Signal Agent
Literature evidence required? → Literature Agent
Hypothesis generation?         → Hypothesis Agent
Need additional investigation?→ loop back
```

This is where your **agentic workflow** becomes visible.

---

# 3.3 Agent 2 — Data Scientist Agent

This agent handles the actual data analysis.

### Responsibilities

* Load light curves
* Validate data
* Handle missing values
* Normalize/clean measurements
* Detect problematic observations
* Extract statistical features
* Identify unusual patterns
* Perform anomaly detection
* Calculate statistical properties

For Kepler data, the underlying observations are astronomical brightness measurements over time; MAST provides extracted Kepler light curves and related data products. ([MAST][2])

### Tools

This is one of your main **tool-calling agents**.

For example:

```text
Python Statistics Tool
        ↓
calculate_periodicity(...)
```

or:

```text
Anomaly Detection Tool
        ↓
detect_anomalies(...)
```

or:

```text
Light Curve Tool
        ↓
load_light_curve(KIC)
```

The LLM decides whether it needs the tool.

For example:

```text
LLM:

"I need to determine whether KIC-123456
contains statistically significant periodic variation."

        ↓

Tool call:

run_period_search(
    kic=123456,
    method="LombScargle"
)

        ↓

Tool result:

period = 3.72 days
power = 0.81
false_alarm_probability = 0.003

        ↓

LLM interprets result.
```

This is much stronger for your portfolio than having Python code hidden behind the scenes.

---

# 3.4 Agent 3 — Signal Analysis Agent

This is the **astronomy-specialist agent**.

Its job is to answer:

> "What does this signal look like scientifically?"

It receives the results from the Data Scientist.

For example:

```text
KIC: 123456

Period: 3.72 days
Amplitude: 0.0042
SNR: 11.8
Duration: 4.1 hours
Shape: periodic dip
```

It can classify the pattern as something like:

```text
Periodic variability
Transit-like
Eclipsing-binary-like
Potential artifact
Irregular/anomalous
Unclear
```

Notice that we're deliberately using **"transit-like"**, rather than saying:

> "This is an exoplanet."

That distinction will become an important scientific guardrail.

### Tools

Possible tools:

```text
periodogram()
fold_light_curve()
estimate_transit_parameters()
calculate_snr()
compare_signal_shapes()
```

---

# 3.5 Agent 4 — Literature Agent

This agent connects the investigation to existing scientific knowledge.

### Responsibilities

Given:

```text
Signal characteristics
+
Object metadata
+
Observed phenomenon
```

it searches scientific literature.

For example:

```text
"periodic 3.7 day light curve
transit-like signal
stellar variability"
```

It retrieves relevant papers and extracts:

```text
Paper
Authors
Year
Relevant finding
Evidence
Similarity to current observation
```

Eventually it should produce something like:

```text
Evidence E1:
Paper X reports similar periodic behavior
in objects with characteristic Y.

Evidence E2:
The observed amplitude is within the
reported range.

Evidence E3:
The signal shape differs from the
known phenomenon by ...
```

This agent should **not decide whether the candidate is scientifically valid**. It supplies evidence to the rest of the system.

---

# 3.6 Agent 5 — Hypothesis Agent

This is where the system becomes more research-oriented.

It takes:

```text
Observations
+
Signal characteristics
+
Literature evidence
```

and generates possible explanations.

Example:

```text
Observation:
Periodic brightness decrease every 3.72 days.

Hypothesis H1:
Possible transit-like event.

Hypothesis H2:
Possible eclipsing binary.

Hypothesis H3:
Possible stellar variability.

Hypothesis H4:
Possible instrumental/data-processing artifact.
```

And importantly:

### Every hypothesis gets an evidence state

```text
H1
Status: Hypothesis
Supporting evidence: E1, E2
Contradicting evidence: E5
Confidence: not yet determined
```

The LLM must never turn:

```text
"could be an exoplanet"
```

into:

```text
"this is an exoplanet"
```

without sufficient evidence.

---

# 3.7 Agent 6 — Critic Agent

This is one of the most important agents in the whole project.

Its job is essentially:

> **Try to prove the current interpretation wrong.**

For every hypothesis, it asks:

```text
What evidence supports this?

What evidence contradicts it?

Could this be an artifact?

Could another phenomenon explain it?

Was the statistical test appropriate?

Is the sample size sufficient?

Are the conclusions stronger than the data justify?

Are the cited papers actually relevant?
```

Example:

```text
Hypothesis:
"The signal may represent a transit-like event."

Critic:

Potential issue:
The apparent periodicity could also be explained
by stellar variability.

Required investigation:
Run a secondary periodicity analysis and compare
the folded light-curve morphology.
```

Then:

```text
Critic
   ↓
More evidence required
   ↓
Research Manager
   ↓
Data Scientist
```

This creates your agentic loop.

---

# 3.8 Agent 7 — Evaluation Agent

This agent is slightly different.

It isn't primarily evaluating the astronomy.

It's evaluating **AstroAgents itself**.

For example:

```text
Did the system identify the correct signal?

Did it use the appropriate tool?

Did it calculate the period correctly?

Did it cite supporting evidence?

Did it distinguish observation from hypothesis?

Did the critic catch known issues?

How many unnecessary tool calls occurred?

How many LLM calls were made?

How long did the investigation take?
```

This will feed directly into your **Agentic Evals** component.

---

# 3.9 The final workflow

I would lock the first version of the workflow as:

```text
                     USER
                       │
                       ↓
              Research Manager
                       │
                       ↓
              Data Scientist
                       │
                       ↓
              Signal Analyst
                       │
              ┌────────┴────────┐
              ↓                 ↓
       Literature Agent    Additional Analysis
              │                 ↑
              └───────┬─────────┘
                      ↓
               Hypothesis Agent
                      ↓
                 Critic Agent
                      │
                ┌─────┴─────┐
                │           │
           Insufficient   Sufficient
             evidence       evidence
                │             │
                ↓             ↓
          More Analysis   Evaluation
                │             │
                └──────→──────┘
                              ↓
                       Research Report
```

### One important improvement

I would **not make the Research Manager manually call every agent in a fixed order**.

Instead, its job is to determine the next useful action based on state.

For example:

```text
Signal detected
      ↓
Need literature?
   YES → Literature Agent
      ↓
Need more numerical evidence?
   YES → Data Scientist
      ↓
Need scientific interpretation?
   YES → Signal Agent
      ↓
Generate hypothesis
      ↓
Critic finds problem
      ↓
Back to Data Scientist
```

This is exactly the kind of conditional/looping workflow that graph-based agent frameworks are designed to represent. ([GitHub][3])

---

## The agent responsibilities we'd lock

| Agent                | Main job                           | Tool calling             |
| -------------------- | ---------------------------------- | ------------------------ |
| **Research Manager** | Plan, delegate, route, loop        | Yes                      |
| **Data Scientist**   | Statistical/data analysis          | **Yes — core tool user** |
| **Signal Analyst**   | Astronomical signal interpretation | Yes                      |
| **Literature Agent** | Scientific literature/evidence     | **Yes**                  |
| **Hypothesis Agent** | Generate explanations              | Optional                 |
| **Critic Agent**     | Challenge/falsify findings         | Optional                 |
| **Evaluation Agent** | Evaluate system performance        | Yes                      |

### Most important design decision

I recommend that **Data Scientist + Signal Analyst + Critic** form the core scientific loop:

```text
DATA
 ↓
SIGNAL
 ↓
HYPOTHESIS
 ↓
CRITIC
 ↓
 ├── sufficient → REPORT
 │
 └── insufficient → DATA → SIGNAL → ...
```

That makes AstroAgents much more than a collection of seven LLM personas.

**#3 can now be considered locked with this workflow.**

[1]: https://github.com/langchain-ai/docs/blob/main/src/oss/langchain/multi-agent/custom-workflow.mdx?utm_source=chatgpt.com "docs/src/oss/langchain/multi-agent/custom-workflow.mdx at main · langchain-ai/docs · GitHub"
[2]: https://archive.stsci.edu/missions-and-data/kepler?utm_source=chatgpt.com "KEPLER | MAST"
[3]: https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/graph-api.mdx?utm_source=chatgpt.com "docs/src/oss/langgraph/graph-api.mdx at main · langchain-ai/docs · GitHub"
