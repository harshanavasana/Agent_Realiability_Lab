# Agent Reliability Lab (ARL) — Week 4: Observability, Tracing & Persistence

Welcome to the **Week 4** milestone of the **Agent Reliability Lab (ARL)**! This week introduced production-grade observability and persistent execution storage to audit agent behavior, diagnose step-level failures, and inspect historical execution runs.

---

## 🎯 Week 4 Objectives & Deliverables

1. **Structured JSON Logging (`observability/logging.py`):**
   - Implemented a custom `JSONFormatter` producing standardized JSON log records with explicit ISO timestamps, log levels, logger scopes, and structured payload metadata.

2. **OpenTelemetry Instrumentation (`observability/telemetry.py`):**
   - Integrated OpenTelemetry `TracerProvider` and `SimpleSpanProcessor`.
   - Instrumented the execution loop with nested parent-child execution spans (`agent_run` -> `step_X`) tracking execution durations and step attributes.

3. **SQLite Run Persistence (`storage/`):**
   - Created `storage/database.py` and `storage/repository.py` managing relational persistence (`arl_runs.db`).
   - Recorded complete run results, trace steps, and payload events into indexed SQLite tables (`runs` and `trace_events`).

---

## 📂 Repository Structure (Week 4 Milestone)

```text
agent-reliability-lab/
├── agent/
│   ├── __init__.py
│   ├── runtime.py       # Core runtime integrated with OpenTelemetry spans & SQLite storage
│   ├── tools.py         # Schema validation & allowlist lookup
│   ├── traces.py        # RunTrace and TraceEvent models
│   ├── model.py         # Ollama HTTP REST adapter
│   ├── instructions.py  # System prompts & schema instructions
│   └── planner.py       # LLMPlanner with conversation & observation memory
├── evals/
│   ├── datasets/        # Versioned evaluation benchmark datasets
│   ├── graders.py       # Modular assertion graders
│   ├── metrics.py       # Percentile latency ($p50$/$p95$) & accuracy metrics
│   └── runner.py        # Benchmark runner
├── observability/
│   ├── __init__.py
│   ├── logging.py       # Structured JSON logger
│   └── telemetry.py     # OpenTelemetry tracer configuration
├── storage/
│   ├── __init__.py
│   ├── database.py      # SQLite schema initializer (arl_runs.db)
│   └── repository.py    # Run & trace event CRUD repository
├── reports/             # Generated JSON evaluation execution reports
├── tests/
│   ├── test_runtime.py       # 11 unit & fault-injection harness tests
│   ├── test_llm_planner.py   # 3 local LLM integration tests
│   └── test_observability.py # SQLite database persistence test
├── arl_runs.db          # Local SQLite execution database
├── pyproject.toml
└── README.md
