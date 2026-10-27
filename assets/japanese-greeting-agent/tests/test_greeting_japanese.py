"""Tests for Japanese greeting responses (R1 & R2)."""
from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

JAPANESE_GREETINGS = [
    "こんにちは",
    "はじめまして",
    "やあ",
    "どうも",
    "おはようございます",
    "こんばんは",
]


def _contains_japanese(text: str) -> bool:
    """Return True if the text contains at least one Japanese character."""
    return any(
        "\u3000" <= c <= "\u9fff" or "\u30a0" <= c <= "\u30ff" or "\u3040" <= c <= "\u309f"
        for c in text
    )


def _make_mock_result(content: str):
    """Build a mock LangGraph ainvoke result."""
    msg = MagicMock()
    msg.content = content
    return {"messages": [msg]}


# ---------------------------------------------------------------------------
# R1 — Japanese Greeting Response
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_english_hi_returns_japanese_greeting(add_agent_to_path):
    """'hi' should produce a response containing Japanese characters."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_agent") as mock_create, \
         patch("agent.create_checkpointer"):
        mock_graph = AsyncMock()
        mock_graph.ainvoke.return_value = _make_mock_result("こんにちは！(Konnichiwa!)")
        mock_create.return_value = mock_graph

        from agent import SampleAgent
        agent = SampleAgent()
        resp = await agent.invoke("hi", "ctx-1")

    assert resp.status == "completed"
    assert _contains_japanese(resp.message), (
        f"Expected Japanese characters in response, got: {resp.message}"
    )


@pytest.mark.asyncio
async def test_english_hello_returns_japanese_greeting(add_agent_to_path):
    """'hello' should produce a response containing Japanese characters."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_agent") as mock_create, \
         patch("agent.create_checkpointer"):
        mock_graph = AsyncMock()
        mock_graph.ainvoke.return_value = _make_mock_result("こんにちは！(Konnichiwa!)")
        mock_create.return_value = mock_graph

        from agent import SampleAgent
        agent = SampleAgent()
        resp = await agent.invoke("hello", "ctx-2")

    assert resp.status == "completed"
    assert _contains_japanese(resp.message)


@pytest.mark.asyncio
async def test_japanese_greeting_returns_natural_reply(add_agent_to_path):
    """'こんにちは' should produce a natural Japanese reply."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_agent") as mock_create, \
         patch("agent.create_checkpointer"):
        mock_graph = AsyncMock()
        mock_graph.ainvoke.return_value = _make_mock_result("こんにちは！お元気ですか？(Konnichiwa! Ogenki desu ka?)")
        mock_create.return_value = mock_graph

        from agent import SampleAgent
        agent = SampleAgent()
        resp = await agent.invoke("こんにちは", "ctx-3")

    assert resp.status == "completed"
    assert _contains_japanese(resp.message)


@pytest.mark.asyncio
async def test_casual_greeting_hey_returns_casual_japanese(add_agent_to_path):
    """'hey' should produce a casual Japanese greeting (やあ or どうも)."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_agent") as mock_create, \
         patch("agent.create_checkpointer"):
        mock_graph = AsyncMock()
        mock_graph.ainvoke.return_value = _make_mock_result("やあ！(Yaa!)")
        mock_create.return_value = mock_graph

        from agent import SampleAgent
        agent = SampleAgent()
        resp = await agent.invoke("hey", "ctx-4")

    assert resp.status == "completed"
    assert _contains_japanese(resp.message)


# ---------------------------------------------------------------------------
# R2 — Greeting Variety
# ---------------------------------------------------------------------------


def test_system_prompt_includes_hajimemashite(add_agent_to_path):
    """System prompt should mention はじめまして for first-meeting contexts."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    assert "はじめまして" in prompt


def test_system_prompt_includes_konnichiwa(add_agent_to_path):
    """System prompt should mention こんにちは for standard daytime greetings."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    assert "こんにちは" in prompt


def test_system_prompt_includes_casual_greeting(add_agent_to_path):
    """System prompt should mention やあ or どうも for casual contexts."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    assert "やあ" in prompt or "どうも" in prompt
