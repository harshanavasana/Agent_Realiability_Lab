# Agent Reliability Lab (ARL) — System Architecture

## 1. High-Level Flow
Task → Planner → Input Schema Validation → Tool Registry Allowlist → Tool Execution → Event Trace → Deterministic Grader

## 2. Invariants & Guardrails
- **Input Validation**: Pydantic models with `extra="forbid"` prevent malformed LLM tool arguments from reaching execution functions.
- **Tool Allowlist**: `get_tool()` enforces strict lookups; unauthorized tools throw immediate runtime errors.
- **Execution Budgets**: Bounded by `max_steps` (default: 5) and `timeout_seconds` (default: 30.0s).
- **Structured Observability**: Every execution emits standard UUID-tagged `TraceEvent` objects inside a `RunTrace`.

## 3. Evaluation Principles
- **Separation of Concerns**: Test cases explicitly define expected outputs and authorized tool calls separately.
- **Grading Matrix**: `TaskResultGrader` evaluates output correctness AND tool authorization compliance independently.