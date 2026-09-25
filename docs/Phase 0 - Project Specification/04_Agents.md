#4 — Exact Agent Design

Now that the workflow is locked, we should define each agent as an actual **software component**, not just a role/persona.

The key principle I recommend for AstroAgents is:

> **Every agent gets a defined purpose, input schema, output schema, tool permissions, and state access.**

This will make the system much easier to implement, evaluate, and observe.

---

## 4.1 Agent Architecture

I recommend **7 agents**:

```text
                    ┌─────────────────────┐
                    │ Research Manager    │
                    │    Supervisor       │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ↓                 ↓                 ↓
      Data Scientist     Signal Analyst    Literature Agent
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ↓
                     Hypothesis Agent
                               ↓
                        Critic Agent
                               │
                     ┌─────────┴─────────┐
                     ↓                   ↓
               More Analysis         Evaluation
                     │                   │
                     └──→ Research ←─────┘
                           Report
```

---

# 4.2 Research Manager / Supervisor

### Purpose

The **Research Manager** is responsible for deciding what should happen next.

It should **not perform scientific calculations**.

### Input

```json
{
  "research_question": "...",
  "dataset_id": "...",
  "target_ids": [],
  "constraints": {}
}
```

### Output

A structured decision:

```json
{
  "next_agent": "data_scientist",
  "task": "Analyze periodicity of candidate signals",
  "reason": "Periodic behavior has not yet been quantified",
  "priority": "high"
}
```

### Tools

It can use:

* `get_dataset_metadata`
* `get_analysis_status`
* `get_available_agents`

But I would **not** give it arbitrary scientific tools.

### Permissions

```text
Can:
✓ Read investigation state
✓ Delegate tasks
✓ Decide next step
✓ Request additional analysis
✓ Terminate investigation

Cannot:
✗ Modify raw data
✗ Execute arbitrary Python
✗ Search arbitrary web pages
✗ Directly generate scientific measurements
```

### Important property

This is your main **routing/decision-making agent**.

---

# 4.3 Data Scientist Agent

This is the most important tool-calling agent.

### Purpose

Perform numerical and statistical analysis on the light curves.

### Input

```json
{
  "target_id": "KIC-123456",
  "light_curve_reference": "...",
  "analysis_request": "Determine whether significant periodicity exists"
}
```

### Output

```json
{
  "target_id": "KIC-123456",
  "findings": [
    {
      "metric": "period",
      "value": 3.72,
      "unit": "days"
    },
    {
      "metric": "signal_to_noise",
      "value": 11.8
    }
  ],
  "anomalies": [],
  "analysis_status": "complete"
}
```

### Tools

This agent gets the largest scientific toolset:

```text
load_light_curve()
clean_light_curve()
normalize_light_curve()

calculate_statistics()
calculate_periodogram()
estimate_period()
calculate_snr()

detect_anomalies()
extract_features()

plot_light_curve()
plot_periodogram()
```

Potentially later:

```text
run_statistical_test()
compare_signal_populations()
```

### Permissions

```text
✓ Read datasets
✓ Run scientific computations
✓ Generate visualizations
✓ Store derived results

✗ Modify raw dataset
✗ Search literature
✗ Make scientific claims beyond computed results
✗ Generate hypotheses
```

That last restriction is useful.

The Data Scientist should say:

> "Period = 3.72 days."

not:

> "Therefore this is an exoplanet."

---

# 4.4 Signal Analyst Agent

### Purpose

Interpret the numerical results in an astronomical context.

### Input

```json
{
  "target_id": "KIC-123456",
  "statistical_results": {},
  "light_curve_features": {},
  "visualization_references": []
}
```

### Output

```json
{
  "classification": "transit_like",
  "observations": [
    "Periodic brightness decrease",
    "Period approximately 3.72 days",
    "Repeated signal morphology"
  ],
  "interpretation": [
    "The signal is consistent with a transit-like pattern"
  ],
  "uncertainties": [
    "Could also be associated with eclipsing binary behavior"
  ]
}
```

### Tools

```text
fold_light_curve()
compare_signal_shapes()
estimate_signal_duration()
calculate_transit_features()
query_kepler_metadata()
```

### Permissions

```text
✓ Read analysis results
✓ Analyze astronomical features
✓ Query astronomy metadata
✓ Produce interpretations

✗ Modify raw data
✗ Search arbitrary literature
✗ Declare a hypothesis as established fact
```

---

# 4.5 Literature Agent

### Purpose

Connect the current investigation to existing scientific literature.

This is where our later **RAG layer** will primarily live.

### Input

```json
{
  "research_question": "...",
  "signal_characteristics": {},
  "candidate_interpretations": []
}
```

### Output

```json
{
  "sources": [
    {
      "paper_id": "...",
      "title": "...",
      "relevance": "...",
      "evidence": "...",
      "citation": "..."
    }
  ],
  "comparison": [
    "Observed period is similar to..."
  ]
}
```

### Tools

```text
search_scientific_literature()
retrieve_paper()
search_local_knowledge_base()
retrieve_chunks()
verify_citation()
```

Later we can decide whether this uses:

* local vector DB
* scientific APIs
* live search
* hybrid search

### Permissions

```text
✓ Search scientific sources
✓ Retrieve papers
✓ Query RAG
✓ Extract evidence
✓ Verify citations

✗ Modify datasets
✗ Run arbitrary scientific code
✗ Generate unsupported scientific conclusions
```

---

# 4.6 Hypothesis Agent

### Purpose

Generate **possible explanations** for the observations.

This agent should be explicitly designed around the distinction:

```text
Observation ≠ Interpretation ≠ Hypothesis
```

### Input

```json
{
  "observations": [],
  "signal_analysis": {},
  "literature_evidence": []
}
```

### Output

```json
{
  "hypotheses": [
    {
      "id": "H1",
      "statement": "The signal may be caused by a transit-like event",
      "supporting_evidence": ["E1", "E3"],
      "contradicting_evidence": [],
      "status": "proposed"
    },
    {
      "id": "H2",
      "statement": "The signal may be associated with an eclipsing binary",
      "supporting_evidence": ["E2"],
      "contradicting_evidence": [],
      "status": "proposed"
    }
  ]
}
```

### Tools

Mostly:

```text
retrieve_existing_findings()
retrieve_evidence()
```

I would **not** give it powerful scientific tools initially.

Its job is reasoning over evidence, not producing the evidence.

---

# 4.7 Critic Agent

This agent is particularly important for demonstrating **agentic reasoning**.

### Purpose

Try to find weaknesses in the current investigation.

### Input

```json
{
  "observations": [],
  "interpretations": [],
  "hypotheses": [],
  "evidence": []
}
```

### Output

```json
{
  "verdict": "more_analysis_required",
  "issues": [
    {
      "type": "alternative_explanation",
      "description": "Periodic stellar variability could explain the signal"
    }
  ],
  "required_actions": [
    {
      "agent": "data_scientist",
      "task": "Perform additional periodicity analysis"
    }
  ]
}
```

Possible verdicts:

```text
sufficient
more_analysis_required
evidence_conflict
insufficient_data
```

### Tools

The Critic can access:

```text
get_analysis_result()
get_evidence()
verify_calculation()
check_citation()
```

Potentially:

```text
run_independent_statistical_check()
```

Giving the Critic **independent verification tools** is especially interesting.

For example:

```text
Data Scientist:
"Period = 3.72 days"

        ↓

Critic:
"Verify this independently"

        ↓

verification tool

        ↓

3.71 days
```

Now your evaluation system can measure whether agents catch incorrect calculations.

---

# 4.8 Evaluation Agent

### Purpose

Evaluate the **AstroAgents investigation**.

Not:

> "Is this an exoplanet?"

but:

> "Did AstroAgents perform the investigation correctly?"

### Input

It receives the entire investigation record:

```text
Research question
Agent decisions
Tool calls
Tool outputs
Observations
Hypotheses
Critic results
Evidence
Final report
Ground truth
```

### Output

```json
{
  "task_success": 0.91,
  "tool_selection": 0.88,
  "numerical_accuracy": 1.0,
  "evidence_coverage": 0.84,
  "hypothesis_quality": 0.82,
  "guardrail_compliance": 1.0,
  "trajectory_efficiency": 0.76
}
```

We'll design these metrics properly in **#9 Agentic Evals**.

---

# 4.9 Agent State Access

This is an important architectural decision.

**Do not give every agent access to the entire state.**

Instead:

| Agent            | Raw Data |   Analysis |     Literature | Hypotheses |    Critic |
| ---------------- | -------: | ---------: | -------------: | ---------: | --------: |
| Research Manager |     Read |       Read |           Read |       Read |      Read |
| Data Scientist   | **Read** | Read/Write |              — |          — |         — |
| Signal Analyst   |        — |   **Read** |              — |          — |         — |
| Literature Agent |        — |       Read | **Read/Write** |          — |         — |
| Hypothesis Agent |        — |       Read |           Read |  **Write** |         — |
| Critic           |        — |       Read |           Read |       Read | **Write** |
| Evaluation Agent |     Read |       Read |           Read |       Read |      Read |

This provides a basic **least-privilege architecture**.

It also makes your guardrail implementation much more meaningful later.

---

# 4.10 Tool Permissions

I'd explicitly create a permission matrix.

```text
                         Manager Data Signal Literature Hypothesis Critic Eval
load_light_curve           ✓       ✓
calculate_periodicity              ✓
detect_anomalies                    ✓
plot_light_curve                    ✓
query_kepler_metadata                       ✓
search_papers                                      ✓
retrieve_paper                                     ✓
verify_citation                                    ✓                 ✓
generate_hypothesis                                         ✓
verify_calculation                                                ✓
evaluate_run                                                        ✓
```

The important thing is that **the LLM never gets unrestricted access to your backend**.

Instead:

```text
LLM
 ↓
Tool request
 ↓
Tool Guardrail
 ↓
Permission check
 ↓
Parameter validation
 ↓
Resource limits
 ↓
Tool execution
 ↓
Result validation
 ↓
Agent
```

This architecture will later give us a concrete place to demonstrate **guardrails**.

---

# 4.11 Agent Output Contract

I strongly recommend that every agent return structured output rather than free-form text.

For example:

```json
{
  "agent": "data_scientist",
  "status": "complete",
  "task": "...",
  "observations": [],
  "results": [],
  "evidence_refs": [],
  "uncertainties": [],
  "recommended_next_action": null
}
```

This becomes extremely useful for:

* LangGraph state
* Agentic Evals
* observability
* UI
* debugging
* guardrails

And it prevents the system from becoming a giant collection of unstructured LLM responses.

---

# 4.12 Final Agent Design

So I recommend we lock **#4** as:

| Agent                | Core Responsibility             | Main Tools              |
| -------------------- | ------------------------------- | ----------------------- |
| **Research Manager** | Planning + routing + loops      | State/query tools       |
| **Data Scientist**   | Numerical/statistical analysis  | Python/scientific tools |
| **Signal Analyst**   | Astronomical interpretation     | Signal/astronomy tools  |
| **Literature Agent** | Literature + evidence           | Search/RAG tools        |
| **Hypothesis Agent** | Generate candidate explanations | Evidence/state tools    |
| **Critic Agent**     | Challenge/falsify findings      | Verification tools      |
| **Evaluation Agent** | Evaluate the investigation      | Evaluation tools        |

### The key architecture decision

The system isn't:

```text
7 LLMs talking to each other.
```

It is:

```text
                    ┌──────────────┐
                    │ Shared State │
                    └──────┬───────┘
                           │
                     Agent decisions
                           │
              ┌────────────┴────────────┐
              │                          │
           Tools                    Other Agents
              │                          │
              └────────────┬─────────────┘
                           │
                     Guardrails
                           │
                     Tool Results
                           │
                       Shared State
```

That gives AstroAgents a much stronger architecture for demonstrating **multi-agent orchestration + tool calling + controlled agent permissions + agentic loops + evaluation + observability**.

