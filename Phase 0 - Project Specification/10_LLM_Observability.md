#10 — LLM Observability

This should be a **first-class subsystem** of AstroAgents, not just application logging.

The goal is to answer, for every research run:

> **What happened, which agent made each decision, which tools were called, what data came back, how the state changed, what the run cost, and where things went wrong?**

Langfuse is a strong fit here because it supports traces containing LLM calls, tool calls, retrieval, agent steps, evaluation, and guardrails, while using OpenTelemetry underneath. ([Langfuse][1])

---

# 10.1 Observability Architecture

I recommend:

```text
                        User
                         │
                         ↓
                  Research Run
                         │
                         ↓
                ┌─────────────────┐
                │ Research Trace │
                └────────┬────────┘
                         │
       ┌─────────────────┼──────────────────┐
       ↓                 ↓                  ↓
   Agent Span        Agent Span         Agent Span
       │                 │                  │
       ↓                 ↓                  ↓
   LLM Call           Tool Call        Retrieval
       │                 │                  │
       └─────────────────┼──────────────────┘
                         ↓
                  State Transition
                         │
                         ↓
                    Guardrail
                         │
                         ↓
                    Evaluation
                         │
                         ↓
                 Final Research Run
```

OpenTelemetry models operations as nested spans within traces, which maps naturally to this structure. ([OpenTelemetry][2])

---

# 10.2 Recommended Stack

For AstroAgents, I recommend:

### Primary

**Langfuse**

for:

* LLM tracing
* agent traces
* tool calls
* retrieval
* token usage
* cost
* latency
* evaluations
* dashboards

Langfuse supports dedicated observation types for agents, tools, retrieval, evaluators, generations, and guardrails. ([Langfuse][3])

### Underlying standard

**OpenTelemetry**

for:

* traces
* spans
* cross-service correlation
* future infrastructure observability

### Application logs

**Python structured logging**

for backend errors and operational logs.

So:

```text
AstroAgents
     │
     ├── Langfuse
     │      └── LLM / Agent observability
     │
     ├── OpenTelemetry
     │      └── distributed tracing
     │
     └── Structured Logs
            └── application diagnostics
```

---

# 10.3 The Most Important Concept: One Research Run = One Trace

Suppose the user starts:

> "Investigate unusual periodic signals in these Kepler targets."

Create:

```text
Trace ID:
RUN-2026-00042
```

Everything related to that investigation belongs under this trace.

Example:

```text
RUN-2026-00042
│
├── Research Manager
│
├── Data Scientist
│   ├── LLM
│   ├── load_light_curve
│   ├── LLM
│   └── calculate_periodogram
│
├── Signal Analyst
│   ├── LLM
│   └── extract_signal_features
│
├── Literature Agent
│   ├── LLM
│   ├── ADS search
│   └── RAG retrieval
│
├── Hypothesis Agent
│   └── LLM
│
├── Critic
│   ├── LLM
│   └── verify_numerical_result
│
├── Data Scientist
│   └── additional analysis
│
├── Evaluation
│
└── Final Report
```

This is exactly the kind of nested trace structure observability platforms are designed to represent. ([Langfuse][4])

---

# 10.4 Agent-Level Tracing

Each agent execution should be represented separately.

Example:

```text
Agent: Data Scientist
Duration: 4.82 sec
Status: SUCCESS
Iteration: 2
```

Its span contains:

```text
Input
Task
LLM call
Tool calls
Tool results
Output
State changes
```

So you can inspect:

> Why did the Data Scientist decide to run BLS?

rather than only seeing the final result.

---

# 10.5 LLM Generation Tracing

Every actual LLM invocation should be separately recorded.

For example:

```text
Generation #37

Agent:
Data Scientist

Model:
<model>

Input tokens:
2,183

Output tokens:
421

Latency:
1.84 sec

Tool requested:
calculate_periodogram
```

This is important because an agent loop may contain many LLM calls.

Langfuse specifically recommends recording individual model invocations rather than aggregating an entire agent loop into one generation, because otherwise you lose visibility into intermediate decisions, token usage, and problematic context growth. ([Langfuse][5])

---

# 10.6 Tool Call Tracing

Every tool call should become its own observation.

Example:

```text
Tool:
calculate_periodogram

Arguments:
{
    "target_id": "KIC-123456",
    "method": "lomb_scargle"
}

Started:
14:31:08

Completed:
14:31:09

Duration:
1.21 sec

Status:
SUCCESS
```

Then:

```text
Result:
period = 3.71284
power = 0.81
FAP = 0.003
```

This allows us to inspect:

```text
Agent decision
      ↓
Tool
      ↓
Arguments
      ↓
Execution
      ↓
Result
      ↓
Next decision
```

---

# 10.7 Retrieval Tracing

The Literature Agent should expose retrieval as separate trace steps.

For example:

```text
Literature Agent
│
├── Query generation
│
├── Local RAG retrieval
│   ├── 20 candidates
│   └── top 5 selected
│
├── ADS search
│   └── 10 results
│
├── Deduplication
│
└── Evidence extraction
```

Langfuse has a dedicated `retriever` observation type for retrieval operations such as vector stores and knowledge sources. ([Langfuse][3])

---

# 10.8 Guardrail Tracing

This connects directly to #8.

Suppose the Hypothesis Agent attempts an unauthorized tool call:

```text
Hypothesis Agent
       │
       ↓
run_box_least_squares()
       │
       ↓
Permission Guardrail
       │
       ↓
BLOCKED
```

Trace:

```text
Guardrail:
agent_permission

Agent:
hypothesis_agent

Tool:
run_box_least_squares

Decision:
BLOCK

Reason:
Tool not permitted
```

This is much more useful than merely logging:

```text
ERROR: unauthorized tool
```

Langfuse has a dedicated `guardrail` observation type, making this distinction natural in the observability layer. ([Langfuse][3])

---

# 10.9 State Transition Tracing

This is something I'd add **even though it's not automatically provided by the LLM framework**.

Whenever the shared state changes:

```text
Before:
current_stage = signal_analysis

After:
current_stage = literature_review
```

record:

```json
{
  "event": "state_transition",
  "from": "signal_analysis",
  "to": "literature_review",
  "trigger": "signal_requires_external_evidence"
}
```

This lets you answer:

> Why did the workflow move from Signal Analysis to Literature?

---

# 10.10 Decision Tracing

The Research Manager's decisions deserve explicit tracing.

For example:

```text
Decision D-019

Current state:
Signal characterized

Critic status:
Alternative explanation exists

Decision:
Run additional analysis

Target agent:
Data Scientist

Reason:
Need to test stellar variability hypothesis
```

This is especially useful because **agentic behavior is about decisions**, not merely LLM text.

---

# 10.11 Complete Trace Example

A real AstroAgents trace might look like:

```text
RUN-00042
│
├── Research Manager [2.1s]
│   └── LLM [1.7s]
│
├── Data Scientist [5.4s]
│   ├── LLM [1.3s]
│   ├── load_light_curve [0.8s]
│   ├── LLM [0.9s]
│   └── calculate_periodogram [2.1s]
│
├── Signal Analyst [3.7s]
│   ├── LLM [2.2s]
│   └── extract_signal_features [1.2s]
│
├── Literature Agent [6.8s]
│   ├── LLM [1.9s]
│   ├── RAG [0.4s]
│   ├── ADS Search [2.1s]
│   └── Evidence Extraction [1.8s]
│
├── Hypothesis Agent [2.4s]
│   └── LLM [2.0s]
│
├── Critic [4.1s]
│   ├── LLM [1.7s]
│   └── verify_numerical_result [1.9s]
│
├── Guardrail [0.01s]
│   └── claim verification
│
├── Data Scientist [3.2s]
│   └── additional analysis
│
└── Evaluation [4.3s]
```

That is the trace I want to eventually show in your project.

---

# 10.12 Trace Metadata

Every trace should contain common metadata:

```json
{
  "research_run_id": "RUN-00042",
  "dataset_id": "kepler_subset_v1",
  "dataset_version": "v1",
  "environment": "production",
  "model": "...",
  "workflow_version": "0.1.0",
  "git_commit": "...",
  "timestamp": "...",
  "user_request_type": "periodic_signal_investigation"
}
```

The **Git commit** is particularly useful.

It lets you answer:

> Which version of AstroAgents generated this result?

---

# 10.13 Model Metadata

For every LLM call:

```text
Model
Provider
Temperature
Max tokens
Prompt version
System prompt version
Input tokens
Output tokens
Latency
Cost
```

This becomes very useful when you later compare models.

For example:

```text
Model A
vs
Model B
```

on exactly the same evaluation benchmark.

---

# 10.14 Prompt Versioning

Don't store only:

```text
prompt = "Analyze this..."
```

Also store:

```text
prompt_version = "data_scientist_v3"
```

Then if performance changes:

```text
v2 → v3
```

you can correlate the change with evaluation results.

This is especially useful because prompt changes can affect agent behavior even when the underlying code stays the same.

---

# 10.15 Tool Metadata

Each tool call should include:

```json
{
  "tool_name": "calculate_periodogram",
  "tool_version": "1.2.0",
  "arguments": {
    "target_id": "KIC-123456"
  },
  "duration_ms": 1210,
  "status": "success"
}
```

This allows us to investigate tool-specific problems.

For example:

```text
calculate_periodogram
Success rate: 99.4%
Average latency: 1.8 sec
```

---

# 10.16 Error Tracing

Errors should be structured.

Bad:

```text
Something went wrong.
```

Good:

```json
{
  "error_type": "ToolExecutionError",
  "agent": "data_scientist",
  "tool": "calculate_periodogram",
  "target_id": "KIC-123456",
  "retry_count": 1,
  "message": "...",
  "recoverable": true
}
```

Then the workflow can decide:

```text
recoverable → retry
non-recoverable → escalate
```

---

# 10.17 Retry Tracing

Suppose a literature search fails.

Trace:

```text
ADS Search
   ↓
HTTP 503
   ↓
Retry #1
   ↓
HTTP 503
   ↓
Retry #2
   ↓
Success
```

The trace should preserve all of this.

Otherwise your latency numbers become misleading.

---

# 10.18 Token and Cost Tracking

At the research-run level:

```text
Total LLM calls: 17
Input tokens: 24,421
Output tokens: 6,212
Total tokens: 30,633

LLM cost: $X
Tool cost: $Y
Total: $Z
```

At the agent level:

```text
Data Scientist
Tokens: 7,200

Literature Agent
Tokens: 12,400

Critic
Tokens: 5,100
```

This can reveal where the system is spending most of its resources.

---

# 10.19 Latency Breakdown

Instead of:

```text
Total runtime = 43 seconds
```

show:

```text
Research Manager       3.1s
Data Scientist         8.7s
Signal Analyst         5.4s
Literature             12.6s
Hypothesis             4.1s
Critic                 7.2s
Evaluation             4.0s
──────────────────────────
Total                  45.1s
```

And further:

```text
LLM latency
Tool latency
RAG latency
External API latency
```

This will make performance optimization much easier.

---

# 10.20 Evaluation Integration

This is where #9 and #10 connect.

After the run:

```text
Research Trace
       │
       ├── Final result
       ├── Tool trajectory
       ├── Agent decisions
       ├── Guardrails
       └── Evidence
              │
              ↓
       Evaluation Engine
              │
              ↓
        Evaluation Scores
```

Those scores should be attached to the trace.

For example:

```text
RUN-00042

Task Success:         0.92
Numerical Accuracy:   0.98
Tool Selection:       0.87
Evidence Coverage:    0.91
Guardrail Compliance: 1.00
```

Langfuse supports scores/evaluation alongside traces, which fits this architecture well. ([Langfuse][1])

---

# 10.21 The AstroAgents Observability Dashboard

I'd make a dedicated **Observability** page.

### Top-level view

```text
┌───────────────────────────────────────────────┐
│ AstroAgents Observability                     │
├───────────────────────────────────────────────┤
│                                               │
│ Research Runs          1,248                  │
│ Avg Runtime            38.4 sec               │
│ Avg Tool Calls          8.7                   │
│ Avg LLM Calls          12.3                   │
│ Guardrail Blocks        2.1%                  │
│                                               │
├───────────────────────────────────────────────┤
│ Recent Runs                                  │
│                                               │
│ RUN-1042   SUCCESS   32.4s   9 tools         │
│ RUN-1041   SUCCESS   41.7s  12 tools         │
│ RUN-1040   WARNING   58.2s  19 tools         │
└───────────────────────────────────────────────┘
```

---

# 10.22 Individual Trace Page

Clicking `RUN-1040`:

```text
Research Run #1040
────────────────────────────────

Research Question
"Investigate unusual periodic signals..."

Status: WARNING
Runtime: 58.2s
LLM Calls: 18
Tool Calls: 19

Agent Trace
────────────────────────────────

Research Manager
    ↓
Data Scientist
    ↓
calculate_periodogram
    ↓
Signal Analyst
    ↓
Literature Agent
    ↓
Hypothesis Agent
    ↓
Critic
    ↓
⚠ Additional analysis requested
    ↓
Data Scientist
    ↓
Critic
    ↓
Evaluation
```

Each node should be expandable.

---

# 10.23 Agent Detail

Click:

> Data Scientist

Show:

```text
Agent
Data Scientist

Task
Determine significant periodicity.

LLM Calls
2

Tools
load_light_curve
calculate_periodogram

Input
...

Decision
"Need periodicity analysis."

Tool Arguments
...

Tool Result
period = 3.71284 days

Output
...
```

This is far more useful than a generic chat transcript.

---

# 10.24 Tool Detail

Click:

> calculate_periodogram

Show:

```text
Tool
calculate_periodogram

Agent
Data Scientist

Input
KIC-123456

Method
Lomb-Scargle

Runtime
1.21 sec

Result
Period: 3.71284 days
Power: 0.81
FAP: 0.003

Verification
✓ Passed
```

---

# 10.25 Guardrail Detail

Click:

> ⚠ Citation verification

Show:

```text
Guardrail Event

Agent:
Literature Agent

Claim:
"..."

Citation:
Paper P-012

Result:
PARTIALLY SUPPORTED

Action:
REWRITE

Reason:
Source discusses the phenomenon but
does not support the causal claim.
```

This makes your guardrails tangible rather than just a checkbox on the architecture diagram.

---

# 10.26 Observability Metrics

I recommend tracking at least:

### Reliability

```text
success rate
error rate
retry rate
tool failure rate
```

### Performance

```text
total latency
agent latency
LLM latency
tool latency
retrieval latency
```

### AI usage

```text
LLM calls
tokens
cost
model usage
```

### Agent behavior

```text
tool calls
tool selection
repeated actions
loop iterations
agent transitions
```

### Scientific quality

```text
numerical verification
evidence coverage
citation failures
unsupported claims
```

### Guardrails

```text
blocked tools
invalid arguments
prompt injection attempts
claim rewrites
loop terminations
```

---

# 10.27 Alerts

Later, we can configure alerts such as:

```text
IF
tool failure rate > threshold
→ alert
```

```text
IF
average research runtime increases significantly
→ alert
```

```text
IF
unsupported claim rate increases
→ alert
```

```text
IF
LLM cost per research run increases
→ alert
```

This becomes useful once AstroAgents is deployed.

---

# 10.28 Privacy / Sensitive Trace Data

One thing we should design from the start:

**Don't blindly record every piece of data into observability.**

For example:

```text
API keys
tokens
credentials
private user information
```

must never appear in traces.

Use:

```text
redaction
masking
allowlists
```

for trace attributes.

Scientific data can also be referenced by IDs rather than copied repeatedly into prompts/traces.

---

# 10.29 Final Architecture

So I recommend locking #10 as:

```text
                         AstroAgents
                              │
                              ↓
                     Research Run Trace
                              │
             ┌────────────────┼────────────────┐
             ↓                ↓                ↓
           Agents           Tools          Retrieval
             │                │                │
             ↓                ↓                ↓
           LLMs          Tool Results       Evidence
             │                │                │
             └────────────────┼────────────────┘
                              ↓
                       State Changes
                              │
             ┌────────────────┼────────────────┐
             ↓                ↓                ↓
        Guardrails       Errors/Retries    Decisions
             │                │                │
             └────────────────┼────────────────┘
                              ↓
                         Evaluation
                              │
                              ↓
                       Langfuse / OTEL
                              │
                              ↓
                    Observability Dashboard
```

### Recommended stack

```text
Langfuse
   ↓
LLM / Agent / Tool / RAG / Evaluation tracing

OpenTelemetry
   ↓
Standard trace infrastructure

Python structured logging
   ↓
Backend operational logs
```

Langfuse's current documentation specifically supports tracing LLM calls, retrieval, tools, agents, evaluators, and guardrails, and its OpenTelemetry integration helps avoid locking the application to a proprietary tracing model. ([Langfuse][6])

---

## #10 — Locked

The key principle is:

> **Every research run should be reconstructable from its trace.**

You should be able to answer:

**What did the user ask?**
→ Research trace

**What did each agent do?**
→ Agent spans

**Why did it do it?**
→ Decision/state events

**Which tools were called?**
→ Tool observations

**What data came back?**
→ Tool outputs

**What literature was retrieved?**
→ Retrieval observations

**Were there guardrail violations?**
→ Guardrail observations

**How expensive/slow was it?**
→ Tokens, cost, latency

**Was the result actually good?**
→ Evaluation scores

That gives AstroAgents a genuine **LLM observability layer**, rather than simply adding console logs.

[1]: https://langfuse.com/docs/observability/overview?utm_source=chatgpt.com "LLM Observability & Application Tracing (Open Source) - Langfuse"
[2]: https://opentelemetry.io/docs/specs/otel/trace/api/?utm_source=chatgpt.com "Tracing API | OpenTelemetry"
[3]: https://langfuse.com/docs/observability/features/observation-types?utm_source=chatgpt.com "Observation Types - Langfuse"
[4]: https://langfuse.com/docs/observability/data-model?utm_source=chatgpt.com "Observability Data Model - Langfuse"
[5]: https://langfuse.com/docs/observability/best-practices?utm_source=chatgpt.com "What does a good trace look like? - Langfuse"
[6]: https://langfuse.com/docs?utm_source=chatgpt.com "Open Source AI Engineering Platform - Langfuse"
