# Japanese Greeting Agent

A conversational AI agent that greets users in Japanese.

## Business challenge

Users need an AI agent capable of greeting them accurately in Japanese, enabling natural and culturally appropriate communication.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Japanese greeting accuracy | — | 100% | — | Customer Engagement / Conversational AI | user |

## Key Milestones

1. **Agent scaffolded** — Python A2A agent project initialized with greeting capability defined in system prompt.
2. **Japanese greeting functional** — Agent responds correctly with "こんにちは" (and variants) to user greetings.
3. **Agent deployed** — Agent running and accessible via the SAP Joule Studio runtime.

## Business Architecture (RBA)

### End-to-End Process

Lead to Cash (generic)

### Process Hierarchy

```
Lead to Cash (generic)
└── Manage Customers and Channels (generic)
    └── Manage customers (generic) [BPS-370]
        └── Manage customer experience
```

### Summary

Greeting users in Japanese maps to the "Manage customer experience" business activity within the Lead to Cash E2E, covering customer engagement and interaction at digital touchpoints.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|------------------------|------------|-------------------|--------------------|--------------------|---------------------|------|---------------------|
| Greet users in Japanese via conversational AI | None — all discovered APIs unavailable in landscape | — | — | — | — | — | Yes | Full custom AI agent required; no standard SAP asset available |

### Key findings

- No standard SAP product directly covers a Japanese-language greeting AI agent use case.
- All discovered conversation/bot APIs are unavailable in the current landscape.
- A custom Python-based AI agent (A2A protocol) is the appropriate solution.
- The agent requires no external MCP tool integrations — greeting logic is handled via the LLM system prompt.
- Deployment target is SAP Joule Studio runtime (SAP AI Core).

## Recommendations

### Japanese Greeting AI Agent

#### Executive Summary

Custom Python A2A agent greeting users in Japanese via LLM.

#### Recommended Solution

Build a lightweight Python AI agent using the A2A protocol on SAP AI Core. The agent's system prompt instructs it to greet users in Japanese (e.g., "こんにちは", "はじめまして") and respond naturally to greetings. No external tool integrations are needed.

#### Recommended solution category

AI Agent

#### Intent fit
95%
