# Agent Reliability Lab (ARL) — Week 5: Advanced Harness Engineering

Welcome to the **Week 5** milestone of the **Agent Reliability Lab (ARL)**! This week upgraded the execution harness to operate under real-world reliability and safety constraints.

---

## 🎯 Week 5 Objectives & Deliverables

1. **State Machine & History Management (`harness/state.py`):**
   - Implemented explicit `AgentState` transitions (`INITIATED`, `RUNNING`, `WAITING_APPROVAL`, `COMPLETED`, `FAILED`).
   - Added windowed history truncation (`truncate_history`) to prevent context window overflow.

2. **Bounded Retries with Backoff (`harness/retries.py`):**
   - Created `execute_with_retry` wrapper with configurable retry counts and exponential backoff to handle transient tool or network errors gracefully.

3. **Least-Privilege Security Policies (`harness/policies.py`):**
   - Added permission levels (`READ_ONLY` vs `DESTRUCTIVE`) to intercept unauthorized or unsafe tool executions before invocation.

4. **Execution Checkpoints & Resumability (`storage/`):**
   - Updated SQLite database schema (`arl_runs.db`) to record intermediate step execution checkpoints (`checkpoints` table).

---

## 📂 Repository Structure (Week 5 Milestone)

```text
agent-reliability-lab/
├── agent/
│   ├── __init__.py
│   ├── runtime.py       # Integrated state transitions, retries, policy checks & checkpoints
│   ├── tools.py         # Schema validation & allowlist lookup
│   ├── traces.py        # RunTrace and TraceEvent models
│   ├── model.py         # Ollama HTTP REST adapter
│   ├── instructions.py  # System prompts & schema instructions
│   └── planner.py       # LLMPlanner with conversation & observation memory
├── harness/
│   ├── __init__.py
│   ├── state.py         # State machine & history context manager
│   ├── retries.py       # Bounded exponential backoff retry executor
│   └── policies.py      # Tool permission levels & safety policies
├── evals/
│   ├── datasets/        # Benchmark datasets
│   ├── graders.py       # Modular assertion graders
│   ├── metrics.py       # Metrics calculator ($p50$/$p95$ latency)
│   └── runner.py        # Benchmark runner
├── observability/
│   ├── logging.py       # Structured JSON logger
│   └── telemetry.py     # OpenTelemetry tracer configuration
├── storage/
│   ├── database.py      # SQLite schema initializer (runs, trace_events, checkpoints)
│   └── repository.py    # CRUD repository with context-managed database connections
├── tests/
│   ├── test_runtime.py          # 11 unit & fault-injection harness tests
│   ├── test_llm_planner.py      # 3 local LLM integration tests
│   ├── test_observability.py    # SQLite run persistence test
│   └── test_harness_advanced.py # 2 advanced harness tests (retries & permission policies)
├── arl_runs.db          # Local SQLite execution database
├── pyproject.toml
└── README.md
