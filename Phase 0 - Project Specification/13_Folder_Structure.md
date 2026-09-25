## #13 — Folder Structure

For AstroAgents, I recommend a **monorepo** with a clear separation between the React frontend, FastAPI backend, scientific tools, agents, evaluation system, and infrastructure.

The structure should make it immediately obvious where each responsibility lives.

### Final structure

```text
astroagents/
│
├── frontend/
│   ├── public/
│   │
│   ├── src/
│   │   ├── app/
│   │   │   ├── router.tsx
│   │   │   ├── providers.tsx
│   │   │   └── App.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   ├── research/
│   │   │   ├── astronomy/
│   │   │   ├── evidence/
│   │   │   ├── evaluation/
│   │   │   └── observability/
│   │   │
│   │   ├── pages/
│   │   │   ├── ResearchWorkspace.tsx
│   │   │   ├── Investigation.tsx
│   │   │   ├── Signals.tsx
│   │   │   ├── Evidence.tsx
│   │   │   ├── Evaluation.tsx
│   │   │   ├── Observability.tsx
│   │   │   └── Settings.tsx
│   │   │
│   │   ├── hooks/
│   │   ├── stores/
│   │   ├── services/
│   │   ├── types/
│   │   ├── utils/
│   │   └── styles/
│   │
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── research.py
│   │   │   │   ├── investigations.py
│   │   │   │   ├── signals.py
│   │   │   │   ├── evidence.py
│   │   │   │   ├── evaluations.py
│   │   │   │   └── observability.py
│   │   │   │
│   │   │   └── websocket.py
│   │   │
│   │   ├── agents/
│   │   │   ├── manager.py
│   │   │   ├── data_scientist.py
│   │   │   ├── signal_analyst.py
│   │   │   ├── literature_agent.py
│   │   │   ├── hypothesis_agent.py
│   │   │   ├── critic.py
│   │   │   └── evaluation_agent.py
│   │   │
│   │   ├── workflow/
│   │   │   ├── graph.py
│   │   │   ├── nodes.py
│   │   │   ├── routing.py
│   │   │   └── state.py
│   │   │
│   │   ├── tools/
│   │   │   ├── data/
│   │   │   ├── astronomy/
│   │   │   ├── analysis/
│   │   │   ├── literature/
│   │   │   └── verification/
│   │   │
│   │   ├── scientific/
│   │   │   ├── preprocessing/
│   │   │   ├── periodicity/
│   │   │   ├── transit/
│   │   │   ├── anomaly/
│   │   │   └── features/
│   │   │
│   │   ├── rag/
│   │   │   ├── ingestion.py
│   │   │   ├── retrieval.py
│   │   │   ├── reranking.py
│   │   │   └── evidence.py
│   │   │
│   │   ├── guardrails/
│   │   │   ├── input.py
│   │   │   ├── permissions.py
│   │   │   ├── tool_validation.py
│   │   │   ├── scientific_claims.py
│   │   │   ├── evidence.py
│   │   │   └── loop_control.py
│   │   │
│   │   ├── models/
│   │   │   ├── research.py
│   │   │   ├── target.py
│   │   │   ├── analysis.py
│   │   │   ├── signal.py
│   │   │   ├── hypothesis.py
│   │   │   ├── evidence.py
│   │   │   ├── critique.py
│   │   │   └── evaluation.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── research.py
│   │   │   ├── tools.py
│   │   │   ├── events.py
│   │   │   └── reports.py
│   │   │
│   │   ├── services/
│   │   │   ├── research_service.py
│   │   │   ├── literature_service.py
│   │   │   ├── evidence_service.py
│   │   │   └── report_service.py
│   │   │
│   │   ├── integrations/
│   │   │   ├── mast.py
│   │   │   ├── nasa_ads.py
│   │   │   ├── llm.py
│   │   │   └── langfuse.py
│   │   │
│   │   ├── database/
│   │   │   ├── session.py
│   │   │   ├── repositories/
│   │   │   └── migrations/
│   │   │
│   │   ├── observability/
│   │   │   ├── tracing.py
│   │   │   ├── logging.py
│   │   │   └── metrics.py
│   │   │
│   │   ├── config/
│   │   │   └── settings.py
│   │   │
│   │   └── prompts/
│   │       ├── manager/
│   │       ├── data_scientist/
│   │       ├── signal_analyst/
│   │       ├── literature/
│   │       ├── hypothesis/
│   │       └── critic/
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   ├── tools/
│   │   ├── guardrails/
│   │   └── workflow/
│   │
│   ├── pyproject.toml
│   └── Dockerfile
│
├── evaluation/
│   ├── datasets/
│   │   ├── benchmark/
│   │   └── hidden/
│   │
│   ├── tasks/
│   │   ├── signal_detection.py
│   │   ├── period_estimation.py
│   │   ├── transit_detection.py
│   │   └── anomaly_detection.py
│   │
│   ├── judges/
│   │   ├── reasoning.py
│   │   ├── hypothesis.py
│   │   └── evidence.py
│   │
│   ├── metrics/
│   │   ├── scientific.py
│   │   ├── tools.py
│   │   ├── evidence.py
│   │   └── efficiency.py
│   │
│   ├── ablations/
│   └── runner.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── evaluation/
│   └── README.md
│
├── knowledge/
│   ├── documents/
│   ├── chunks/
│   └── README.md
│
├── infrastructure/
│   ├── docker/
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.dev.yml
│   │   └── docker-compose.prod.yml
│   │
│   ├── postgres/
│   │   └── init.sql
│   │
│   └── nginx/
│       └── nginx.conf
│
├── scripts/
│   ├── download_data.py
│   ├── prepare_dataset.py
│   ├── ingest_knowledge.py
│   └── run_evaluation.py
│
├── docs/
│   ├── architecture/
│   ├── agents/
│   ├── tools/
│   ├── evaluation/
│   └── api/
│
├── .github/
│   └── workflows/
│       ├── test.yml
│       ├── build.yml
│       └── deploy.yml
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

## The most important separation

There are four areas I particularly want to keep separate:

### 1. `agents/`

Contains **LLM-driven behavior**.

```text
agents/
├── manager.py
├── data_scientist.py
├── signal_analyst.py
├── literature_agent.py
├── hypothesis_agent.py
└── critic.py
```

These files answer:

> **What should the agent decide/do next?**

---

### 2. `tools/`

Contains the **LLM-callable interface**.

```text
tools/
├── data/
├── astronomy/
├── analysis/
├── literature/
└── verification/
```

For example:

```text
agents/data_scientist.py
        ↓
tools/analysis/periodogram.py
        ↓
scientific/periodicity/lomb_scargle.py
```

This gives us three distinct layers:

```text
Agent
  ↓
Tool interface
  ↓
Deterministic scientific implementation
```

That's much cleaner than putting scientific calculations directly inside an agent.

---

### 3. `scientific/`

This is your **actual scientific computing layer**.

For example:

```text
scientific/
└── periodicity/
    └── lomb_scargle.py
```

It should contain ordinary Python functions that can be tested independently of an LLM.

Example:

```python
def calculate_periodogram(
    time,
    flux,
    min_period,
    max_period
):
    ...
```

You should be able to test this with:

```text
LLM = OFF
Agent = OFF
Database = OFF
```

and still verify the scientific calculation.

---

### 4. `evaluation/`

Keep evaluation **outside the production agent code**.

This is important.

You don't want:

```text
Agent → knows ground truth → evaluates itself
```

Instead:

```text
                  ┌───────────────┐
                  │ AstroAgents   │
                  └───────┬───────┘
                          │
                   investigation
                          │
                          ▼
                  ┌───────────────┐
                  │ Evaluation    │
                  │ Engine        │
                  └───────┬───────┘
                          │
                  hidden ground truth
                          │
                          ▼
                       Metrics
```

The `evaluation/datasets/hidden/` directory should never be exposed to the agent during an evaluation run.

---

# Database models vs Pydantic schemas

One small but important distinction:

```text
models/
```

should represent **database persistence**.

```text
schemas/
```

should represent **API/tool/state contracts**.

For example:

```text
models/signal.py
```

→ SQLAlchemy database model.

While:

```text
schemas/tools.py
```

→ Pydantic tool request/result.

This prevents your database schema from becoming tightly coupled to your API schema.

---

# Prompts

Keep prompts in their own directory:

```text
prompts/
├── manager/
├── data_scientist/
├── signal_analyst/
├── literature/
├── hypothesis/
└── critic/
```

Don't bury huge prompts inside Python files.

This also makes **prompt versioning and Langfuse observability** easier.

For example:

```text
prompts/critic/v1.txt
prompts/critic/v2.txt
```

Later you can evaluate:

```text
Critic prompt v1
        vs
Critic prompt v2
```

without changing the agent implementation.

---

# What should NOT go into Git

Your `.gitignore` should exclude:

```text
.env
__pycache__/
.venv/
node_modules/
dist/
data/raw/
data/processed/
knowledge/documents/
*.parquet
*.fits
*.h5
```

Especially don't commit the actual Kepler data.

The repository should contain **scripts/configuration for obtaining the data**, not gigabytes of astronomical data.

---

# One refinement: don't overbuild the MVP

The structure above is the **target architecture**, but you shouldn't create 100 empty files on day one.

Initially, you can start with:

```text
backend/app/
├── agents/
├── workflow/
├── tools/
├── scientific/
├── guardrails/
├── schemas/
├── models/
├── api/
└── main.py
```

Then introduce `rag/`, `evaluation/`, `observability/`, etc. as you implement those capabilities.

That keeps the architecture clean without creating unnecessary development overhead.

---

## #13 LOCKED

The key architectural boundaries are:

```text
Frontend
   ↓
API
   ↓
Workflow / Agents
   ↓
Tools
   ↓
Scientific Functions
   ↓
Data / External Services
```

with cross-cutting:

```text
Guardrails
Observability
Evaluation
```

and persistence:

```text
PostgreSQL + pgvector
```

