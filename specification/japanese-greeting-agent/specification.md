# Specification: japanese-greeting-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [ ] Read the project input (`product-requirements-document.md`, `intent.md`)
- [ ] Bootstrap agent code in `assets/japanese-greeting-agent/` using instructions from the sap-agent-bootstrap section. (invoke from inside `assets/japanese-greeting-agent/`, use copy commands — do NOT create files manually)
- [ ] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

No runtime skills needed — greeting logic is simple enough to live in the system prompt.

---

## Project-Specific Tasks

## System Prompt: Japanese Greeting Behaviour

- [ ] Open `assets/japanese-greeting-agent/app/agent.py` and update the system prompt (`get_system_prompt`) to instruct the agent to:
  - Always greet the user in Japanese (e.g., こんにちは, はじめまして, やあ)
  - Use formal Japanese (はじめまして, こんにちは) for first greetings or polite contexts
  - Use casual Japanese (やあ, どうも) for informal contexts
  - If the user's input is unrecognised, respond politely in Japanese asking for clarification
  - Never respond with greetings in any language other than Japanese for greeting interactions
  - Add guardrail: agent only handles greetings; for off-topic questions, politely redirect in Japanese

## R1 – Japanese Greeting Response

- [ ] Verify the agent responds to English greetings ("hi", "hello", "hey") with a Japanese greeting (e.g., "こんにちは！")
- [ ] Verify the agent responds to Japanese greetings ("こんにちは") with a natural Japanese reply
- [ ] Verify the agent responds to casual greetings with casual Japanese

## R2 – Greeting Variety

- [ ] Verify the agent uses `はじめまして` for first-meeting / formal contexts
- [ ] Verify the agent uses `こんにちは` for standard daytime greetings
- [ ] Verify the agent uses `やあ` or `どうも` for casual contexts

## R3 – Graceful Fallback

- [ ] Verify the agent responds politely in Japanese when it receives an unrecognised input
- [ ] Add hardcoded fallback greeting `"こんにちは！"` for when the LLM is unavailable (in error handling path)

---

## Business Instrumentation

- [ ] Implement business step instrumentation for each milestone from the PRD:
  - **M1** — `M1.achieved: agent scaffolded with Japanese greeting system prompt` / `M1.missed: agent scaffolding did not complete`
  - **M2** — `M2.achieved: Japanese greeting response validated` / `M2.missed: Japanese greeting response not produced`
  - **M3** — `M3.achieved: agent deployed and responding on SAP AI Core` / `M3.missed: agent deployment did not complete`
- [ ] Add OpenTelemetry custom spans for each milestone using the context manager form inside plain async helpers (not inside async generators)
- [ ] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## MCP Tool Integration

No MCP tools required — this agent has no SAP API integrations. Skip all MCP steps.

---

## Testing

- [ ] `conftest.py` only sets `IBD_TESTING=true`
- [ ] Write unit tests in `assets/japanese-greeting-agent/tests/`:
  - `test_greeting_japanese.py` — mock LLM, assert Japanese greeting returned for "hi", "hello", "こんにちは"
  - `test_fallback.py` — assert polite Japanese response for unrecognised input
- [ ] Write one integration test: end-to-end agent flow with mocked LLM, asserting Japanese greeting in response
- [ ] Run `pytest` from `assets/japanese-greeting-agent/` (no args)
- [ ] If coverage < 70%, add tests until threshold met
- [ ] Run `pytest` again from `assets/japanese-greeting-agent/` (no args) to generate final `test_report.json`
- [ ] Verify `test_report.json` exists in `assets/japanese-greeting-agent/`
