# Agent Reliability Lab (ARL) — Week 3: Evaluation Engineering Fundamentals

Welcome to the **Week 3** milestone of the **Agent Reliability Lab (ARL)**! This week established a modular, systematic evaluation framework designed to measure agent performance across task correctness, tool selection accuracy, evidence groundedness (hallucination detection), budget compliance, and percentile latencies.

---

## 🎯 Week 3 Objectives & Deliverables

1. **Dataset Management & Isolation (`evals/datasets/`):**
   - Created versioned JSONL datasets separating development (`development.jsonl`) from held-out test scenarios to prevent evaluation leakage.

2. **Modular Assertion Graders (`evals/graders.py`):**
   - `TaskResultGrader`: Assesses output match or authorized safety rejection.
   - `ToolSelectionGrader`: Validates expected tool execution sequences.
   - `GroundednessGrader`: Checks retrieved evidence inclusion to detect hallucinations.
   - `BudgetComplianceGrader`: Ensures executions terminate within step limits without `MAX_STEPS_EXCEEDED` errors.

3. **Evaluation Metrics Module (`evals/metrics.py`):**
   - Computes aggregate metrics including Pass Rate (%), Tool Accuracy (%), Groundedness (%), and $p50$/$p95$ Latency distributions.

---

## 📊 Week 3 Baseline Metrics Summary

- **Dataset:** `evals/datasets/development.jsonl`
- **Total Benchmark Cases:** 5
- **Overall Pass Rate:** 80.0%
- **Tool Accuracy:** 80.0%
- **Groundedness Rate:** 100.0%
- **Latency (p50):** 9.124s
- **Latency (p95):** 13.887s

---

## 🛣️ 8-Week Implementation Roadmap
- [x] **Week 1:** Execution Harness, Schema Validation, Tracing & Deterministic Evals
- [x] **Week 2:** Local LLM Integration (Ollama + Qwen 2.5) & Observation Memory
- [x] **Week 3:** Evaluation Engineering Fundamentals (Modular Graders, Groundedness & Metrics)
- [ ] **Week 4:** OpenTelemetry Tracing, Structured Logging & SQLite Run Persistence
- [ ] **Week 5:** Advanced Harness Engineering (State, Memory & Resumable Checkpoints)
- [ ] **Week 6:** Advanced Evals (Trajectory Quality & LLM-as-a-Judge Calibration)
- [ ] **Week 7:** Experimentation, Regression Testing & GitHub Actions CI/CD Pipeline
- [ ] **Week 8:** Production Platform (FastAPI Backend + Streamlit Dashboard)
