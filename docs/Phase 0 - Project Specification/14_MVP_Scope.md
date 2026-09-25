# #14 — MVP Scope

This is the most important item because it determines whether **AstroAgents becomes a focused, working research system or an enormous unfinished platform**.

I recommend making the MVP prove the complete scientific-agentic loop:

> **Question → Plan → Analyze → Interpret → Retrieve Evidence → Generate Hypotheses → Critique → Re-analyze → Report → Evaluate**

That is enough to demonstrate essentially every major capability we designed.

---

## 14.1 MVP objective

The first version should answer a question like:

> **“Investigate this Kepler light curve and determine whether it contains a statistically interesting periodic or transit-like signal, characterize the signal, identify plausible explanations, and produce an evidence-backed research report.”**

The user selects:

```text
Research Question
        +
Kepler Target
        ↓
     AstroAgents
        ↓
Investigation
        ↓
Research Report
```

Don't initially make the system investigate hundreds or thousands of targets autonomously.

Start with **one target per investigation**.

---

# 14.2 MVP agent set

Use **six core agents** initially.

### 1. Research Manager

```text
Plan
Delegate
Route
Loop
Terminate
```

### 2. Data Scientist

```text
Load
Clean
Normalize
Periodogram
BLS
Anomaly detection
Feature extraction
```

### 3. Signal Analyst

```text
Interpret signal
Characterize morphology
Estimate signal properties
Identify uncertainty
```

### 4. Literature Agent

```text
Search literature
Retrieve evidence
Verify citations
```

### 5. Hypothesis Agent

```text
Generate candidate explanations
Connect evidence
Identify required tests
```

### 6. Critic

```text
Challenge hypotheses
Find alternative explanations
Request additional analysis
```

The **Evaluation Agent does not need to participate in the normal investigation**.

It belongs to the evaluation pipeline.

---

# 14.3 MVP workflow

The first complete workflow should be:

```text
                         User
                          │
                          ▼
                  Research Question
                          │
                          ▼
                 Research Manager
                          │
                          ▼
                   Data Scientist
                          │
                  ┌───────┴────────┐
                  ▼                ▼
             Periodogram           BLS
                  │                │
                  └───────┬────────┘
                          ▼
                    Signal Analyst
                          │
                          ▼
                   Literature Agent
                          │
                          ▼
                   Hypothesis Agent
                          │
                          ▼
                       Critic
                          │
                   ┌──────┴──────┐
                   │             │
              More analysis     Done
                   │             │
                   ▼             ▼
             Data Scientist   Report
                   │
                   └──────────────┘
```

This is the **minimum agentic loop** I would want to demonstrate.

---

# 14.4 MVP scientific analysis

Don't implement every possible astronomical analysis technique.

Implement these first:

### A. Light-curve loading

```text
load_light_curve
```

Input:

```json
{
  "target_id": "KIC-..."
}
```

Output:

```json
{
  "time": [...],
  "flux": [...],
  "quality": [...]
}
```

---

### B. Cleaning

```text
clean_light_curve
```

Handle things such as:

* missing values
* invalid observations
* obvious quality flags
* normalization
* basic detrending

---

### C. Periodicity

```text
calculate_periodogram
```

Use Lomb–Scargle.

Return:

```json
{
  "best_period_days": 3.72,
  "power": 0.81,
  "false_alarm_probability": 0.003
}
```

---

### D. Transit-like search

```text
run_box_least_squares
```

Return:

```json
{
  "period_days": 3.71,
  "duration_days": 0.17,
  "depth": 0.0031,
  "snr": 11.4
}
```

---

### E. Anomaly detection

```text
detect_anomalies
```

This doesn't need to be an extremely sophisticated ML system initially.

The goal is to identify unusual portions of the light curve that the agents can investigate.

---

### F. Signal features

```text
extract_signal_features
```

Example:

```text
period
depth
duration
SNR
number_of_events
shape
symmetry
```

---

# 14.5 MVP visualizations

Only build **three essential astronomy plots** initially.

### 1. Raw/cleaned light curve

```text
Flux
 │
 │     ╲      ╱
 │      ╲____╱
 │
 └──────────────── Time
```

### 2. Periodogram

```text
Power
 │
 │          │
 │          │
 │     │    │
 │_____|____|________ Period
```

### 3. Folded light curve

```text
Flux
 │
 │       ╲___╱
 │
 └──────────────── Phase
       0       1
```

These three plots demonstrate the scientific analysis much better than filling the dashboard with dozens of charts.

---

# 14.6 MVP RAG

Keep RAG small.

Don't build a massive scientific knowledge platform.

Start with a curated corpus containing material related to:

```text
Kepler
Transit detection
Box Least Squares
Lomb–Scargle
Eclipsing binaries
Stellar variability
False positives
Kepler pipeline
Light-curve anomalies
```

Pipeline:

```text
Question / Signal
       ↓
Literature Agent
       ↓
Local pgvector
       ↓
Relevant chunks
       ↓
Evidence objects
       ↓
Hypothesis / Critic
```

NASA ADS can be the external literature source when the local corpus isn't sufficient.

---

# 14.7 MVP report

Every successful investigation should produce a structured report.

```text
ASTROAGENTS RESEARCH REPORT

1. Research Question

2. Target
   KIC-XXXXXXXX

3. Dataset
   Kepler DR25

4. Methodology
   - preprocessing
   - periodogram
   - BLS
   - anomaly detection

5. Observed Signals
   - period
   - depth
   - duration
   - SNR

6. Signal Characterization

7. Literature Evidence

8. Candidate Hypotheses
   H1: ...
   H2: ...
   H3: ...

9. Critic Findings

10. Additional Analysis

11. Conclusions

12. Uncertainties & Limitations

13. References
```

The most important part:

### The report must distinguish

```text
OBSERVATION
───────────
Directly measured/computed.

INTERPRETATION
──────────────
Scientific interpretation of the observation.

HYPOTHESIS
──────────
Possible explanation that remains uncertain.
```

This becomes one of AstroAgents' defining characteristics.

---

# 14.8 MVP UI

Build **five pages**.

### 1. Research Workspace

User starts an investigation.

```text
┌──────────────────────────────────────┐
│ New Research Investigation           │
│                                      │
│ Research Question                    │
│ [_______________________________]    │
│                                      │
│ Target                               │
│ [ KIC-123456 ▼ ]                     │
│                                      │
│ [ Start Investigation ]              │
└──────────────────────────────────────┘
```

---

### 2. Live Investigation

This is the centerpiece.

```text
┌───────────────┬───────────────────────┬──────────────┐
│ Agent Trace   │ Scientific Workspace  │ Inspector    │
│               │                       │              │
│ ✓ Manager     │ Light Curve           │ Signal       │
│ ✓ Data        │                       │              │
│ ⟳ Signal      │      📈               │ Period       │
│ ○ Literature  │                       │ SNR          │
│ ○ Hypothesis  │ Periodogram           │ Depth        │
│ ○ Critic      │      📊               │              │
│               │                       │              │
└───────────────┴───────────────────────┴──────────────┘
```

This page should update through WebSockets.

---

### 3. Investigation Details

Show:

* observations
* analyses
* signals
* hypotheses
* critiques
* evidence
* decisions
* provenance

---

### 4. Evaluation

Show:

```text
Task Success
Scientific Accuracy
Period Error
Signal Detection
Tool Selection
Evidence Coverage
Citation Correctness
Guardrail Compliance
Latency
Tool Calls
```

Don't collapse them into one score.

---

### 5. Observability

Show:

```text
RUN-00142

Research Manager
 ├── LLM
 └── decision

Data Scientist
 ├── LLM
 ├── load_light_curve
 └── periodogram

Signal Analyst
 └── LLM

Literature Agent
 ├── retrieval
 └── ADS

Hypothesis Agent
 └── LLM

Critic
 └── verification
```

This makes the agentic architecture visible to someone evaluating the project.

---

# 14.9 MVP evaluation dataset

This is critical.

Don't evaluate only on arbitrary real Kepler targets.

Create a controlled benchmark containing:

```text
Known periodic signals
Known transit-like signals
Known anomalies
Known non-transit signals
Injected transit signals
```

For each case, store evaluator-only ground truth such as:

```json
{
  "target_id": "EVAL-001",
  "expected_period": 3.72,
  "signal_present": true,
  "signal_type": "transit_like"
}
```

Then run:

```text
AstroAgents
     ↓
Prediction
     ↓
Evaluation Engine
     ↓
Ground Truth
     ↓
Metrics
```

This makes your evaluation claims much more meaningful.

---

# 14.10 MVP evaluation metrics

The initial evaluation dashboard should have:

### Scientific

```text
Period MAE
Period RMSE
Signal Precision
Signal Recall
Signal F1
Numerical Accuracy
```

### Agentic

```text
Task Success
Tool Selection Accuracy
Unnecessary Tool Calls
Trajectory Validity
Hypothesis Quality
Critic Effectiveness
```

### Evidence

```text
Citation Validity
Evidence Coverage
Evidence Relevance
```

### System

```text
Runtime
LLM Calls
Tool Calls
Token Usage
Estimated Cost
Guardrail Blocks
```

---

# 14.11 MVP guardrails

Implement these before adding fancy features:

```text
✓ Tool permission validation
✓ Tool parameter validation
✓ Resource/time limits
✓ Tool-result validation
✓ Numerical verification
✓ Observation/interpretation/hypothesis classification
✓ Citation verification
✓ Maximum iteration limit
✓ Duplicate tool-call detection
✓ Final report validation
```

For example:

```text
Critic
  │
  │ "run BLS with period = -100"
  ▼
Tool Guardrail
  │
  ├── INVALID
  │
  ▼
BLOCK
```

That is a much stronger demonstration than merely putting "AI safety" in the README.

---

# 14.12 MVP observability

Every investigation should produce:

```text
research_run_id
agent spans
LLM calls
tool calls
tool arguments
tool results
retrieval events
guardrail events
state transitions
decisions
latency
tokens
cost
errors
```

One run should be reconstructable afterward.

LangGraph itself supports persistent checkpoints for stateful workflows, including recovery and inspection of execution history, so the workflow persistence layer fits naturally with the architecture we've already designed. ([GitHub][1])

---

# 14.13 What we deliberately DON'T build in MVP

This is just as important.

### ❌ Don't build

```text
Multi-user collaboration
```

Not necessary initially.

### ❌ Don't build

```text
Mobile application
```

No value for the portfolio objective.

### ❌ Don't build

```text
Kubernetes
```

Docker Compose is enough.

### ❌ Don't build

```text
Kafka
```

WebSockets + direct service calls are sufficient.

### ❌ Don't build

```text
Microservices
```

Keep the backend modular but as one FastAPI application.

### ❌ Don't build

```text
Custom LLM
```

Use an external model.

### ❌ Don't build

```text
Fine-tuned astronomy LLM
```

Not necessary to demonstrate agentic architecture.

### ❌ Don't build

```text
Massive Kepler archive
```

Use a curated/programmatically retrieved dataset.

### ❌ Don't build

```text
Autonomous discovery of new exoplanets
```

That's scientifically and technically unnecessary for the MVP.

### ❌ Don't build

```text
Dozens of agents
```

Six agents are already enough to demonstrate meaningful multi-agent behavior.

---

# 14.14 MVP → V2 roadmap

After the MVP works end-to-end:

### V1 — Core

```text
One target
   ↓
6 agents
   ↓
Scientific analysis
   ↓
RAG
   ↓
Critic loop
   ↓
Report
   ↓
Evaluation
```

### V2 — Scale

Add:

```text
Multiple targets
Batch investigations
Target ranking
Parallel analysis
More anomaly types
More evaluation cases
```

### V3 — Advanced

Potential additions:

```text
Human-in-the-loop research approval
Experiment planning
Cross-target comparison
Advanced hypothesis testing
More sophisticated scientific models
Collaborative investigations
```

But none of these should delay the first complete working system.

---

# 14.15 The actual MVP definition

I would define **AstroAgents MVP** as:

> **A web-based multi-agent scientific research assistant that takes a Kepler target and research question, uses deterministic astronomical analysis tools to characterize periodic/transit-like signals, retrieves supporting scientific evidence, generates competing hypotheses, subjects them to a critic-driven analysis loop, and produces a provenance-aware research report with separate observations, interpretations, hypotheses, uncertainties, citations, and evaluation metrics.**

And the complete MVP flow is:

```text
                         USER
                           │
                           ▼
                 Research Question
                    + Kepler Target
                           │
                           ▼
                 ┌──────────────────┐
                 │ Research Manager │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Data Scientist   │
                 └────────┬─────────┘
                          │
               ┌──────────┼──────────┐
               ▼          ▼          ▼
          Periodogram     BLS    Anomaly Detection
               │          │          │
               └──────────┼──────────┘
                          ▼
                 ┌──────────────────┐
                 │ Signal Analyst   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Literature Agent │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Hypothesis Agent │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │      Critic      │
                 └────────┬─────────┘
                          │
                   Evidence enough?
                    ┌─────┴─────┐
                   NO          YES
                    │            │
                    ▼            ▼
              More Analysis    Report
                    │
                    └──→ Data Scientist

                          │
                          ▼
                 ┌──────────────────┐
                 │ Evaluation Engine│
                 └──────────────────┘
```

## #14 LOCKED

So the **entire 14-item design is now complete**.

The project is no longer just "an AI astronomy chatbot." It has a defined scientific problem, real data, a dynamic multi-agent workflow, genuine tool calling, deterministic scientific computation, RAG, structured state, scientific guardrails, agentic evaluation, observability, a research-oriented UI, a concrete stack, a maintainable repository structure, and a bounded MVP.

One particularly useful implementation detail is that the LangGraph workflow can use persistent PostgreSQL-backed checkpoints rather than relying only on in-memory execution, which fits the requirement that an investigation be resumable and reconstructable. ([GitHub][1])

**The design phase is now finished. The next phase should be implementation planning: database schema → API contracts → LangGraph state → tool interfaces → first scientific tool → first end-to-end investigation.**

[1]: https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx?utm_source=chatgpt.com "docs/src/oss/langgraph/persistence.mdx at main · langchain-ai/docs · GitHub"
