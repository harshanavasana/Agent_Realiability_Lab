# Agent Reliability Lab (ARL) — Week 6: Advanced Evaluation Engineering

Welcome to the **Week 6** milestone of the **Agent Reliability Lab (ARL)**! This week introduced process-level evaluation metrics: trajectory efficiency scoring, LLM-as-a-Judge rubric grading, and adversarial prompt injection benchmarks.

---

## 🎯 Week 6 Objectives & Deliverables

1. **Trajectory Evaluation & Path Efficiency (`evals/graders/trajectory.py`):**
   - Built `TrajectoryEvaluator` to measure total execution steps against optimal paths, detecting redundant tool iterations and penalizing inefficient execution trajectories.

2. **LLM-as-a-Judge Rubric Grading (`evals/graders/llm_judge.py`):**
   - Implemented `LLMJudge` utilizing local Qwen 2.5 to score open-ended responses across Accuracy, Groundedness, and Clarity on a 0.0–1.0 scale with structured reasoning.

3. **Adversarial & Safety Benchmarking (`evals/datasets/adversarial.jsonl`):**
   - Added adversarial scenarios testing harness resilience under prompt injection attempts, unauthorized privilege escalation, and malformed queries.

4. **Package Refactoring:**
   - Modularized `evals/graders/` into a package directory supporting extensible grader plugins.

---

## 📂 Repository Structure (Week 6 Milestone)

```text
agent-reliability-lab/
├── agent/
│   ├── __init__.py
│   ├── runtime.py       # Core execution runtime with tracing & persistence
│   ├── tools.py         # Schema validation & allowlist lookup
│   ├── traces.py        # RunTrace and TraceEvent models
│   ├── model.py         # Ollama HTTP REST adapter
│   ├── instructions.py  # System prompts & schema instructions
│   └── planner.py       # LLMPlanner with conversation & observation memory
├── harness/
│   ├── state.py         # State machine & history context manager
│   ├── retries.py       # Bounded exponential backoff retry executor
│   └── policies.py      # Tool permission levels & safety policies
├── evals/
│   ├── datasets/        # Development, test, and adversarial datasets
│   ├── graders/         # Grader package
│   │   ├── __init__.py  # Task, Tool, Groundedness & Budget graders
│   │   ├── trajectory.py# Trajectory efficiency evaluator
│   │   └── llm_judge.py # LLM-as-a-Judge evaluator
│   ├── metrics.py       # Metrics calculator ($p50$/$p95$ latency)
│   └── runner.py        # Comprehensive evaluation runner
├── observability/
│   ├── logging.py       # Structured JSON logger
│   └── telemetry.py     # OpenTelemetry tracer configuration
├── storage/
│   ├── database.py      # SQLite schema initializer
│   └── repository.py    # Persistent run & checkpoint CRUD repository
├── tests/
│   ├── test_runtime.py          # 11 unit & fault-injection harness tests
│   ├── test_llm_planner.py      # 3 local LLM integration tests
│   ├── test_observability.py    # SQLite run persistence test
│   ├── test_harness_advanced.py # 2 advanced harness tests
│   └── test_evals_advanced.py   # 2 trajectory & judge tests
├── arl_runs.db          # Local SQLite execution database
├── pyproject.toml
└── README.md
