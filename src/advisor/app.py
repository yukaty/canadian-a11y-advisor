"""Streamlit chat interface for the Canadian Accessibility Advisor."""

import streamlit as st
from dotenv import load_dotenv

from advisor.graph import create_graph

SAMPLE_QUESTIONS = [
    "What laws apply to federally regulated businesses?",
    "Does Alberta have web accessibility laws?",
    "Who needs to comply with AODA?",
    "WCAG 2.0 vs 2.1?",
    "What WCAG level does Canada require?",
]


def _init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "graph" not in st.session_state:
        with st.spinner("Initializing advisor..."):
            st.session_state.graph = create_graph()


def _run_graph(prompt: str) -> str:
    initial_state = {
        "question": prompt,
        "is_relevant": False,
        "response": "",
    }

    try:
        result = st.session_state.graph.invoke(initial_state)
        return result["response"]
    except Exception as e:
        return f"An error occurred: {str(e)}\n\nPlease try rephrasing your question."


load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Canadian Accessibility Advisor", page_icon="🍁", layout="centered"
)

st.title("Canadian Accessibility Advisor 🍁")
st.caption("Get answers about Canadian accessibility laws and WCAG compliance")

# Legal disclaimer
st.warning(
    "This tool provides general information about Canadian accessibility laws and is not legal advice. Consult a qualified legal professional for specific compliance questions."
)

_init_session_state()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sample questions in sidebar
with st.sidebar:
    st.header("Sample Questions")
    st.markdown("Try asking:")
    for question in SAMPLE_QUESTIONS:
        st.markdown(f"- {question}")

    st.divider()

    if st.button("Clear Chat History", icon=":material/delete:"):
        st.session_state.messages = []
        st.rerun()


# Chat input
if prompt := st.chat_input("Ask about Canadian accessibility laws..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from graph
    with st.chat_message("assistant"):
        with st.spinner("Analyzing question..."):
            response = _run_graph(prompt)

        st.markdown(response)

    # Add assistant response to chat
    st.session_state.messages.append({"role": "assistant", "content": response})
