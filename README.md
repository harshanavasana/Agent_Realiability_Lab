# Agent Reliability Lab (ARL) — Week 7: Experimentation, Regression & CI/CD

Welcome to the **Week 7** milestone of the **Agent Reliability Lab (ARL)**! This week established a scientific framework for harness A/B testing, component ablation studies, automated quality regression gating, and CI integration.

---

## 🎯 Week 7 Objectives & Deliverables

1. **Harness Comparison Framework (`experiments/comparison.py`):**
   - Built `HarnessComparator` to run side-by-side evaluation benchmark passes across different harness configurations, calculating precise metric deltas ($\Delta$ Pass Rate, $\Delta$ Tool Accuracy).

2. **Ablation Studies (`experiments/ablation.py`):**
   - Implemented controlled ablation testing functions to measure the exact contribution of specific harness components (e.g., step budgets, retry limits).

3. **Automated Regression Quality Gate (`evals/regression.py`):**
   - Created `run_regression_gate()` to evaluate model pass rates against configurable minimum quality thresholds, blocking builds (`sys.exit(1)`) if performance degrades.

4. **Continuous Integration Pipeline (`.github/workflows/evals.yml`):**
   - Formatted a GitHub Actions workflow that executes all 19 pytest unit and integration tests automatically on pushes and pull requests.

---

## 📂 Repository Structure (Week 7 Milestone)

```text
agent-reliability-lab/
├── .github/
│   └── workflows/
│       └── evals.yml        # GitHub Actions CI workflow configuration
├── agent/
│   ├── runtime.py           # Core execution runtime
│   ├── tools.py             # Schema validation & allowlist lookup
│   ├── traces.py            # Trace models
│   ├── model.py             # Ollama HTTP adapter
│   ├── instructions.py      # System prompts
│   └── planner.py           # LLMPlanner with conversation memory
├── harness/
│   ├── state.py             # State machine manager
│   ├── retries.py           # Bounded retry executor
│   └── policies.py          # Safety & permission policies
├── evals/
│   ├── datasets/            # Benchmark datasets
│   ├── graders/             # Grader package (Task, Tool, Groundedness, Trajectory, LLM Judge)
│   ├── metrics.py           # Metric calculator ($p50$/$p95$ latency)
│   ├── runner.py            # Evaluation runner
│   └── regression.py        # Automated quality gate
├── experiments/
│   ├── __init__.py
│   ├── comparison.py        # Harness A/B comparison framework
│   └── ablation.py          # Ablation study runner
├── observability/
│   ├── logging.py           # Structured JSON logger
│   └── telemetry.py         # OpenTelemetry configuration
├── storage/
│   ├── database.py          # SQLite schema initializer
│   └── repository.py        # SQLite repository
├── tests/
│   ├── test_runtime.py          # 11 harness & fault-injection tests
│   ├── test_llm_planner.py      # 3 local LLM integration tests
│   ├── test_observability.py    # 1 persistence test
│   ├── test_harness_advanced.py # 2 advanced harness tests
│   ├── test_evals_advanced.py   # 2 trajectory & judge tests
│   └── test_experiments.py      # 1 experiment comparison test
├── arl_runs.db              # Local SQLite database
├── pyproject.toml
└── README.md
