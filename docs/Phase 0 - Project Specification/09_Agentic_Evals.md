#9 — Agentic Evals

This is where AstroAgents becomes much more interesting as a **portfolio project**.

We don't just want to show:

> "The agents produced a good-looking report."

We want to answer:

> **"How do we know AstroAgents actually performed the investigation correctly?"**

The evaluation system should therefore evaluate **both the scientific result and the agent behavior that produced it**.

---

# 9.1 Evaluation Architecture

I recommend a separate evaluation pipeline:

```text
                 Evaluation Dataset
                        │
                        ↓
                 ┌──────────────┐
                 │  AstroAgents │
                 │   Run        │
                 └──────┬───────┘
                        │
            ┌───────────┼────────────┐
            ↓           ↓            ↓
       Final Result   Trajectory   Tool Calls
            │           │            │
            └───────────┼────────────┘
                        ↓
                Evaluation Pipeline
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
     Scientific      Agentic      Safety /
     Evaluation      Evaluation   Guardrails
          │             │             │
          └─────────────┼─────────────┘
                        ↓
                 Evaluation Report
```

And **the evaluation data must be hidden from the agents**.

---

# 9.2 Two Different Datasets

We already decided in #2 that we'll have:

### Research Dataset

Used by normal AstroAgents investigations.

```text
Kepler light curves
+
metadata
```

### Evaluation Dataset

Used to determine whether AstroAgents is correct.

```text
Known / controlled signals
+
hidden ground truth
```

The agents should never receive the evaluation labels.

For example:

```text
Agent sees:

KIC-123456
light curve
```

but evaluation infrastructure knows:

```text
Ground truth:

signal_type = injected_transit
period = 3.72 days
period_ground_truth = 3.70 days
```

The evaluator compares them **after the run**.

NASA's Kepler DR25 resources include injected light-curve data specifically used for pipeline completeness/reliability studies, which makes controlled evaluation possible without pretending injected signals are real astrophysical discoveries.

---

# 9.3 Evaluation Dimensions

I recommend **8 evaluation dimensions**.

```text id="c8t3av"
1. Task Success
2. Scientific Accuracy
3. Tool Selection
4. Tool Efficiency
5. Evidence / Citation Quality
6. Reasoning / Trajectory Quality
7. Guardrail Compliance
8. Cost / Latency Efficiency
```

Let's define each.

---

# 9.4 Metric 1 — Task Success

The simplest question:

> Did AstroAgents complete the requested investigation correctly?

For a controlled task:

```text
Task:

Identify whether a target contains a
significant periodic signal.
```

Ground truth:

```text
periodic_signal = true
```

Agent result:

```text
periodic_signal = true
```

→ success.

For multiple targets:

```text
precision
recall
F1
```

can be calculated.

---

# 9.5 Metric 2 — Scientific Accuracy

This is where deterministic metrics become extremely useful.

### Period estimation error

If ground truth is:

```text
P = 3.70 days
```

and AstroAgents obtains:

```text
P = 3.72 days
```

we can calculate:

```text
absolute error = |3.72 - 3.70|
               = 0.02 days
```

and:

```text
relative error =
|3.72 - 3.70| / 3.70
```

This is much better than asking an LLM:

> "Was the period accurate?"

---

### Signal classification

For controlled examples:

```text
transit-like
non-transit
anomalous
non-anomalous
```

we can calculate:

```text
precision
recall
F1
confusion matrix
```

---

### Anomaly detection

If ground truth exists:

```text
TP
FP
TN
FN
```

Then:

```text
precision
recall
F1
```

---

# 9.6 Metric 3 — Tool Selection Accuracy

This is one of the metrics that makes the project an **Agentic Eval** project rather than just an ML evaluation project.

Suppose the task is:

> Determine whether a signal is periodic.

The agent chooses:

```text
calculate_periodogram()
```

That may be an appropriate tool.

But if it chooses:

```text
search_scientific_literature()
```

as its first action, that doesn't directly answer the numerical question.

We can define expected tool classes for benchmark tasks.

Example:

```json id="49j0hs"
{
  "task": "periodicity_detection",
  "expected_tools": [
    "load_light_curve",
    "calculate_periodogram"
  ]
}
```

Then measure:

```text
Tool Selection Accuracy
=
appropriate tool decisions
/
tool decisions
```

However, **we should not require one exact trajectory**.

If an agent uses a scientifically valid alternative tool, it should not automatically fail.

So we should distinguish:

```text
required tool
preferred tool
acceptable alternative
irrelevant tool
```

---

# 9.7 Metric 4 — Tool Efficiency

Two agents may both solve the same task:

### Agent A

```text
5 tool calls
```

### Agent B

```text
23 tool calls
```

Both correct.

Agent B may still be less efficient.

Measure:

```text
total tool calls
redundant tool calls
failed tool calls
repeated calls
unnecessary searches
```

Possible metric:

```text
Tool Efficiency =
useful tool calls / total tool calls
```

We can also measure:

```text
average tool calls per successful task
```

---

# 9.8 Metric 5 — Evidence Quality

This evaluates the RAG/Literature component.

Suppose the final report contains:

```text
10 scientific claims
```

and:

```text
8 have valid supporting evidence
```

Then:

```text
Evidence Coverage = 80%
```

But coverage isn't enough.

We also need:

### Citation correctness

Does the cited source actually support the claim?

```text
8 cited claims
6 directly supported
2 partially supported
```

We can report:

```text
Direct Support Rate
Partial Support Rate
Unsupported Claim Rate
```

---

# 9.9 Metric 6 — Scientific Reasoning / Trajectory

This is where an LLM judge can be useful.

But I would **not let an LLM judge everything**.

For example, deterministic checks can answer:

```text
Was period correct?
Was citation valid?
Was tool authorized?
Was evidence present?
```

An LLM judge can assess things like:

```text
Was the reasoning coherent?

Did the agent consider plausible alternatives?

Did the critic identify a meaningful weakness?

Did the final interpretation appropriately reflect uncertainty?
```

---

# 9.10 LLM-as-a-Judge

We can give the judge a structured evaluation prompt.

For example:

```text
Evaluate the scientific reasoning.

Consider:

1. Does the reasoning follow from the evidence?
2. Are alternative explanations considered?
3. Are hypotheses clearly labeled?
4. Are unsupported claims avoided?
5. Does the Critic meaningfully challenge the hypothesis?
```

The judge returns structured scores.

But I recommend **not using a simple 1–10 score** as our main evaluation.

Instead:

```json id="k5g4hl"
{
  "reasoning_coherence": 0.86,
  "alternative_explanation_coverage": 0.72,
  "uncertainty_handling": 0.94
}
```

We'll combine these with deterministic metrics.

---

# 9.11 Metric 7 — Guardrail Compliance

Every guardrail event is already recorded.

So we can measure:

```text
unauthorized tool calls
blocked tool calls
invalid tool parameters
unsupported claims
citation failures
numerical verification failures
maximum-iteration violations
prompt-injection attempts handled
```

For example:

```text
100 tool calls
97 valid
3 blocked
0 unauthorized executions
```

That's a useful system metric.

---

# 9.12 Metric 8 — Cost and Latency

For each research run:

```text
total LLM calls
input tokens
output tokens
tool calls
execution time
tool execution time
LLM latency
retrieval latency
```

Example:

```text
Research Run #1024

LLM calls:             18
Tool calls:            11
Tokens:                24,820
Runtime:               43.2 sec
Literature searches:    3
```

This allows us to compare agentic strategies.

---

# 9.13 Don't Use One Giant Score

I strongly recommend **not doing this**:

```text
Overall Score = 8.7/10
```

That hides too much information.

Instead show:

```text
Task Success          92%
Numerical Accuracy    98%
Tool Selection        87%
Evidence Coverage     91%
Citation Correctness  95%
Guardrail Compliance 100%
Tool Efficiency       78%
```

This makes your evaluation dashboard much more meaningful.

---

# 9.14 Benchmark Task Types

We should create multiple benchmark categories.

### Benchmark A — Signal Detection

```text
Given a light curve,
determine whether a periodic signal exists.
```

Ground truth:

```text
signal_present
```

---

### Benchmark B — Period Estimation

```text
Estimate the dominant period.
```

Ground truth:

```text
known period
```

Metric:

```text
relative period error
```

---

### Benchmark C — Transit-like Detection

```text
Determine whether the signal has
transit-like characteristics.
```

Ground truth:

```text
injected / non-injected
```

Metrics:

```text
precision
recall
F1
```

---

### Benchmark D — Anomaly Detection

```text
Identify unusual light curves.
```

Metrics:

```text
precision
recall
F1
```

---

### Benchmark E — Hypothesis Generation

Give the system:

```text
observations + literature evidence
```

and evaluate whether it produces plausible candidate explanations.

This is where LLM evaluation becomes more useful.

---

### Benchmark F — Critic Effectiveness

This is particularly interesting.

Run:

```text
Without Critic
```

and:

```text
With Critic
```

Then compare:

```text
scientific accuracy
unsupported claim rate
alternative explanation coverage
```

This gives you a direct experiment demonstrating whether the Critic Agent actually adds value.

---

# 9.15 Agent Ablation Studies

This is an excellent portfolio/research feature.

We can run:

```text
System A:
Data Agent only

System B:
Data + Signal

System C:
Data + Signal + Literature

System D:
Data + Signal + Literature + Critic

System E:
Full AstroAgents
```

Then compare their metrics.

Conceptually:

```text
                    Scientific Performance
                           ↑
                           │
                    ┌──────┤
                    │      │
              ┌─────┤      │
              │     │      │
        ┌─────┤     │      │
        │     │     │      │
        └─────┴─────┴──────┴────→
       Basic   +Signal  +Literature +Critic
```

This demonstrates that your multi-agent architecture isn't just complexity for the sake of complexity.

---

# 9.16 Trajectory Evaluation

We should store the entire trajectory:

```text
t0
Research Manager
 ↓
t1
Data Scientist
 ↓
calculate_periodogram()
 ↓
t2
Signal Analyst
 ↓
t3
Literature Agent
 ↓
search_scientific_literature()
 ↓
t4
Hypothesis Agent
 ↓
t5
Critic
 ↓
verify_numerical_result()
 ↓
t6
Data Scientist
 ↓
...
```

Then evaluate:

### Was the trajectory valid?

### Were decisions justified?

### Were there redundant steps?

### Did the agent recover from errors?

### Did the Critic cause meaningful additional analysis?

This is a core **agentic trajectory evaluation**.

---

# 9.17 Hidden Ground Truth

This is critical.

The agents must not see:

```text
ground_truth.json
```

during evaluation.

Architecture:

```text
                 Evaluation Runner
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
       Agent-visible        Evaluator-only
          dataset              labels
             │                   │
             ↓                   ↓
        AstroAgents          Evaluation
             │                   │
             └─────────┬─────────┘
                       ↓
                    Metrics
```

This prevents accidental leakage.

---

# 9.18 Evaluation Dataset Structure

Something like:

```text id="iy7zv5"
evaluation/
│
├── cases/
│   ├── case_001
│   ├── case_002
│   ├── case_003
│   └── ...
│
├── metadata/
│
├── hidden_ground_truth/
│
└── benchmark_config/
```

The agent gets:

```text
case_001/light_curve
case_001/metadata
```

The evaluator additionally knows:

```text
case_001/ground_truth
```

---

# 9.19 Evaluation Run Schema

We can store:

```json id="0avl4p"
{
  "evaluation_run_id": "EVAL-001",
  "benchmark": "period_detection",
  "case_id": "CASE-014",
  "agent_run_id": "RUN-1024",
  "metrics": {
    "period_error": 0.004,
    "tool_selection": 0.91,
    "trajectory_efficiency": 0.82,
    "evidence_coverage": 0.95
  }
}
```

This lets you track performance over time.

---

# 9.20 Evaluation Dashboard

Eventually your UI can show:

```text
┌──────────────────────────────────────────────┐
│ AstroAgents Evaluation                       │
├──────────────────────────────────────────────┤
│                                              │
│ Task Success              92%                │
│ Numerical Accuracy        98%                │
│ Tool Selection            87%                │
│ Evidence Coverage         91%                │
│ Citation Correctness      95%                │
│ Guardrail Compliance     100%                │
│                                              │
├──────────────────────────────────────────────┤
│ Benchmark Performance                         │
│                                              │
│ Period Detection         94%                 │
│ Transit Detection        89%                 │
│ Anomaly Detection        87%                 │
│                                              │
├──────────────────────────────────────────────┤
│ Agent Efficiency                              │
│ Avg. tool calls:         8.4                 │
│ Avg. LLM calls:          12.7                │
│ Avg. runtime:            38.2 sec            │
└──────────────────────────────────────────────┘
```

---

# 9.21 Deterministic vs LLM Evaluation

This is an important architectural decision.

### Use deterministic evaluation for:

```text
✓ Period error
✓ Signal classification
✓ Precision / recall / F1
✓ Numerical correctness
✓ Tool permission
✓ Tool parameters
✓ Citation existence
✓ Evidence references
✓ Runtime
✓ Token usage
✓ Tool-call count
```

### Use LLM-as-a-judge for:

```text
✓ Reasoning coherence
✓ Hypothesis quality
✓ Alternative explanation quality
✓ Critic usefulness
✓ Scientific writing quality
✓ Uncertainty communication
```

### Use human evaluation selectively for:

```text
✓ Final scientific usefulness
✓ Expert-level interpretation
```

That combination is much more defensible than relying entirely on an LLM judge.

---

# 9.22 The "Evaluator Does Not Grade Itself" Problem

You mentioned having an Evaluation Agent.

We should **not let the Evaluation Agent simply read the final report and decide:

> "I think this was 95% correct."

Instead:

```text
                AstroAgents
                    │
                    ↓
              Run artifacts
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
   Deterministic         LLM Judge
   Evaluators             Evaluator
          │                   │
          └─────────┬─────────┘
                    ↓
              Evaluation Engine
                    │
                    ↓
              Final Metrics
```

The Evaluation Agent is therefore **one component of the evaluation framework**, not the sole authority.

This is much stronger.

---

# 9.23 Final Evaluation Architecture

I recommend locking #9 as:

```text
                       Benchmark Case
                            │
                            ↓
                       AstroAgents
                            │
                 ┌──────────┼──────────┐
                 ↓          ↓          ↓
             Scientific  Trajectory  Guardrails
               Output      Trace       Trace
                 │          │          │
                 └──────────┼──────────┘
                            ↓
                  ┌───────────────────┐
                  │ Evaluation Engine │
                  └─────────┬─────────┘
                            │
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
        Deterministic   LLM-as-Judge   System Metrics
          Metrics                         │
             │              │             │
             └──────────────┼─────────────┘
                            ↓
                     Evaluation Report
```

### Core benchmark dimensions

| Dimension             | Primary evaluation    |
| --------------------- | --------------------- |
| Signal detection      | Deterministic         |
| Period estimation     | Deterministic         |
| Anomaly detection     | Deterministic         |
| Tool selection        | Rule/trajectory-based |
| Tool efficiency       | Deterministic         |
| Numerical correctness | Deterministic         |
| Evidence coverage     | Deterministic         |
| Citation correctness  | Evidence verification |
| Reasoning quality     | LLM judge             |
| Hypothesis quality    | LLM judge + evidence  |
| Critic effectiveness  | Ablation + evaluation |
| Guardrail compliance  | Deterministic         |
| Latency/cost          | System telemetry      |

And most importantly:

> **AstroAgents will be evaluated not only on whether it reaches a correct answer, but on whether it reaches that answer through an appropriate, efficient, evidence-backed, and safe trajectory.**

**#9 is now locked.**

Next is **#10 — LLM Observability**. We'll design the complete tracing system: what gets traced, agent spans, LLM calls, tool calls, state transitions, guardrails, evaluation results, token/cost tracking, and what the observability dashboard should actually display.
