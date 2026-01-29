"""LangGraph workflow for the advisor."""

import json
from typing import Any, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from advisor.config import MODEL_CONFIG
from advisor.prompts import ADVISOR_PROMPT, REJECTION_MESSAGE, VERIFIER_PROMPT
from advisor.tools import search_accessibility_docs


class AdvisorState(TypedDict):
    """State passed through the workflow."""

    question: str
    is_relevant: bool
    response: str


def _parse_json_response(content: str) -> dict[str, Any]:
    """Extract JSON object from LLM response content."""

    text = content.strip()
    if text.startswith("```"):
        parts = text.split("```")
        if len(parts) > 1:
            text = parts[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    return json.loads(text)


def verify_question(state: AdvisorState) -> AdvisorState:
    """Check if question is relevant."""
    llm = ChatOpenAI(model=MODEL_CONFIG.verifier_model, temperature=0)
    result = llm.invoke(VERIFIER_PROMPT.format(question=state["question"]))

    try:
        data = _parse_json_response(result.content)
        state["is_relevant"] = data.get("is_relevant", False)
    except (json.JSONDecodeError, TypeError):
        state["is_relevant"] = True

    return state


def reject_question(state: AdvisorState) -> AdvisorState:
    """Return rejection message."""

    state["response"] = REJECTION_MESSAGE
    return state


def generate_response(state: AdvisorState) -> AdvisorState:
    """Search documents and generate answer."""

    # Search based on analysis
    search_results = search_accessibility_docs.invoke(state["question"])

    # Generate answer
    llm = ChatOpenAI(model=MODEL_CONFIG.advisor_model, temperature=0)
    result = llm.invoke(
        ADVISOR_PROMPT.format(
            question=state["question"],
            search_results=search_results,
        )
    )

    state["response"] = result.content
    return state


def create_graph():
    """Create the LangGraph workflow.

    Workflow:
    1. verify_question: Check relevance
    2. If relevant → advisor: Search and respond
    3. If not relevant → reject: Return rejection message
    """
    workflow = StateGraph(AdvisorState)

    # Add nodes
    workflow.add_node("verify_question", verify_question)
    workflow.add_node("advisor", generate_response)
    workflow.add_node("reject", reject_question)

    # Entry point
    workflow.set_entry_point("verify_question")

    # Conditional routing based on relevance
    workflow.add_conditional_edges(
        "verify_question",
        lambda state: "advisor" if state["is_relevant"] else "reject",
        {"advisor": "advisor", "reject": "reject"},
    )

    # Terminal edges
    workflow.add_edge("advisor", END)
    workflow.add_edge("reject", END)

    return workflow.compile()
