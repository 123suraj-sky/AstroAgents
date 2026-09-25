#11 — UI Requirements

Now we design the **actual AstroAgents web application**.

The most important decision is:

> **AstroAgents should look like a scientific investigation workspace, not a ChatGPT clone.**

The UI should make the underlying agentic system visible: research progress, signals, evidence, hypotheses, critiques, tool calls, evaluations, and traces.

React is well suited to this because the UI can be composed from reusable components and different investigation states can conditionally render different panels. ([React][1])

---

# 11.1 Overall Application Structure

I recommend this layout:

```text
┌──────────────────────────────────────────────────────────────┐
│ ASTROAGENTS                         Research Run: RUN-00142 │
├───────────────┬──────────────────────────────────────────────┤
│               │                                              │
│  Navigation   │              Main Workspace                  │
│               │                                              │
│  Research     │                                              │
│  Investigations│                                             │
│  Signals      │                                              │
│  Evidence     │                                              │
│  Evaluations  │                                              │
│  Observability│                                              │
│               │                                              │
│  Settings     │                                              │
│               │                                              │
└───────────────┴──────────────────────────────────────────────┘
```

### Sidebar

```text
AstroAgents

▣ Research
◉ Investigations
◌ Signals
◇ Evidence
△ Evaluations
⌁ Observability

────────────

⚙ Settings
```

The sidebar stays relatively minimal.

The main area changes depending on the selected section.

---

# 11.2 Main Pages

I recommend **7 primary pages**:

```text
1. Research Workspace
2. Investigation Details
3. Signals
4. Evidence / Literature
5. Evaluation Dashboard
6. Observability
7. Settings
```

The most important pages are the first six.

---

# 11.3 Page 1 — Research Workspace

This is where the user starts an investigation.

### Layout

```text
┌────────────────────────────────────────────────────────────┐
│ New Research Investigation                                 │
│                                                            │
│ Research Question                                          │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ Identify unusual periodic signals in the selected      │ │
│ │ Kepler targets and investigate possible explanations. │ │
│ └────────────────────────────────────────────────────────┘ │
│                                                            │
│ Dataset                                                    │
│ [ Kepler Research Dataset ▼ ]                             │
│                                                            │
│ Targets                                                    │
│ [ Select targets ]                                        │
│                                                            │
│ Investigation Mode                                         │
│ ● Full Investigation                                      │
│ ○ Signal Detection Only                                   │
│ ○ Literature Analysis                                     │
│                                                            │
│                         [ Start Investigation ]            │
└────────────────────────────────────────────────────────────┘
```

### User inputs

* Research question
* Dataset
* Targets
* Investigation mode
* Optional analysis constraints

We should **not** make the user configure seven agents manually.

The Research Manager handles that.

---

# 11.4 Research Question Examples

Under the input box, provide examples:

```text
Try:

"Find unusual periodic signals among these targets."

"Identify targets with transit-like light-curve patterns."

"Investigate whether the strongest periodic signals
have plausible alternative explanations."
```

This helps demonstrate the intended capabilities without making the UI feel like a generic chatbot.

---

# 11.5 Page 2 — Live Investigation Workspace

Once the user starts a run, the interface changes.

This should be the **main showcase page**.

I'd use a three-panel layout:

```text
┌───────────────────────────────────────────────────────────────┐
│ RUN-00142     ● Running                    02:34 elapsed     │
├───────────────┬─────────────────────────────┬─────────────────┤
│ AGENT FLOW    │ SCIENTIFIC WORKSPACE        │ DETAILS         │
│               │                             │                 │
│ ✓ Manager     │ Light Curve                │ Current Agent   │
│ ✓ Data        │                             │ Data Scientist  │
│ ● Signal      │      [chart]                │                 │
│ ○ Literature  │                             │ Status          │
│ ○ Hypothesis │ Periodogram                 │ Running         │
│ ○ Critic      │      [chart]                │                 │
│               │                             │ Tool            │
│               │ Findings                    │ calculate_...   │
│               │ ...                         │                 │
└───────────────┴─────────────────────────────┴─────────────────┘
```

This page combines:

**agent activity + scientific output + execution details.**

---

# 11.6 Agent Activity Panel

The left panel shows the workflow.

Example:

```text
Research Manager
      ✓
      │
Data Scientist
      ✓
      │
Signal Analyst
      ●
      │
Literature Agent
      ○
      │
Hypothesis Agent
      ○
      │
Critic
      ○
```

But because the workflow is dynamic, it shouldn't be presented as a rigid pipeline.

If the Critic sends the workflow back:

```text
Critic
  ↓
⚠ More analysis required
  ↓
Data Scientist
```

the UI should visibly show that loop.

That's an important visual demonstration of your **agentic workflow**.

---

# 11.7 Agent Status

Each agent can have:

```text
○ Pending
● Running
✓ Completed
⚠ Waiting
✕ Failed
```

Clicking an agent opens its details.

Example:

```text
Data Scientist

Status: Completed

Task
Determine whether significant periodicity exists.

Tools Used
✓ load_light_curve
✓ calculate_periodogram

Result
Period: 3.71284 days
Power: 0.81
FAP: 0.003

Next Action
Signal Analyst
```

---

# 11.8 Scientific Workspace

The center should be the main visual area.

For astronomy, charts are extremely important.

### Light Curve

```text
Flux
 │
 │      ╲      ╲      ╲
 │       ╲      ╲      ╲
 │────────╲──────╲──────╲────
 │
 └──────────────────────── Time
```

### Periodogram

```text
Power
 │
 │             ╭╮
 │             ││
 │      ╭╮     ││
 │──────││─────││────────
 │
 └──────────────────────── Frequency
```

### Folded Light Curve

```text
Flux
 │
 │       ╲
 │        ╲____
 │             ╲
 │───────────────╲──────
 │
 └────────────────────── Phase
```

These shouldn't be decorative charts. Every visualization should be linked to an analysis result.

---

# 11.9 Findings Panel

Show structured scientific findings rather than a giant AI paragraph.

Example:

```text
Findings

✓ Periodic variation detected
  Period: 3.71 days
  Source: AN-004

✓ Repeated flux decreases
  Depth: 0.31%
  Source: AN-005

⚠ Alternative explanation exists
  Stellar variability
  Source: CR-002
```

Each finding should be clickable.

---

# 11.10 Observation / Interpretation / Hypothesis

This deserves a dedicated UI treatment.

For example:

```text
┌───────────────────────────────────────────┐
│ OBSERVATION                               │
│                                           │
│ Periodic brightness decrease detected.   │
│                                           │
│ Period: 3.71 days                         │
│ Source: calculate_periodogram()           │
└───────────────────────────────────────────┘

┌───────────────────────────────────────────┐
│ INTERPRETATION                            │
│                                           │
│ Morphology is consistent with a           │
│ transit-like signal.                     │
└───────────────────────────────────────────┘

┌───────────────────────────────────────────┐
│ HYPOTHESIS                                │
│                                           │
│ An orbiting body could explain the signal.│
│                                           │
│ Status: Under Review                      │
└───────────────────────────────────────────┘
```

This directly reflects one of the core scientific guardrails.

---

# 11.11 Hypothesis Panel

A dedicated section:

```text
Hypotheses

H1
Transit-like phenomenon

Status: Under Review

Supporting Evidence
✓ E-001
✓ E-004

Contradicting Evidence
⚠ E-007

Critic
"Stellar variability remains a plausible
alternative explanation."

[ View Evidence ]
```

Multiple hypotheses can appear simultaneously.

For example:

```text
H1  Transit-like signal       Under Review
H2  Eclipsing binary          Under Review
H3  Stellar variability       Supported by some evidence
H4  Instrumental artifact     Weak evidence
```

The UI should **not turn these into a ranking**. They're competing explanations with evidence attached.

---

# 11.12 Critic Panel

When the Critic runs:

```text
┌──────────────────────────────────────────┐
│ CRITIC REVIEW                            │
├──────────────────────────────────────────┤
│                                          │
│ ⚠ Alternative Explanation                │
│                                          │
│ Stellar variability could produce a      │
│ similar periodic signal.                 │
│                                          │
│ Required Action                          │
│                                          │
│ Run additional variability analysis.     │
│                                          │
│ [ View Analysis ]                        │
└──────────────────────────────────────────┘
```

This makes the agent's contribution obvious.

---

# 11.13 Tool Call Panel

This is essential because **tool calling is one of the project's selling points**.

When an agent calls:

```text
calculate_periodogram()
```

show:

```text
┌──────────────────────────────────────────┐
│ 🔧 TOOL CALL                             │
├──────────────────────────────────────────┤
│ Agent                                    │
│ Data Scientist                           │
│                                          │
│ Tool                                     │
│ calculate_periodogram                    │
│                                          │
│ Arguments                                │
│ target_id: KIC-123456                    │
│ method: lomb_scargle                     │
│                                          │
│ Status                                   │
│ ✓ Completed                              │
│                                          │
│ Runtime                                  │
│ 1.21 sec                                 │
└──────────────────────────────────────────┘
```

Then expandable:

```text
Result

period = 3.71284 days
power = 0.81
false_alarm_probability = 0.003
```

---

# 11.14 Page 3 — Investigation Details

After the run finishes, the user gets a persistent investigation page.

```text
Investigation #RUN-00142

Status: Completed
Duration: 42.8 sec
Targets: 20
Signals: 4
Hypotheses: 7
Evidence: 16

────────────────────────────────────

Summary

[scientific summary]

────────────────────────────────────

Signals
[4 signal cards]

────────────────────────────────────

Hypotheses
[7 hypothesis cards]

────────────────────────────────────

Evidence
[16 evidence items]

────────────────────────────────────

Critic Findings
[3 issues]

────────────────────────────────────

Final Report
[Open Report]
```

---

# 11.15 Page 4 — Signals

This page focuses entirely on detected signals.

Table:

```text
┌────────────┬──────────────┬─────────┬────────┬──────────┐
│ Target     │ Period       │ SNR     │ Type   │ Status   │
├────────────┼──────────────┼─────────┼────────┼──────────┤
│ KIC-123456 │ 3.71 days    │ 11.4    │ Transit-like │ Review │
│ KIC-789012 │ 8.32 days    │ 7.8     │ Periodic    │ Review │
│ KIC-345678 │ 1.92 days    │ 14.2    │ Anomalous   │ Review │
└────────────┴──────────────┴─────────┴────────┴──────────┘
```

Clicking a signal opens:

```text
Signal SIG-001

Target
KIC-123456

Period
3.71 days

Depth
0.31%

SNR
11.4

Morphology
Repeating dip

[Light Curve]
[Periodogram]
[Folded Curve]

Evidence
...

Hypotheses
...
```

---

# 11.16 Page 5 — Evidence / Literature

This page visualizes your RAG system.

```text
Evidence Explorer

Search:
[ transit-like Kepler signals           ]

Filters:
[Year] [Topic] [Source] [Target]

─────────────────────────────────────────

E-001
Paper: ...
Year: 2022

Relevant evidence
"..."

Supports:
H1

Relevance
0.91

Citation status
✓ Verified
```

---

# 11.17 Evidence Provenance

Click an evidence item:

```text
Evidence E-001

Claim
"The observed morphology is consistent
with transit-like signals."

Source
Paper P-017

Section
Results

Retrieved chunk
────────────────────────────
[exact relevant passage]
────────────────────────────

Supports
H1

Citation
✓ Verified
```

This is where AstroAgents can visually demonstrate **grounded scientific reasoning**.

---

# 11.18 Page 6 — Evaluation Dashboard

This should be a separate top-level page.

```text
AstroAgents Evaluation

┌────────────────────────────────────────────┐
│ Task Success             92%               │
│ Numerical Accuracy       98%               │
│ Tool Selection           87%               │
│ Evidence Coverage        91%               │
│ Citation Correctness     95%               │
│ Guardrail Compliance    100%               │
└────────────────────────────────────────────┘
```

Then:

### Benchmark Results

```text
Signal Detection
Period Estimation
Transit Detection
Anomaly Detection
Hypothesis Generation
Critic Effectiveness
```

---

# 11.19 Evaluation Run Comparison

This is where your ablation experiments can be visualized.

For example:

```text
Evaluation Comparison

Baseline
Data + Signal
Data + Signal + Literature
Full System
```

Then metrics:

```text
             Baseline  +Lit  +Critic  Full
Detection      ...      ...    ...     ...
Evidence       ...      ...    ...     ...
Accuracy       ...      ...    ...     ...
```

Don't present this as an overall winner/ranking; the point is to show **how different system configurations behave across different metrics**.

---

# 11.20 Page 7 — Observability

This connects directly to #10.

Main screen:

```text
Observability

Research Runs
──────────────────────────────────────────────

RUN-1042   ✓   32.4s   9 tools    12 LLM calls
RUN-1041   ✓   41.7s  12 tools    16 LLM calls
RUN-1040   ⚠   58.2s  19 tools    18 LLM calls
```

Clicking one opens the trace.

---

# 11.21 Trace Visualization

I'd use a collapsible tree:

```text
RUN-1040
│
├── Research Manager
│   └── LLM
│
├── Data Scientist
│   ├── LLM
│   ├── load_light_curve
│   └── calculate_periodogram
│
├── Signal Analyst
│   ├── LLM
│   └── extract_signal_features
│
├── Literature Agent
│   ├── LLM
│   ├── RAG
│   └── ADS Search
│
├── Hypothesis Agent
│   └── LLM
│
├── Critic
│   ├── LLM
│   └── verify_numerical_result
│
├── Guardrail
│   └── Citation Verification
│
└── Evaluation
```

Every node can expand.

---

# 11.22 Guardrail Dashboard

I'd include a small dedicated view inside Observability:

```text
Guardrails

Allowed tool calls       182
Blocked tool calls         4
Rewritten claims           7
Citation failures          3
Invalid parameters         2
Loop terminations          1
```

Then:

```text
Recent Guardrail Events

14:32  Citation verification   REWRITE
14:34  Tool permission         BLOCK
14:36  Invalid parameter       BLOCK
```

---

# 11.23 Final Research Report

AstroAgents should generate a professional scientific report.

Structure:

```text
ASTROAGENTS RESEARCH REPORT

1. Research Question

2. Dataset

3. Methodology

4. Targets Investigated

5. Observed Signals

6. Signal Characterization

7. Literature Evidence

8. Candidate Hypotheses

9. Critic Findings

10. Additional Analyses

11. Conclusions

12. Uncertainties and Limitations

13. Evidence / References
```

The report should explicitly separate:

```text
OBSERVATIONS
INTERPRETATIONS
HYPOTHESES
```

---

# 11.24 Report Example

Instead of:

> "AstroAgents discovered an exoplanet."

Use:

> **Observation:** A periodic flux decrease with an estimated period of 3.71 days was detected.

> **Interpretation:** The morphology is consistent with a transit-like signal.

> **Candidate hypothesis:** An orbiting body could potentially explain the observed periodicity.

> **Alternative explanation:** Eclipsing-binary behavior remains a possible explanation and was therefore investigated.

That's much more scientifically responsible.

---

# 11.25 Real-Time Updates

The investigation page should update while the workflow runs.

For example:

```text
14:31:02  Research Manager started
14:31:04  Data Scientist started
14:31:06  load_light_curve completed
14:31:07  Periodicity detected
14:31:09  Signal Analyst started
14:31:12  Literature Agent started
14:31:15  Evidence retrieved
14:31:18  Hypothesis generated
14:31:20  Critic identified alternative explanation
14:31:21  Additional analysis requested
```

This will make the multi-agent nature of the application immediately visible.

---

# 11.26 Backend → Frontend Events

For real-time updates, I recommend:

```text
FastAPI
   │
   ↓
WebSocket / SSE
   │
   ↓
React
```

Events could look like:

```json
{
  "event": "tool_completed",
  "run_id": "RUN-00142",
  "agent": "data_scientist",
  "tool": "calculate_periodogram",
  "timestamp": "..."
}
```

The frontend consumes these events and updates the appropriate components.

---

# 11.27 UI State Architecture

We shouldn't put everything into one giant React state object.

Use separate frontend state domains:

```text
Research State
Agent Activity State
Scientific Results State
Evidence State
Evaluation State
Observability State
```

This maps nicely to the backend concepts we've already designed.

React's component model is specifically intended for composing interfaces from reusable components, so we can build the workspace from independent panels rather than one monolithic page. ([React][2])

---

# 11.28 Component Structure

Something like:

```text
src/
│
├── components/
│   ├── layout/
│   │   ├── Sidebar
│   │   ├── TopBar
│   │   └── PageContainer
│   │
│   ├── research/
│   │   ├── ResearchForm
│   │   ├── AgentActivity
│   │   ├── FindingsPanel
│   │   ├── HypothesisCard
│   │   └── CriticPanel
│   │
│   ├── astronomy/
│   │   ├── LightCurveChart
│   │   ├── PeriodogramChart
│   │   ├── FoldedLightCurve
│   │   └── SignalTable
│   │
│   ├── evidence/
│   │   ├── EvidenceCard
│   │   ├── PaperCard
│   │   └── CitationStatus
│   │
│   ├── evaluation/
│   │   ├── MetricCard
│   │   ├── BenchmarkTable
│   │   └── EvaluationRun
│   │
│   └── observability/
│       ├── TraceTree
│       ├── AgentSpan
│       ├── ToolCall
│       └── GuardrailEvent
```

---

# 11.29 Visual Design Direction

I recommend a **scientific mission-control aesthetic**.

Not:

```text
❌ ChatGPT clone
❌ Generic SaaS dashboard
❌ Huge chat box
❌ Excessive gradients
```

Instead:

```text
✓ Dark scientific workspace
✓ Dense but readable information
✓ Astronomy-inspired visualization
✓ Clear data hierarchy
✓ Monospace for technical values
✓ Subtle grid / telemetry elements
✓ Strong charts
✓ Clear status indicators
✓ Expandable technical details
```

Think:

```text
Scientific workstation
+
Mission control
+
Modern developer observability dashboard
```

rather than:

```text
AI chatbot
```

---

# 11.30 Color Semantics

Keep colors **semantic**, not decorative.

For example:

```text
Running       → blue
Completed     → green
Warning       → amber
Blocked       → red
Hypothesis    → purple
Evidence      → neutral/blue
```

The exact visual theme can be decided when we build the frontend.

---

# 11.31 Responsive Design

Desktop is the primary target because the application contains:

* scientific charts
* trace trees
* multiple panels
* evaluation tables

But it should still collapse reasonably on smaller screens:

```text
Desktop

[Agent] [Scientific Workspace] [Details]


Tablet

[Agent + Scientific Workspace]
[Details]


Mobile

[Agent Activity]
[Scientific Result]
[Details]
```

We should **not** attempt to squeeze the entire observability dashboard into a phone layout.

---

# 11.32 MVP UI

We don't need all seven pages immediately.

For the MVP, I'd implement:

### 1. Research Workspace

```text
Research question
Dataset
Targets
Start
```

### 2. Live Investigation

```text
Agent activity
Light curve
Findings
Tool calls
Hypotheses
Critic
```

### 3. Investigation Details

```text
Signals
Evidence
Hypotheses
Final report
```

### 4. Evaluation

```text
Metrics
Benchmark results
```

### 5. Observability

```text
Run traces
Agent spans
Tool calls
Guardrails
```

Everything else can follow.

---

# 11.33 Final UI Architecture

```text
                         AstroAgents
                              │
              ┌───────────────┼────────────────┐
              ↓               ↓                ↓
          Research       Investigations    Signals
              │               │                │
              └───────────────┼────────────────┘
                              ↓
                        Evidence
                              │
                    ┌─────────┴─────────┐
                    ↓                   ↓
              Evaluations         Observability
                    │                   │
                    └─────────┬─────────┘
                              ↓
                         Final Report
```

And the central investigation experience:

```text
┌─────────────────────────────────────────────────────────┐
│ RUN-00142   ● RUNNING                    02:34          │
├──────────────┬──────────────────────────┬───────────────┤
│ AGENT TRACE  │ SCIENTIFIC WORKSPACE     │ INSPECTOR     │
│              │                          │               │
│ ✓ Manager   │ Light Curve              │ Agent         │
│ ✓ Data      │ ───────────────          │ Data Scientist│
│ ● Signal    │                          │               │
│ ○ Literature│ Periodogram              │ Tool          │
│ ○ Hypothesis│ ───────────────          │ BLS           │
│ ○ Critic    │                          │               │
│              │ Findings                 │ Result        │
│              │ Hypotheses               │ Period: ...   │
│              │ Evidence                 │ SNR: ...      │
└──────────────┴──────────────────────────┴───────────────┘
```

This should be the **hero experience of the entire project**.

---

## #11 — Locked

The UI will therefore be a **scientific research workspace** centered around five things:

1. **What the agents are doing**
2. **What the astronomical data shows**
3. **What evidence supports the findings**
4. **How hypotheses are challenged**
5. **How well the agent system performed**

The most important UX decision is:

> **Don't hide the agentic system behind a chat interface. Expose the investigation itself.**

That gives the project a very clear visual identity and also makes your multi-agent architecture, tool calling, guardrails, evaluations, and observability demonstrable rather than merely claimed.

**#11 is now locked.**

[1]: https://react.dev/learn?utm_source=chatgpt.com "Quick Start – React"
[2]: https://react.dev/?utm_source=chatgpt.com "React"
