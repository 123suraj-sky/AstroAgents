#6 — RAG Strategy

For AstroAgents, I recommend **not making RAG the center of the system**. The scientific computation should come from the Kepler data and deterministic tools; RAG should provide **scientific context and evidence**.

So the architecture should be:

```text
                 AstroAgents
                      │
        ┌─────────────┴─────────────┐
        │                           │
 Scientific Data               Scientific Knowledge
        │                           │
 Kepler Light Curves              RAG / Search
        │                           │
 Python/Astropy                 Literature Agent
        │                           │
        └─────────────┬─────────────┘
                      ↓
              Evidence-backed
              investigation
```

---

## 6.1 What exactly should RAG answer?

The Literature Agent should answer questions such as:

> "Have similar periodic signals been reported?"

> "What phenomena can produce this type of light-curve morphology?"

> "What characteristics distinguish a transit from an eclipsing binary?"

> "What statistical methods are commonly used to analyze this type of signal?"

> "Has this particular Kepler target already been studied?"

It should **not** answer:

> "What is the period of this signal?"

That should come from your scientific tools.

So:

| Question                                 | Source               |
| ---------------------------------------- | -------------------- |
| What is the period?                      | Scientific tool      |
| What is the SNR?                         | Scientific tool      |
| Is there an anomaly?                     | Scientific/ML tool   |
| What does the signal resemble?           | Signal Agent + tools |
| Has this phenomenon been studied?        | **RAG/Literature**   |
| What explanations are known?             | **RAG/Literature**   |
| What papers support this interpretation? | **RAG/Literature**   |

This separation is important for scientific reliability.

---

# 6.2 Knowledge Sources

For the MVP, I recommend **two knowledge layers**.

### Layer 1 — Curated local scientific knowledge

Create a small, controlled corpus containing relevant astronomy papers.

Possible topics:

```text
Kepler mission
Kepler light curves
Transit detection
Box Least Squares
Lomb-Scargle
Stellar variability
Eclipsing binaries
Transit false positives
Light-curve anomalies
Kepler pipeline
Exoplanet detection
```

This gives you a **reproducible evaluation corpus**.

---

### Layer 2 — Live scientific literature search

Use **NASA ADS (Astrophysics Data System)** as the primary literature search source.

ADS is operated by the Smithsonian Astrophysical Observatory under a NASA cooperative agreement and maintains a very large astronomy/astrophysics literature index. ([Astrophysics Data System][1])

ADS also provides a developer API for programmatic search and related functionality. ([ADS.][2])

This is particularly suitable for AstroAgents because ADS supports:

* keyword searches
* fielded searches
* astronomical object searches
* citations
* references
* related-paper discovery

([ADS.][3])

---

# 6.3 Local RAG + Live Search

I recommend a **hybrid approach**:

```text
                     Literature Agent
                           │
              ┌────────────┴────────────┐
              ↓                         ↓
        Local RAG                     ADS
       curated corpus             live search
              │                         │
              └────────────┬────────────┘
                           ↓
                   Evidence Ranking
                           ↓
                   Evidence Selection
                           ↓
                     Agent Context
```

### Why both?

**Local RAG**

Gives you:

* reproducibility
* predictable evaluation
* fast retrieval
* controlled knowledge
* no dependency on live search

**ADS**

Gives you:

* current literature
* broader coverage
* object-specific searches
* citation/reference relationships

ADS explicitly supports object-based searches and citation/reference queries, which are useful when investigating individual astronomical targets. ([ADS.][4])

---

# 6.4 What should go into the Vector Database?

Don't simply download random PDFs and embed everything.

Instead, create a structured corpus.

For each paper:

```text id="8p8f7r"
Paper
│
├── Metadata
│   ├── title
│   ├── authors
│   ├── year
│   ├── DOI
│   ├── ADS ID
│   └── arXiv ID
│
├── Abstract
│
├── Sections
│   ├── Introduction
│   ├── Methods
│   ├── Results
│   ├── Discussion
│   └── Conclusion
│
└── Evidence chunks
```

Each chunk should retain metadata:

```json id="o3p5yv"
{
  "paper_id": "paper_001",
  "chunk_id": "paper_001_chunk_17",
  "section": "Results",
  "text": "...",
  "year": 2021,
  "topics": [
    "transit",
    "Kepler",
    "light_curve"
  ]
}
```

This becomes extremely useful later when generating citations.

---

# 6.5 Chunking Strategy

For scientific papers, I would **not use arbitrary fixed-size chunks only**.

Prefer:

```text
Paper
 ↓
Sections
 ↓
Paragraphs
 ↓
Semantic chunks
```

For example:

```text
Methods
  ├── Data preprocessing
  ├── Period search
  ├── Transit detection
  └── Statistical validation
```

A chunk should ideally contain one coherent scientific idea.

For example:

```text
Chunk:

"The Box Least Squares algorithm searches for
periodic box-shaped decreases in flux and is
therefore useful for identifying transit-like
signals..."
```

rather than:

```text
Chunk 1:
"...Box Least Squares..."

Chunk 2:
"...periodic..."

Chunk 3:
"...transit..."
```

---

# 6.6 Retrieval Pipeline

The Literature Agent should work like this:

```text
Research Context
      ↓
Generate Search Query
      ↓
┌───────────────────────┐
│ Local Vector Search   │
└───────────┬───────────┘
            │
            +
┌───────────▼───────────┐
│ NASA ADS Search       │
└───────────┬───────────┘
            ↓
       Merge Results
            ↓
     Deduplicate Papers
            ↓
       Rerank Evidence
            ↓
     Retrieve Top Chunks
            ↓
      Evidence Package
            ↓
      Literature Agent
```

---

# 6.7 Don't Let the LLM Decide Relevance Alone

This is an important design choice.

Suppose ADS returns 20 papers.

Don't simply give all 20 to the LLM.

Use:

```text
Initial retrieval
       ↓
Top 20
       ↓
Metadata filtering
       ↓
Embedding similarity
       ↓
Reranking
       ↓
Top 5
       ↓
LLM evidence extraction
```

This reduces context size and makes retrieval more deterministic.

---

# 6.8 Evidence Package

The Literature Agent shouldn't just receive raw text.

It should receive structured evidence:

```json id="q4qv0x"
{
  "query": "periodic transit-like Kepler light curve",
  "evidence": [
    {
      "evidence_id": "E1",
      "paper_id": "P17",
      "title": "...",
      "section": "Methods",
      "text": "...",
      "relevance": 0.91
    },
    {
      "evidence_id": "E2",
      "paper_id": "P42",
      "title": "...",
      "section": "Results",
      "text": "...",
      "relevance": 0.87
    }
  ]
}
```

Then the Hypothesis Agent can say:

```text
H1
Supporting evidence:
E1, E2
```

instead of hallucinating a citation.

---

# 6.9 Citation Architecture

This is where I want AstroAgents to be stronger than a normal RAG chatbot.

Every scientific claim should be traceable:

```text
Claim
 ↓
Evidence ID
 ↓
Chunk
 ↓
Paper
 ↓
ADS / DOI / arXiv
```

For example:

```text
Claim C17
   ↓
Evidence E3
   ↓
Paper P12
   ↓
Section: Results
   ↓
ADS Bibcode / DOI
```

The final report can then display:

> The observed morphology is consistent with previously studied transit-like signals. **[E3]**

Clicking `[E3]` could show:

```text
Evidence E3

Paper:
...

Section:
Results

Relevant passage:
...

Source:
NASA ADS
```

That gives your UI a strong **evidence provenance** feature.

---

# 6.10 Citation Verification

Remember the `verify_citation()` tool from #5?

Now we can give it a real purpose.

Suppose the LLM produces:

```text
Claim:
"Paper X reports that this type of signal
is characteristic of eclipsing binaries."
```

The citation verifier checks:

```text
Claim
 ↓
Retrieve cited evidence
 ↓
Does the evidence actually support the claim?
 ↓
YES / PARTIAL / NO
```

Output:

```json id="2zrqvb"
{
  "claim_id": "C17",
  "source_id": "P12",
  "support": "partial",
  "reason": "The paper discusses eclipsing binaries,
             but does not make the claimed causal statement."
}
```

Then the Critic can challenge the claim.

This creates a nice chain:

```text
RAG
 ↓
Claim
 ↓
Citation
 ↓
Verification
 ↓
Critic
```

---

# 6.11 RAG Should Be Evidence Retrieval, Not Answer Generation

This distinction is important.

Don't build:

```text
Question
 ↓
RAG
 ↓
LLM answer
```

Instead build:

```text
Question
 ↓
Literature Agent
 ↓
Search
 ↓
Evidence
 ↓
Scientific interpretation
 ↓
Hypothesis
 ↓
Critic
```

RAG supplies **evidence**.

Agents perform the reasoning.

---

# 6.12 RAG Evaluation

Since Agentic Evals are a major project feature, we'll eventually evaluate the RAG system too.

Metrics can include:

### Retrieval

* Recall@K
* Precision@K
* MRR
* NDCG

### Evidence

* Evidence relevance
* Evidence coverage
* Citation correctness
* Citation completeness

### Generation

* Unsupported claim rate
* Citation-grounded claim rate
* Contradiction rate

For example:

```text id="mby8ws"
100 scientific claims
        ↓
82 have supporting evidence
        ↓
75 have directly supporting evidence
```

Then:

```text
Evidence coverage = 82%
Direct support rate = 75%
```

We'll formalize this later in **#9 Agentic Evals**.

---

# 6.13 Local RAG Technology

For the first implementation, I recommend:

```text
PostgreSQL
    +
pgvector
```

rather than immediately introducing another database.

Your architecture can be:

```text
PostgreSQL
│
├── users
├── research_runs
├── targets
├── analyses
├── hypotheses
├── papers
├── evidence
└── embeddings
```

This keeps the initial infrastructure simpler.

Later, if the corpus grows substantially, we can evaluate a dedicated vector database.

---

# 6.14 What About ArXiv?

Use it as a **secondary source**, not the primary search interface.

ADS already indexes arXiv e-prints and provides links to available full text. ([Astrophysics Data System][1])

So our preferred hierarchy is:

```text
                 Literature Search
                        │
                        ↓
                 NASA ADS first
                        │
              ┌─────────┴─────────┐
              ↓                   ↓
       Local Knowledge       External Results
              │                   │
              │             ┌─────┴─────┐
              │             ↓           ↓
              │          arXiv       Publisher
              │
              └──────────┬─────────────┘
                         ↓
                    Evidence
```

---

# 6.15 RAG Architecture We'll Lock

The final design becomes:

```text
                       Literature Agent
                              │
                              ↓
                    Query Generation
                              │
                  ┌───────────┴───────────┐
                  ↓                       ↓
             Local RAG                 NASA ADS
           curated papers          scientific search
                  │                       │
                  └───────────┬───────────┘
                              ↓
                         Deduplicate
                              ↓
                           Rerank
                              ↓
                     Retrieve Evidence
                              ↓
                    Evidence Validation
                              ↓
                       Evidence Store
                              ↓
                  Hypothesis / Critic
```

### Technology choice

For MVP:

```text
Embedding Model
      ↓
PostgreSQL + pgvector
      ↓
Local scientific corpus

NASA ADS API
      ↓
Live literature retrieval
```

ADS provides an API specifically intended for programmatic access to its search and related capabilities. ([ADS.][2])

---

# 6.16 What I Would NOT Do

Avoid these designs:

### ❌ RAG over the entire internet

Too noisy and difficult to evaluate.

### ❌ Give every agent literature search

Only the Literature Agent should normally have that capability.

### ❌ Put entire PDFs into prompts

Use structured chunks and evidence retrieval.

### ❌ Let the LLM invent citations

Every citation must correspond to a stored evidence object.

### ❌ Use RAG to calculate scientific measurements

Numerical results come from the scientific tools.

### ❌ Treat retrieved papers as ground truth

Papers provide **evidence and context**, not automatic truth.

---

# #6 — Locked Design

So AstroAgents will use a **Hybrid Scientific RAG** architecture:

| Component                 | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| **Local curated corpus**  | Reproducible scientific knowledge          |
| **PostgreSQL + pgvector** | Embedding/vector retrieval                 |
| **NASA ADS**              | Live astronomy literature search           |
| **Evidence store**        | Track exact supporting passages            |
| **Reranking**             | Select the most relevant evidence          |
| **Citation verifier**     | Check claim ↔ source support               |
| **Critic Agent**          | Challenge unsupported/weak interpretations |

And the core philosophy is:

> **Scientific tools produce measurements. RAG provides scientific evidence. Agents reason over both.**

That separation will make the later **guardrails, evaluations, and observability** much cleaner.

**#6 is now locked.**

[1]: https://prod.adsabs.harvard.edu/about/?utm_source=chatgpt.com "About ADS"
[2]: https://ui.adsabs.harvard.edu/help/api/?utm_source=chatgpt.com "ADS API"
[3]: https://ui.adsabs.harvard.edu/help/gettingstarted/literature-search?utm_source=chatgpt.com "Beginning a literature search"
[4]: https://ui.adsabs.harvard.edu/help/search/search-syntax?utm_source=chatgpt.com "Search Syntax"
