from __future__ import annotations

from dataclasses import dataclass

from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


from schemas import ReportOutput
from tools import fetch_url, search_web


@dataclass
class CompanyReportBundle:
    research_notes: str
    report: ReportOutput


def _research_agent(llm: ChatGroq):
    system_message = """
                You are a careful company research analyst.
                Use the available tools to gather public information about a company.
                Prefer official company sources, annual reports, investor pages, and credible news.
                Do not invent facts.
                Collect enough information to support a later business analysis.
                When finished, write concise research notes with bullet points for:
                1) company overview
                2) key business information
                3) recent developments
                4) likely challenges
                5) source URLs used
                
                """

    tools = [search_web, fetch_url]
    agent = create_react_agent(llm, tools=tools, prompt=system_message)
    return agent


def build_company_report(company_name: str, model_name: str = "llama-3.3-70b-versatile") -> CompanyReportBundle:
    llm = ChatGroq(model=model_name, temperature=0.2)
    research_executor = _research_agent(llm)
    research_result = research_executor.invoke({"messages": [("user", f"Research the company: {company_name}")]})
    research_notes = research_result["messages"][-1].content

    report_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a business consultant writing a structured intelligence report.
                Use only the research notes provided.
                Do not invent facts. If something is uncertain, use wording like 'likely' or 'possible'.
                Make the recommendations practical and company-specific.
                Return the answer in the requested structured format.
                
                """,
            ),
            (
                "human",
                """
                Company name: {company_name}
                Research notes: {research_notes}
                Create the final report with:
                - company_overview
                - key_business_information
                - potential_business_challenges
                - ai_opportunities
                - personalized_pitch
                - sources
                Keep the pitch to about one page.
                
                """,
            ),
        ]
    )

    report_chain = report_prompt | llm.with_structured_output(ReportOutput)
    report = report_chain.invoke(
        {
            "company_name": company_name,
            "research_notes": research_notes,
        }
    )

    return CompanyReportBundle(research_notes=research_notes, report=report)
