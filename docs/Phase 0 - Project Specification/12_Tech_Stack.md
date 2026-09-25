## #12 — Tech Stack

For **AstroAgents**, I’d lock the stack around Python for the scientific/agent backend and React for the research workspace UI. The goal is to demonstrate the architecture without adding infrastructure that doesn't materially improve the project.

### 12.1 Final Stack

| Layer                    | Technology                | Purpose                                               |
| ------------------------ | ------------------------- | ----------------------------------------------------- |
| **Frontend**             | React + TypeScript        | Research workspace UI                                 |
| **Build**                | Vite                      | Fast frontend development/build                       |
| **Styling**              | Tailwind CSS              | UI styling                                            |
| **UI Components**        | shadcn/ui                 | Consistent professional components                    |
| **Charts**               | Plotly.js                 | Interactive light curves, periodograms, folded curves |
| **Frontend State**       | Zustand                   | Research/workspace state                              |
| **Server State**         | TanStack Query            | API data, caching, refetching                         |
| **Backend API**          | FastAPI                   | REST API + streaming                                  |
| **Agent Framework**      | LangGraph                 | Stateful multi-agent workflow                         |
| **LLM Interface**        | LiteLLM                   | Provider/model abstraction                            |
| **Structured Outputs**   | Pydantic                  | Agent/tool/state schemas                              |
| **Scientific Computing** | NumPy, Pandas, SciPy      | Numerical analysis                                    |
| **Astronomy**            | Astropy                   | Astronomical/time-series analysis                     |
| **ML**                   | scikit-learn              | Anomaly detection/statistical ML                      |
| **Astronomy Data**       | Astroquery + MAST         | Kepler/MAST retrieval                                 |
| **RAG**                  | pgvector + embeddings     | Scientific knowledge retrieval                        |
| **Database**             | PostgreSQL                | Persistent research state                             |
| **Cache**                | Redis                     | Optional caching/event infrastructure                 |
| **Realtime**             | WebSockets                | Live investigation updates                            |
| **Observability**        | Langfuse + OpenTelemetry  | LLM/agent tracing                                     |
| **Logging**              | Python structured logging | Backend diagnostics                                   |
| **Testing**              | pytest + HTTPX            | Backend/unit/API tests                                |
| **Frontend Testing**     | Vitest + Testing Library  | React tests                                           |
| **Containerization**     | Docker + Docker Compose   | Local/dev deployment                                  |
| **CI/CD**                | GitHub Actions            | Testing/build/deployment                              |
| **API Contract**         | OpenAPI                   | Backend ↔ frontend contract                           |
| **Deployment**           | Azure VM / Docker Compose | Initial production deployment                         |

---

# 12.2 Frontend

### React + TypeScript

Use:

```text
React
TypeScript
Vite
Tailwind CSS
shadcn/ui
```

React is appropriate because the application is highly interactive:

* agent status changes
* live traces
* research state
* charts
* evidence panels
* hypothesis cards
* evaluation dashboards

TypeScript is important because your frontend will consume many structured objects:

```text
ResearchRun
AgentEvent
ToolCall
Observation
Signal
Hypothesis
Evidence
Critique
EvaluationResult
```

This is exactly the kind of application where TypeScript provides significant value.

### Plotly.js

Use **Plotly** for astronomy visualizations.

You need:

```text
Light Curve
    ↓
Periodogram
    ↓
Folded Light Curve
    ↓
Signal annotations
```

Plotly gives you interactive zooming, hovering, selecting regions, and annotations without having to build the visualization layer yourself.

---

# 12.3 Frontend State

Use **two different mechanisms** rather than putting everything into one global store.

### Zustand

For application/workspace state:

```text
currentResearchRun
selectedTarget
selectedSignal
selectedAgent
selectedHypothesis
UI panels
filters
```

### TanStack Query

For server data:

```text
GET /research/runs
GET /research/runs/{id}
GET /signals
GET /evidence
GET /evaluations
```

This gives you a clean separation:

```text
React
 ├── Zustand
 │     └── UI/client state
 │
 └── TanStack Query
       └── server state
```

---

# 12.4 Backend

Use:

```text
Python
FastAPI
Pydantic
```

FastAPI becomes the main application API.

Example:

```text
/api/v1/research
/api/v1/research/{run_id}
/api/v1/signals
/api/v1/evidence
/api/v1/evaluations
/api/v1/observability
```

FastAPI also gives you automatic OpenAPI documentation.

---

# 12.5 Agent Framework

### LangGraph

This is the core orchestration framework.

Your workflow becomes something conceptually like:

```text
Research Manager
       ↓
Data Scientist
       ↓
Signal Analyst
       ↓
Literature Agent
       ↓
Hypothesis Agent
       ↓
Critic
       ↓
 ┌─────┴─────┐
 │           │
More       Report
Analysis
 │
 └──→ Data Scientist
```

The important reason for using LangGraph isn't simply "because it is an agent framework."

It gives you:

* persistent state
* conditional routing
* loops
* checkpoints
* human intervention points
* structured agent execution
* graph visualization/debugging possibilities

That maps directly to the architecture you've already designed.

---

# 12.6 LLM Provider

I recommend **LiteLLM** as the provider abstraction.

Instead of hard-coding your agents to one provider:

```text
Research Manager
       ↓
   LLM interface
       ↓
 ┌─────┼─────┐
OpenAI  Gemini  Anthropic
```

You can switch models without rewriting the agent architecture.

For example:

```text
Development → cheaper model
Evaluation → fixed model
Production → selected model
```

More importantly, your portfolio project demonstrates **model abstraction**, rather than being tied to one API.

---

# 12.7 Structured Outputs

### Pydantic

Pydantic should be used everywhere structured data crosses a boundary.

For example:

```python
class ToolRequest(BaseModel):
    tool_name: str
    parameters: dict
    agent: str
```

and:

```python
class Hypothesis(BaseModel):
    hypothesis_id: str
    statement: str
    status: str
    supporting_evidence: list[str]
    contradicting_evidence: list[str]
```

This is especially important for your guardrails.

Architecture:

```text
LLM
 ↓
Pydantic validation
 ↓
Guardrail
 ↓
Tool
 ↓
Pydantic result validation
 ↓
State
```

---

# 12.8 Scientific Computing

The scientific layer should remain deterministic Python.

### Core

```text
NumPy
Pandas
SciPy
```

### Astronomy

```text
Astropy
Astroquery
```

### ML

```text
scikit-learn
```

Your architecture should deliberately separate:

```text
LLM reasoning
        │
        ▼
Tool request
        │
        ▼
Deterministic scientific code
        │
        ▼
Numerical result
        │
        ▼
LLM interpretation
```

This separation is one of the strongest technical aspects of the project.

The LLM should **not** calculate a period by itself.

It should call:

```text
calculate_periodogram()
```

and receive something like:

```json
{
  "period_days": 3.72,
  "power": 0.81,
  "false_alarm_probability": 0.003
}
```

---

# 12.9 Astronomy Data

Use:

```text
Astroquery
     ↓
MAST
     ↓
Kepler data
```

The application shouldn't bundle massive astronomical datasets inside Docker.

Instead:

```text
Target ID
   ↓
MAST/Astroquery
   ↓
Light curve
   ↓
Cache / processing
   ↓
Analysis
```

For reproducibility, store:

```text
dataset_id
dataset_version
target_id
data_source
retrieval_timestamp
processing_version
```

---

# 12.10 PostgreSQL + pgvector

Use **PostgreSQL as the primary database**.

Don't introduce MongoDB.

Your database can contain:

```text
research_runs
targets
analyses
observations
signals
hypotheses
critiques
literature
evidence
decisions
tool_calls
guardrail_events
evaluation_results
```

And use:

```text
PostgreSQL
      +
   pgvector
```

for your local scientific knowledge base.

That gives you one primary database rather than:

```text
PostgreSQL
MongoDB
Pinecone
Redis
...
```

which would be unnecessary for this project.

---

# 12.11 RAG

The RAG stack becomes:

```text
Scientific papers
      ↓
Chunking
      ↓
Embeddings
      ↓
PostgreSQL + pgvector
      ↓
Similarity search
      ↓
Reranking
      ↓
Evidence
```

You can additionally query NASA ADS when appropriate.

So:

```text
Literature Agent
      │
      ├── Local RAG
      │
      └── NASA ADS
             ↓
       Evidence Store
```

This reinforces the principle we already locked:

> RAG provides scientific evidence; scientific tools provide measurements.

---

# 12.12 Redis

Redis should be **optional**, not foundational.

Use it for things like:

```text
temporary caching
job coordination
rate limiting
short-lived realtime state
```

Don't make Redis the source of truth.

Your architecture remains:

```text
PostgreSQL → persistent state
Redis      → temporary/cache infrastructure
LangGraph  → active workflow state
```

---

# 12.13 Real-Time Communication

Use:

```text
FastAPI
   ↓
WebSocket
   ↓
React
```

Example events:

```json
{
  "event": "tool_started",
  "run_id": "RUN-00142",
  "agent": "data_scientist",
  "tool": "calculate_periodogram"
}
```

Then:

```text
Backend
   ↓
WebSocket
   ↓
Live Investigation UI
```

The UI can immediately show:

```text
✓ Data Scientist
✓ load_light_curve
⟳ calculate_periodogram
○ Signal Analyst
○ Literature Agent
```

---

# 12.14 Observability

This part should remain exactly aligned with #10:

```text
Langfuse
    +
OpenTelemetry
```

### Langfuse

For:

* LLM generations
* prompts
* token usage
* cost
* agent traces
* model latency
* tool calls
* evaluations

### OpenTelemetry

For broader application tracing:

```text
React
 ↓
FastAPI
 ↓
LangGraph
 ↓
Agent
 ↓
Tool
 ↓
PostgreSQL
```

This lets you demonstrate both:

**LLM observability** and **application observability**.

---

# 12.15 Testing

Use:

### Backend

```text
pytest
pytest-asyncio
HTTPX
```

Test:

```text
scientific functions
tools
Pydantic schemas
guardrails
API endpoints
agent routing
```

### Frontend

```text
Vitest
React Testing Library
```

Test:

```text
components
state
API interactions
research workspace
hypothesis cards
evaluation dashboard
```

### Agent evaluation

Keep this separate from normal unit tests:

```text
pytest
   ↓
unit/integration tests

Evaluation Runner
   ↓
benchmark tasks
   ↓
agentic evaluations
```

---

# 12.16 Docker

Use Docker Compose for local development:

```text
docker-compose.yml

├── frontend
├── backend
├── postgres
├── redis
└── langfuse
```

You can also run supporting services separately if needed.

Don't containerize MAST or NASA ADS—they are external services.

---

# 12.17 CI/CD

Use GitHub Actions:

```text
Push
 ↓
Lint
 ↓
Frontend tests
 ↓
Backend tests
 ↓
Build Docker images
 ↓
Security/basic validation
 ↓
Deploy
```

For the portfolio MVP, you don't need Kubernetes.

Docker Compose is sufficient.

---

# 12.18 Deployment

Given your existing experience with Azure VMs and Docker Compose, I'd use:

```text
Azure VM
    ↓
Docker Compose
    ├── Nginx / Frontend
    ├── FastAPI
    ├── PostgreSQL
    └── Redis
```

External:

```text
LLM Provider
NASA MAST
NASA ADS
Langfuse
```

For the first production version, **don't introduce Kubernetes, Kafka, or microservices**.

AstroAgents is already architecturally complex because of the agent workflow. Adding infrastructure complexity would make the project harder to build and explain without improving the core demonstration.

---

# 12.19 Final Architecture

Putting everything together:

```text
                         ┌──────────────────────┐
                         │       React          │
                         │    TypeScript/Vite    │
                         │ Tailwind + shadcn/ui  │
                         │      Plotly.js        │
                         └──────────┬───────────┘
                                    │
                              REST/WebSocket
                                    │
                         ┌──────────▼───────────┐
                         │       FastAPI        │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │      LangGraph       │
                         │  Research Workflow   │
                         └──────────┬───────────┘
                                    │
          ┌──────────┬──────────────┼──────────────┬──────────┐
          ▼          ▼              ▼              ▼          ▼
     Research    Data Scientist  Signal       Literature  Critic
      Manager                    Analyst         Agent
          │          │              │              │          │
          │          ▼              │              ▼          │
          │    Scientific Tools    │        RAG / ADS       │
          │          │              │              │          │
          └──────────┴──────────────┴──────────────┴──────────┘
                                    │
                         ┌──────────▼───────────┐
                         │     Guardrails       │
                         │ Pydantic + Validation│
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼─────────────────┐
                 ▼                  ▼                 ▼
          ┌────────────┐     ┌────────────┐    ┌────────────┐
          │ PostgreSQL │     │   Redis    │    │  pgvector  │
          │   State    │     │   Cache    │    │    RAG     │
          └────────────┘     └────────────┘    └────────────┘

                    ┌─────────────────────────┐
                    │       Observability     │
                    │ Langfuse + OpenTelemetry│
                    └─────────────────────────┘

                    ┌─────────────────────────┐
                    │ Scientific Data Sources │
                    │ MAST / Kepler / NASA ADS│
                    └─────────────────────────┘
```

### The important design decision

I would **lock this principle into the project**:

> **LLMs orchestrate and reason; deterministic scientific tools calculate; PostgreSQL stores provenance; RAG supplies evidence; guardrails validate actions and claims; Langfuse records the entire investigation.**

That single principle makes the architecture coherent rather than just being a collection of AI technologies.

### #12 LOCKED

**Core stack:**

```text
React + TypeScript + Vite
Tailwind + shadcn/ui
Plotly.js
Zustand + TanStack Query

FastAPI
LangGraph
LiteLLM
Pydantic

NumPy
Pandas
SciPy
scikit-learn
Astropy
Astroquery

PostgreSQL
pgvector
Redis

WebSockets

Langfuse
OpenTelemetry

pytest
Vitest
React Testing Library

Docker Compose
GitHub Actions
Azure VM
```


