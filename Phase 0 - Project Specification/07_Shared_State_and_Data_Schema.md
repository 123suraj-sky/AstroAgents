#7 — Shared State & Data Schema

This is the **central data model of AstroAgents**.

The agents should not communicate by passing huge natural-language messages directly to one another. Instead, they should read and update a **structured investigation state**.

Conceptually:

```text
                         Research Run
                              │
                    ┌─────────┴─────────┐
                    │   Shared State    │
                    └─────────┬─────────┘
                              │
        ┌──────────┬──────────┼──────────┬──────────┐
        ↓          ↓          ↓          ↓          ↓
      Data      Signals    Literature Hypotheses  Critic
      Agent      Agent       Agent       Agent     Agent
        │          │          │            │         │
        └──────────┴──────────┴────────────┴─────────┘
                              │
                              ↓
                       Evaluation Agent
```

The important distinction is:

> **Shared state contains structured facts and references, not a transcript of everything every agent said.**

---

# 7.1 What the State Needs to Store

I recommend these major sections:

```text
AstroResearchState
│
├── research
├── dataset
├── targets
├── observations
├── analyses
├── signals
├── literature
├── hypotheses
├── critiques
├── decisions
├── evidence
├── evaluation
├── artifacts
└── execution
```

---

# 7.2 Research Context

This contains the original research request.

```json
{
  "research": {
    "research_id": "RUN-00142",
    "question": "Identify unusual periodic signals in the selected Kepler targets",
    "objective": "Investigate periodic and transit-like signals",
    "status": "running",
    "created_at": "...",
    "current_stage": "signal_analysis"
  }
}
```

The Research Manager primarily controls this section.

---

# 7.3 Dataset State

```json
{
  "dataset": {
    "dataset_id": "kepler_subset_v1",
    "source": "NASA Kepler",
    "version": "v1",
    "target_count": 5000,
    "evaluation_dataset": false
  }
}
```

We should also distinguish:

```text
research dataset
```

from:

```text
evaluation dataset
```

because we don't want agents accidentally accessing hidden ground truth during evaluation.

---

# 7.4 Target State

A research run may investigate multiple targets.

```json
{
  "targets": [
    {
      "target_id": "KIC-123456",
      "status": "under_investigation",
      "priority": "high"
    },
    {
      "target_id": "KIC-789012",
      "status": "pending",
      "priority": "medium"
    }
  ]
}
```

This allows the Research Manager to prioritize targets.

---

# 7.5 Observations

This is one of the **most important schemas**.

An observation should represent something directly obtained from the data.

```json
{
  "observation_id": "OBS-001",
  "target_id": "KIC-123456",
  "type": "periodic_signal",
  "statement": "The light curve contains a recurring flux decrease.",
  "source": "calculate_periodogram",
  "analysis_id": "AN-001",
  "status": "verified"
}
```

Notice:

```text
"The light curve contains a recurring flux decrease."
```

is an observation.

Whereas:

```text
"This is an exoplanet."
```

is **not** an observation.

This schema will help enforce the scientific distinction we established earlier.

---

# 7.6 Analysis Results

Every scientific computation gets its own record.

Example:

```json
{
  "analysis_id": "AN-001",
  "target_id": "KIC-123456",
  "tool": "calculate_periodogram",
  "method": "lomb_scargle",
  "parameters": {
    "frequency_range": [0.01, 5.0]
  },
  "result": {
    "period_days": 3.72,
    "power": 0.81,
    "false_alarm_probability": 0.003
  },
  "status": "verified"
}
```

This is extremely useful.

Instead of an agent saying:

> "The period seems to be around 3.7 days."

we have:

```text
AN-001
period_days = 3.72
method = Lomb-Scargle
tool = calculate_periodogram
```

That makes the result auditable.

---

# 7.7 Signal State

The Signal Analyst converts raw analysis into structured signal characteristics.

```json
{
  "signal_id": "SIG-001",
  "target_id": "KIC-123456",
  "classification": "transit_like",
  "period_days": 3.71,
  "depth": 0.0031,
  "duration_days": 0.17,
  "snr": 11.4,
  "morphology": "repeating_dip",
  "confidence": null
}
```

I deliberately recommend **not storing an LLM-generated confidence score initially**.

We'll decide how confidence should be calculated later.

---

# 7.8 Evidence State

This connects RAG to the rest of the system.

```json
{
  "evidence": [
    {
      "evidence_id": "E-001",
      "source_type": "scientific_paper",
      "paper_id": "P-001",
      "section": "Results",
      "text_reference": "chunk://P-001/17",
      "supports": ["H-001"],
      "status": "verified"
    }
  ]
}
```

Now we have:

```text
Hypothesis
   ↓
Evidence
   ↓
Paper
   ↓
Exact chunk
```

This is the provenance chain we designed in #6.

---

# 7.9 Literature State

Keep paper metadata separate from evidence.

```json
{
  "literature": [
    {
      "paper_id": "P-001",
      "title": "...",
      "authors": ["..."],
      "year": 2022,
      "source": "NASA ADS",
      "identifier": "...",
      "relevance_score": 0.91
    }
  ]
}
```

Why separate them?

One paper can produce multiple evidence objects:

```text
P-001
 ├── E-001
 ├── E-002
 └── E-003
```

---

# 7.10 Hypothesis State

This is where we explicitly enforce the scientific distinction.

```json
{
  "hypotheses": [
    {
      "hypothesis_id": "H-001",
      "statement": "The periodic signal may be caused by a transit-like event.",
      "status": "proposed",
      "supporting_evidence": [
        "E-001",
        "E-004"
      ],
      "contradicting_evidence": [
        "E-007"
      ],
      "required_tests": [
        "Independent signal validation"
      ]
    }
  ]
}
```

Possible statuses:

```text
proposed
under_review
supported
weakened
rejected
inconclusive
```

Importantly, **supported ≠ proven**.

---

# 7.11 Critic State

The Critic Agent needs its own structured state.

```json
{
  "critiques": [
    {
      "critique_id": "CR-001",
      "hypothesis_id": "H-001",
      "severity": "medium",
      "issue_type": "alternative_explanation",
      "description": "Stellar variability may produce a similar periodic pattern.",
      "required_action": {
        "agent": "data_scientist",
        "task": "Perform additional variability analysis"
      },
      "status": "open"
    }
  ]
}
```

Possible issue types:

```text
alternative_explanation
data_quality
statistical_uncertainty
insufficient_evidence
citation_problem
calculation_error
unsupported_claim
```

---

# 7.12 Decision State

This is where the Research Manager records **why the workflow moved somewhere**.

Example:

```json
{
  "decision_id": "D-012",
  "agent": "research_manager",
  "decision": "run_additional_analysis",
  "reason": "Critic identified a plausible alternative explanation.",
  "next_agent": "data_scientist",
  "related_critique": "CR-001"
}
```

This is extremely valuable for observability.

Later your UI can show:

> **Why did the system run this analysis?**

Answer:

> Because Critic CR-001 identified a potential alternative explanation.

---

# 7.13 Artifact State

Scientific analysis will generate artifacts:

```text
light curve plots
periodograms
folded light curves
CSV outputs
analysis reports
```

Don't put the actual files inside the graph state.

Store references:

```json
{
  "artifacts": [
    {
      "artifact_id": "ART-001",
      "type": "plot",
      "name": "KIC-123456_periodogram.png",
      "storage_reference": "..."
    }
  ]
}
```

This keeps the agent state lightweight.

---

# 7.14 Execution State

This is for agentic workflow information.

```json
{
  "execution": {
    "current_agent": "critic",
    "iteration": 4,
    "max_iterations": 12,
    "tool_calls": 17,
    "started_at": "...",
    "last_updated": "...",
    "status": "running"
  }
}
```

This will later feed directly into **observability and evaluation**.

---

# 7.15 Evaluation State

Keep evaluation results separate from scientific findings.

```json
{
  "evaluation": {
    "status": "pending",
    "task_success": null,
    "numerical_accuracy": null,
    "tool_selection": null,
    "evidence_coverage": null,
    "citation_correctness": null,
    "trajectory_efficiency": null,
    "guardrail_compliance": null
  }
}
```

This prevents the agents from accidentally treating evaluation metrics as scientific evidence.

---

# 7.16 The Complete State

Putting everything together:

```python
class AstroResearchState:
    research: ResearchState
    dataset: DatasetState
    targets: list[TargetState]

    observations: list[Observation]
    analyses: list[AnalysisResult]
    signals: list[Signal]

    literature: list[Paper]
    evidence: list[Evidence]

    hypotheses: list[Hypothesis]
    critiques: list[Critique]

    decisions: list[Decision]
    artifacts: list[Artifact]

    evaluation: EvaluationState
    execution: ExecutionState
```

We can implement this using typed schemas such as **Pydantic models**.

---

# 7.17 State vs Database

An important architecture decision:

### LangGraph state

Contains the **current working context** needed by agents.

### PostgreSQL

Contains the **persistent research record**.

So:

```text
                    Agent Workflow
                         │
                    LangGraph State
                         │
                  ┌──────┴──────┐
                  ↓             ↓
              Agents        Checkpoints
                                │
                                ↓
                          PostgreSQL
                                │
             ┌──────────────────┼──────────────────┐
             ↓                  ↓                  ↓
        Research Runs      Scientific Data      Evidence
```

We should **not treat LangGraph state as our permanent database**.

---

# 7.18 Why This Matters for Your Project

This design gives us several strong features later.

### Agentic Evals

We can reconstruct:

```text
What did the agent know?
What did it decide?
What tool did it call?
What result did it receive?
Why did it continue?
```

### Observability

We can trace:

```text
State
 ↓
Decision
 ↓
Tool
 ↓
Result
 ↓
State update
```

### Guardrails

We can validate state transitions:

```text
Hypothesis cannot become "supported"
unless required evidence exists.
```

### UI

The frontend can simply consume structured state:

```text
Research
├── Findings
├── Signals
├── Evidence
├── Hypotheses
├── Critiques
├── Visualizations
└── Agent Trace
```

---

# 7.19 One Important Rule: Immutable Raw Data

I recommend one strict rule:

> **Agents may never modify the original astronomical observations.**

Instead:

```text
Raw Light Curve
      │
      ↓
Derived Dataset
      │
      ↓
Analysis
      │
      ↓
Finding
```

For example:

```text
raw_light_curve
       ↓
cleaned_light_curve
       ↓
normalized_light_curve
       ↓
periodogram
       ↓
signal_features
```

Every transformation gets a reference to its parent.

That gives us a reproducible analysis chain.

---

# 7.20 State Flow Example

For one target:

```text
KIC-123456
     │
     ↓
load_light_curve()
     │
     ↓
Analysis AN-001
     │
     ↓
Observation OBS-001
     │
     ↓
Signal SIG-001
     │
     ├──────────────→ Literature
     │                    │
     │                    ↓
     │                 Evidence E1
     │                    │
     └────────────────────┤
                          ↓
                     Hypothesis H1
                          │
                          ↓
                     Critic CR-001
                          │
                          ↓
                  Additional Analysis
                          │
                          ↓
                       AN-002
```

That is exactly the kind of lineage we want to preserve.

---

# 7.21 Final State Architecture

So I recommend locking #7 as:

```text
AstroResearchState
│
├── Research Context
├── Dataset
├── Targets
│
├── Observations
├── Analyses
├── Signals
│
├── Literature
├── Evidence
│
├── Hypotheses
├── Critiques
├── Decisions
│
├── Artifacts
├── Execution
└── Evaluation
```

With this core rule:

> **Agents communicate through structured shared state and references, while PostgreSQL provides persistence and LangGraph manages the active workflow state.**

And the most important provenance chain is:

```text
Raw Data
   ↓
Analysis
   ↓
Observation
   ↓
Interpretation
   ↓
Hypothesis
   ↓
Evidence / Counter-evidence
   ↓
Critique
   ↓
Final Finding
```

**#7 is now locked.**

Next is **#8 — Guardrails**, where we'll design the actual safety/scientific reliability layer: input validation, agent permissions, tool-call validation, iteration limits, numerical verification, citation verification, observation-vs-hypothesis checks, and protection against prompt/tool injection.
