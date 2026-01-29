# Canadian Accessibility Advisor

A lightweight multi-agent Q&A tool that helps developers and business owners understand Canadian accessibility laws and WCAG compliance requirements.

## Why This Exists

Canadian accessibility requirements vary by jurisdiction, such as federal requirements under the Accessible Canada Act (ACA) and provincial requirements like Ontario’s AODA, each with different rules and WCAG levels. This tool answers plain-language questions so you don't have to read legal documents.

## What It Does

- Explains Canadian accessibility legislation (ACA, AODA, provincial summaries)
- Clarifies WCAG standards and compliance levels
- Highlights jurisdiction-specific requirements

## How It Works

```
User Question
     ↓
[Verifier] → Off-topic? → Polite rejection
     ↓
    On-topic
     ↓
[RAG Search] → FAISS retrieves relevant passages
     ↓
[Advisor] → Generates cited response
```

## Tech Stack

- **Language**: Python 3.13
- **Agent Framework**: LangGraph + LangChain
- **Vector Store**: FAISS (local)
- **LLMs**: OpenAI `gpt-5-nano` (Verifier), `gpt-5-mini` (Advisor)
- **Embeddings**: OpenAI `text-embedding-3-small`
- **UI**: Streamlit

Built with LangGraph for clean state management.

## Quick Start

```bash
# Install
poetry install

# Configure
cp .env.example .env
# Edit .env and set OPENAI_API_KEY

# Run
poetry run streamlit run src/advisor/app.py
```

## Sample Questions

- What laws apply to federally regulated businesses?
- Does Alberta have web accessibility laws?
- Who needs to comply with AODA?
- WCAG 2.0 vs 2.1?
- What WCAG level does Canada require?

## Project Structure

```
├── src/advisor/
│   ├── app.py          # Streamlit UI
│   ├── graph.py        # LangGraph workflow
│   ├── prompts.py      # System prompts
│   ├── tools.py        # RAG search tool
│   ├── vectorstore.py  # FAISS index management
│   └── config.py       # Model configuration
├── docs/               # RAG document corpus
└── data/               # FAISS index (auto-generated)
```

## Updating Documents

Docs live in `docs/`. To rebuild the index:

```bash
rm -rf data/faiss_index/
poetry run streamlit run src/advisor/app.py
```

## Disclaimer

This tool provides general information about Canadian accessibility laws and is not legal advice. Consult a qualified legal professional for specific compliance questions.
