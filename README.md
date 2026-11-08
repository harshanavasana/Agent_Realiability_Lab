# Agent Reliability Lab (ARL) — Week 2: Local LLM Integration & Observation Memory

Welcome to the **Week 2** milestone of the **Agent Reliability Lab (ARL)**! This repository expands our custom deterministic harness into a functional, non-deterministic AI agent system powered by a local Large Language Model (**Qwen 2.5:1.5B via Ollama**).

---

## 🎯 Week 2 Learning Objectives & Deliverables

In Week 2, we replaced hardcoded deterministic planners with actual LLM reasoning while keeping the execution controls, schema validations, and step budgets established in Week 1.

### Key Features Implemented:
1. **Local Model HTTP Adapter (`agent/model.py`):**
   - Built a custom HTTP client using `httpx` to interface directly with Ollama's local REST API (`http://localhost:11434/api/chat`).
   - Configured JSON mode enforcement (`format="json"`) to constrain token sampling to valid JSON syntax.

2. **Structured Action Parsing & Clean Prompts (`agent/instructions.py`, `agent/planner.py`):**
   - Formatted system instructions and tool definitions.
   - Built robust response sanitization to strip markdown code blocks (e.g., ````json ... ````) before feeding parameters into Pydantic models.
   - Handled task completion signals via explicit `final_answer` actions.

3. **Context & Observation Memory:**
   - Implemented state history tracking inside `LLMPlanner`.
   - Injected tool execution observations back into the prompt history thread so the agent can evaluate previous step outputs and determine when to finish tasks.

4. **Integrated Unit & E2E Testing:**
   - Expanded test suite to **14 passing tests** across `test_runtime.py` and `test_llm_planner.py`.

---

## 📂 Repository Structure (Week 2 Milestone)

```text
agent-reliability-lab/
├── agent/
│   ├── __init__.py
│   ├── runtime.py       # Core loop, execution budgets, step & timeout limits
│   ├── tools.py         # Schema validation (extra="forbid") & allowlist
│   ├── traces.py        # RunTrace and TraceEvent dataclasses with UUID generation
│   ├── model.py         # HTTP adapter for Ollama chat endpoint
│   ├── instructions.py  # System prompts, tool schemas & output formatting rules
│   └── planner.py       # LLMPlanner with conversation & observation memory
├── evals/
│   ├── __init__.py
│   ├── dataset.jsonl    # 10-case evaluation benchmark dataset
│   ├── graders.py       # TaskResultGrader & ToolSelectionGrader
│   └── runner.py        # LLM evaluation runner generating JSON reports
├── reports/             # Generated JSON evaluation execution reports
├── tests/
│   ├── test_runtime.py      # 11 unit & fault-injection harness tests
│   └── test_llm_planner.py  # 3 local LLM integration tests
├── ARCHITECTURE.md      # System invariants & architectural documentation
├── pyproject.toml
└── README.md
