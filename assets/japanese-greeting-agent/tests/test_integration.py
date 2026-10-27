"""Integration test: end-to-end agent flow with mocked LLM."""
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
async def test_end_to_end_japanese_greeting(add_agent_to_path):
    """End-to-end: user says 'hello', agent returns a Japanese greeting.

    The entire LLM stack is mocked so no real API calls are made.
    """
    expected_response = "こんにちは！(Konnichiwa!) はじめまして！(Hajimemashite!)"

    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_agent") as mock_create, \
         patch("agent.create_checkpointer"), \
         patch("agent.SummarizationMiddleware"):
        mock_graph = AsyncMock()
        mock_graph.ainvoke.return_value = _make_mock_result(expected_response)
        mock_create.return_value = mock_graph

        from agent import SampleAgent
        agent = SampleAgent()

        # Act
        resp = await agent.invoke("hello", "integration-ctx-1")

    # Assert
    assert resp.status == "completed", f"Expected 'completed', got '{resp.status}'"
    assert _contains_japanese(resp.message), (
        f"Expected Japanese characters in response, got: {resp.message}"
    )
    assert "こんにちは" in resp.message or "はじめまして" in resp.message, (
        f"Expected formal Japanese greeting in response, got: {resp.message}"
    )


@pytest.mark.asyncio
async def test_end_to_end_system_prompt_integrity(add_agent_to_path):
    """System prompt must contain all required Japanese greeting variations."""
    from agent import get_system_prompt
    prompt = get_system_prompt()

    required = ["こんにちは", "はじめまして", "やあ", "おはようございます", "こんばんは"]
    missing = [g for g in required if g not in prompt]
    assert not missing, f"System prompt missing greetings: {missing}"
