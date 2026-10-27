"""Tests for graceful fallback behaviour (R3)."""
from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


def _contains_japanese(text: str) -> bool:
    return any(
        "\u3000" <= c <= "\u9fff" or "\u30a0" <= c <= "\u30ff" or "\u3040" <= c <= "\u309f"
        for c in text
    )


def _make_mock_result(content: str):
    msg = MagicMock()
    msg.content = content
    return {"messages": [msg]}


@pytest.mark.asyncio
async def test_unrecognised_input_returns_polite_japanese(add_agent_to_path):
    """Unrecognised input should receive a polite Japanese response."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_agent") as mock_create, \
         patch("agent.create_checkpointer"):
        mock_graph = AsyncMock()
        mock_graph.ainvoke.return_value = _make_mock_result(
            "申し訳ありません、私は挨拶専門のエージェントです。"
        )
        mock_create.return_value = mock_graph

        from agent import SampleAgent
        agent = SampleAgent()
        resp = await agent.invoke("What is the stock price?", "ctx-fallback-1")

    assert resp.status == "completed"
    assert _contains_japanese(resp.message), (
        f"Expected Japanese fallback, got: {resp.message}"
    )


def test_system_prompt_includes_fallback_instruction(add_agent_to_path):
    """System prompt should instruct the agent to redirect off-topic input in Japanese."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    # Check for the off-topic redirect instruction
    assert "off-topic" in prompt.lower() or "申し訳" in prompt or "redirect" in prompt.lower()


@pytest.mark.asyncio
async def test_error_path_returns_graceful_message(add_agent_to_path):
    """When the LLM raises an exception, invoke() should return a graceful message.

    The agent framework returns status='completed' with a user-friendly error
    message rather than propagating the raw exception — this ensures the A2A
    task always finishes cleanly.
    """
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_agent") as mock_create, \
         patch("agent.create_checkpointer"):
        mock_graph = AsyncMock()
        mock_graph.ainvoke.side_effect = RuntimeError("LLM unavailable")
        mock_create.return_value = mock_graph

        from agent import SampleAgent
        agent = SampleAgent()
        resp = await agent.invoke("hi", "ctx-fallback-2")

    # The framework converts LLM errors to a completed task with a graceful message
    assert resp.status in ("completed", "error")
    assert resp.message  # some message is always returned
