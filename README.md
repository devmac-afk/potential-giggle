# AI Company Research Agent

A Streamlit-based web application built for an AI/ML internship assessment. It acts as an autonomous AI agent that researches a given company, identifies business challenges, and proposes tailored AI opportunities.

---

## 1. Approach
The goal of this project was to build a reliable and autonomous "Two-Step" AI agent capable of gathering unstructured data from the web and formatting it into a highly structured business report. 
- **Phase 1 (The Researcher):** The application uses an LLM equipped with tools to search the web and scrape content. It autonomously decides what to search and which links to click.
- **Phase 2 (The Consultant):** The application passes the raw, messy research notes to a second prompt, which forces the LLM to output a strictly typed JSON structure (using Pydantic) matching the required business report format.

## 2. Architecture
The architecture follows a modern LangGraph Agent loop integrated with a Streamlit frontend:
- **Frontend Layer:** `app.py` (Streamlit) handles the user interface, input forms, and renders the final structured output in a clean dashboard.
- **Agent/Routing Layer:** `agent.py` leverages `langgraph.prebuilt.create_react_agent`. The graph handles the cyclic execution (Thought -> Action -> Observation) allowing the LLM to recursively search and read until it is satisfied.
- **Tools Layer:** `tools.py` provides the API capabilities (`duckduckgo-search` for web indexing, and `requests` + `BeautifulSoup`/`pypdf` for text extraction).
- **Data Enforcement Layer:** `schemas.py` uses `Pydantic` to enforce the exact schema (Opportunities, Challenges, Pitch) the LLM must return.

## 3. AI Tools & Libraries Used
- **LLM Provider:** Groq API (`llama-3.3-70b-versatile`) - Used for its incredibly fast inference speeds and generous API rate limits.
- **LangChain & LangGraph:** Used as the orchestration framework for building the agent loop, managing conversation state, and standardizing tool calling.
- **DuckDuckGo Search:** Used as a free, unauthenticated search engine API to allow the agent to find current company links.
- **BeautifulSoup4 & PyPDF:** Used to parse raw HTML and PDF documents into clean, readable text for the LLM context window.
- **Pydantic:** Used to enforce JSON schema validation on the LLM's final output.

## 4. Challenges Faced
1. **API Rate Limits (HTTP 429):** Initially, the project was built using Google's Gemini models. Because ReAct agents run in a continuous loop (making multiple LLM calls per user request), the agent quickly exhausted the Free Tier limits (5 requests per minute), causing the app to crash.
2. **Library Deprecations:** LangChain recently underwent a massive architectural change. Legacy methods like `AgentExecutor` were completely removed, causing `ModuleNotFound` and `ImportError` issues during deployment.
3. **Environment Security:** Ensuring that sensitive API keys were not exposed when pushing code to public GitHub repositories or deploying to Streamlit Cloud.

## 5. How Challenges Were Solved
1. **Migrating to Groq:** To solve the rate limit issues, the LLM provider was completely swapped to **Groq** using the `llama-3.3-70b-versatile` model. Groq provides significantly faster token generation and a much more generous free tier, allowing the agent to loop freely without exhausting quota.
2. **Adopting LangGraph:** The codebase was refactored to replace the deprecated `AgentExecutor` with the modern `create_react_agent` from the `langgraph` library. This future-proofed the code and solved the import errors on the cloud environment.
3. **Secrets Management:** A `.gitignore` file was introduced to prevent the local `.env` file from being tracked. On deployment, Streamlit Cloud's built-in "Secrets Management" dashboard was used to inject the `GROQ_API_KEY` directly into the cloud environment safely.

---

## Run Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your Groq key in a `.env` file:
```env
GROQ_API_KEY=your_key_here
```

3. Start the app:
```bash
streamlit run app.py
```
