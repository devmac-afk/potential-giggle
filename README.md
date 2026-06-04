# AI Company Research Agent

Simple Streamlit app for the AI/ML internship assessment.

## What it does

- Takes a company name as input
- Searches public sources
- Reads relevant webpages or PDFs
- Generates a structured report with:
  - company overview
  - key business information
  - likely challenges
  - AI opportunities
  - CEO-style pitch

## Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your Google Gemini key:

```bash
set GOOGLE_API_KEY=your_key_here
```

3. Start the app:

```bash
streamlit run app.py
```

## Notes

- The app uses one LangChain research agent and two tools: web search and URL fetch.
- It is intentionally simple so it is easy to understand and explain in an interview.
- The model provider is Google Gemini, so you do not need a paid OpenAI API key.
