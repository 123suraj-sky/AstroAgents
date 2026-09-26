# AstroAgents — Agent Instructions

This file is the primary guide for any AI agent working in this repository.
Read it fully before writing a single line of code.

---

## 1. Project Overview

**AstroAgents** is a multi-agent AI scientific discovery system built around astronomical datasets. A researcher submits a question; the system orchestrates a team of specialized agents (Research Manager → Data Scientist → Astronomy Agent → Literature Agent → Hypothesis Agent → Critic Agent → Evaluation Agent) that collaboratively investigate the question and produce an evidence-backed research report.

**Stack at a glance**

| Layer | Tech |
|---|---|
| Frontend | React 19 + TypeScript, Vite 8, vanilla CSS |
| Backend | Python 3.10+, FastAPI, uvicorn |
| Agent framework | LangGraph (see `backend/app/workflow/`) |
| LLM integrations | `backend/app/integrations/llm.py` |
| Observability | Langfuse (`backend/app/integrations/langfuse.py`) |
| Infra | Docker Compose (`docker-compose.yml`) |

---

## 2. Before You Start Any Task

Run through this checklist **every time**, in order:

1. **Check `.agents/TASKS.md`** — see what is currently in progress. Never duplicate or conflict with active work.
2. **Check `.agents/MEMORY.md`** — read known issues, past decisions, and context from previous sessions.
3. **Read relevant `docs/` files** — before implementing anything, read the docs that relate to your task:
   - `docs/01_ps.md` — full project specification and architecture
   - `docs/02_start.md` — setup and getting started
   - `docs/03_web_app.md` — frontend/UI specification
   - `docs/agents/` — agent design documents
   - `docs/api/` — API contracts
   - `docs/architecture/` — system design
   - `docs/evaluation/` — evaluation framework
   - `docs/tools/` — tool definitions
4. **Verify dependencies before importing** — check `frontend/package.json` or `backend/pyproject.toml` before adding any import. Never assume a library is installed.

---

## 3. Repository Layout

```
AstroAgents/
├── frontend/               # React + TypeScript SPA
│   └── src/
│       ├── assets/         # SVG icons and images
│       ├── components/     # Reusable UI components
│       ├── pages/          # Route-level page components
│       ├── hooks/          # Custom React hooks
│       ├── stores/         # State management
│       ├── services/       # API service layer
│       ├── types/          # TypeScript type definitions
│       ├── utils/          # Utility functions
│       └── styles/         # Global styles
├── backend/
│   └── app/
│       ├── agents/         # Agent implementations
│       ├── api/routes/     # FastAPI route handlers
│       ├── api/websocket.py
│       ├── config/         # Settings
│       ├── database/       # DB session, migrations, repositories
│       ├── guardrails/     # Input, output, and tool guardrails
│       ├── integrations/   # LLM, Langfuse, NASA ADS, MAST
│       ├── models/         # Pydantic/SQLAlchemy models
│       ├── observability/  # Logging, metrics, tracing
│       ├── prompts/        # Prompt templates per agent
│       ├── rag/            # Evidence, ingestion, retrieval, reranking
│       ├── schemas/        # Request/response schemas
│       ├── scientific/     # Astronomy computation modules
│       ├── services/       # Business logic services
│       ├── tools/          # Agent tool definitions
│       └── workflow/       # LangGraph graph, nodes, routing, state
├── docs/                   # All project documentation
├── data/                   # Datasets
├── evaluation/             # Evaluation harness
├── knowledge/              # RAG knowledge base
├── scripts/                # Utility scripts
├── infrastructure/         # Deployment configs
├── AGENTS.md               # ← this file
├── SKILLS.md               # Installed Kiro skills reference
└── skill-lock.json         # Skill integrity manifest
```

---

## 4. Frontend Rules

### 4.1 SVG Icons — Always Import, Never Inline

**Do not** write `<svg>...</svg>` markup inline in JSX for static icons.

```tsx
// ❌ WRONG — inline SVG for a static icon
<svg width="16" height="16" viewBox="0 0 16 16">
  <path d="M8 1L..." />
</svg>

// ✅ CORRECT — imported from assets
import editIcon from '../../assets/17_edit.svg';
<img src={editIcon} alt="Edit" className="w-4 h-4" />
```

**Exception:** dynamic or animated SVGs (e.g. loading spinners, progress rings driven by JS) may stay inline because they require runtime manipulation.

**Asset naming convention:** `NN_name.svg` where `NN` is a zero-padded two-digit number following the highest existing number in `frontend/src/assets/`.
Example sequence: `01_search.svg`, `02_close.svg`, `17_edit.svg`, `18_delete.svg`.

When adding a new icon:
1. Drop the `.svg` file into `frontend/src/assets/` with the next available number.
2. Import it at the top of the component file.
3. Render with `<img src={icon} alt="descriptive label" className="w-X h-X" />`.

### 4.2 No Emoji Icons in Components

**Do not** use emoji characters as UI icons in component markup.

```tsx
// ❌ WRONG
<button>🔍 Search</button>
<span>⚠️</span>

// ✅ CORRECT
import searchIcon from '../../assets/01_search.svg';
<button><img src={searchIcon} alt="" aria-hidden="true" /> Search</button>
```

Using text emoji as icons breaks accessibility, dark/light mode theming, and sizing consistency.

### 4.3 Component Standards

- **TypeScript strictly** — no `any` types without a comment justifying it.
- **`min-h-[100dvh]`** instead of `h-screen` for full-height sections — prevents the iOS Safari viewport jump.
- **CSS Grid over Flexbox math** — never `w-[calc(33%-1rem)]`; use `grid-cols-3 gap-4` instead.
- **No hardcoded pixel widths** — use `rem`, `%`, `max-width`, or Tailwind utilities.
- **Always provide** loading, empty, and error states for any component that fetches data.
- **Forms** — label above input, error text below input, never placeholder-as-label.
- **Semantic HTML** — use `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, not `<div>` soup.
- **Alt text** — every meaningful `<img>` needs a descriptive `alt`. Decorative images use `alt=""`.

### 4.4 Styling

- Global styles live in `frontend/src/styles/`.
- Component-scoped styles use CSS modules or the existing pattern — match what's already in the file.
- Check `frontend/src/App.css` and `frontend/src/index.css` before adding new global rules.

---

## 5. Backend Rules

- **FastAPI patterns** — route handlers in `backend/app/api/routes/`, business logic in `backend/app/services/`.
- **Pydantic models** for all request/response shapes — never pass raw dicts across layer boundaries.
- **Guardrails are mandatory** — any new agent output that makes a scientific claim must pass through the relevant guardrail in `backend/app/guardrails/`.
- **Tool permissions** — each agent gets only the tools it needs (see `docs/tools/`). Do not give an agent access to tools outside its defined scope.
- **Observability** — wrap new agent calls with the tracing helpers in `backend/app/observability/tracing.py`.
- **Prompts** — agent prompts live in `backend/app/prompts/<agent_name>/`. Never hardcode prompt strings inside agent Python files.
- **No arithmetic in LLM responses** — any numerical claim from an LLM must be verified by the Python tool layer.

---

## 6. Skills — When to Use Which

All installed skills are documented in `SKILLS.md`. Key rules for using them in this project:

### 6.1 Frontend / UI Work

Before starting any frontend design or implementation task, ask yourself which skill applies:

| Task | Recommended skill |
|---|---|
| Building or animating a UI component | `animate` |
| Making the app feel native on mobile | `mobile-native` |
| Picking a React library (toast, drag-drop, etc.) | `pick-ui-library` |
| Reviewing animation code quality | `review-animations` |
| Finding where the UI should animate | `find-animation-opportunities` |
| Auditing or planning animation fixes | `improve-animations` |
| Prototyping multiple UI directions | `prototype` |
| Polishing or critiquing an interface | `impeccable` |
| Applying Emil Kowalski's UI philosophy | `emil-design-eng` |
| Apple-style fluid, gesture-driven UI | `apple-design` |
| Working with Sonner toasts | `ask-sonner` |
| Naming a motion effect | `animation-vocabulary` |

### 6.2 Design Style / Aesthetic Direction

**When multiple skills could achieve the same visual goal, ask the user which direction to take before proceeding.** The skills below represent genuinely different aesthetics — don't pick one silently.

| Aesthetic goal | Skills to choose between |
|---|---|
| Premium landing page / marketing | `taste-skill` vs `soft-skill` vs `gpt-tasteskill` |
| Minimalist / editorial UI | `minimalist-skill` vs `taste-skill` (low-variance preset) |
| Upgrading an existing UI | `redesign-skill` vs `taste-skill` (redesign mode) vs `impeccable` |
| High-agency creative build | `gpt-tasteskill` vs `soft-skill` vs `taste-skill` |
| Brutalist / industrial style | `brutalist-skill` (unique — no overlap) |

**Prompt to show the user when there's ambiguity:**

> "I can approach this with a few different design philosophies. Which fits best?
> - **`taste-skill`** — reads the brief, infers direction, anti-slop; good for most cases
> - **`soft-skill`** — agency-level, Double-Bezel architecture, haptic depth
> - **`gpt-tasteskill`** — Awwwards-level with GSAP motion
> - **`minimalist-skill`** — clean editorial, warm monochrome, no gradients
> Which direction should I take?"

### 6.3 Image Generation Tasks

| Task | Skill |
|---|---|
| Website section design references | `imagegen-frontend-web` |
| Mobile app screen concepts | `imagegen-frontend-mobile` |
| Brand identity / logo boards | `brandkit` |
| Design image → implement as code | `image-to-code-skill` |

### 6.4 Other Skills

| Task | Skill |
|---|---|
| Force complete, untruncated output | `output-skill` |
| Generate a DESIGN.md for Stitch | `stitch-skill` |
| Writing Swift code | `write-swift` |

### 6.5 Which taste-skill version to use

- **Default:** `taste-skill` (v2 — `design-taste-frontend`)
- **Only use `taste-skill-v1`** if you have been explicitly told a feature depends on its v1 behavior.

---

## 7. Observability & Tracing

Every research session produces a trace. When adding new agent interactions:

- Wrap LLM calls with the tracing helpers in `backend/app/observability/tracing.py`.
- Log metrics via `backend/app/observability/metrics.py`.
- Use structured logging from `backend/app/observability/logging.py` — not `print()`.
- Langfuse integration lives in `backend/app/integrations/langfuse.py`.

---

## 8. Testing

- Backend tests live in `backend/tests/`.
- Evaluation harness lives in `evaluation/`.
- Run backend tests with `pytest` from the `backend/` directory.
- Do not modify `evaluation/` scripts without reading `docs/evaluation/` first.

---

## 9. Git Hygiene

- **Never commit to `main` directly.** Always use a feature branch.
- **Stage specific files** — not `git add .` or `git add -A`.
- **Never commit `.env` files** — use `.env.example` as the template.
- Commit messages: imperative mood, present tense (`Add hypothesis agent routing`, not `Added` or `Adding`).
- Keep PRs focused. One feature or fix per PR.

---

## 10. Environment

- Copy `.env.example` to `.env` and fill in values before running locally.
- Frontend dev server: `cd frontend && npm run dev`
- Backend dev server: `cd backend && uvicorn app.main:app --reload`
- Full stack: `docker-compose up`
- Python virtual env: `.venv/` in the project root (already present).

---

## 11. Quick Checklist Before Submitting Work

- [ ] Read `.agents/TASKS.md` and `.agents/MEMORY.md` before starting
- [ ] Read the relevant `docs/` files for the task
- [ ] No inline SVGs for static icons — all in `frontend/src/assets/`
- [ ] No emoji used as UI icons
- [ ] Correct SVG naming convention followed (`NN_name.svg`)
- [ ] No `h-screen` — use `min-h-[100dvh]`
- [ ] Loading, empty, and error states provided for data-fetching components
- [ ] All dependencies verified in `package.json` or `pyproject.toml` before importing
- [ ] Scientific claims pass through the appropriate guardrail
- [ ] New agent calls are wrapped with observability tracing
- [ ] Prompts live in `backend/app/prompts/`, not hardcoded in agent files
- [ ] Correct skill loaded for the design task
- [ ] Ambiguous multi-skill design decisions confirmed with the user first
