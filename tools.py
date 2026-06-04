from __future__ import annotations

from io import BytesIO
from typing import List
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from langchain_core.tools import tool
from pypdf import PdfReader


def _clean_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    text = " ".join(line for line in lines if line)
    return " ".join(text.split())


@tool
def search_web(query: str) -> str:
    """Search the public web for company information and return top results with URLs."""
    try:
        results: List[dict] = []
        with DDGS() as ddgs:
            for item in ddgs.text(query, max_results=5):
                results.append(
                    {
                        "title": item.get("title", ""),
                        "url": item.get("href", ""),
                        "snippet": item.get("body", ""),
                    }
                )

        if not results:
            return "No search results found."

        lines = []
        for idx, item in enumerate(results, start=1):
            lines.append(f"{idx}. {item['title']}\nURL: {item['url']}\nSnippet: {item['snippet']}")
        return "\n\n".join(lines)
    except Exception as exc:
        return f"Search failed: {exc}"


@tool
def fetch_url(url: str) -> str:
    """Fetch a web page or PDF and return cleaned text for analysis."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return "Invalid URL. Only http and https URLs are supported."

        response = requests.get(
            url,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").lower()
        is_pdf = "pdf" in content_type or parsed.path.lower().endswith(".pdf")

        if is_pdf:
            reader = PdfReader(BytesIO(response.content))
            pages = []
            for page in reader.pages[:5]:
                pages.append(page.extract_text() or "")
            text = _clean_text("\n".join(pages))
            return text[:6000] if text else "PDF could not be read."

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        parts = [title] if title else []

        for tag in soup.find_all(["h1", "h2", "h3", "p", "li"]):
            text = tag.get_text(" ", strip=True)
            if text:
                parts.append(text)

        text = _clean_text("\n".join(parts))
        if not text:
            return "No readable text found on the page."

        return text[:6000]
    except Exception as exc:
        return f"Fetch failed: {exc}"

