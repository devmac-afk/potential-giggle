from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv

from agent import build_company_report


load_dotenv()

st.set_page_config(
    page_title="Unada AI Company Research Agent",
    page_icon="🤖",
    layout="wide",
)


def render_report(result):
    report = result.report

    st.subheader("Company Overview")
    st.write(report.company_overview)

    st.subheader("Key Business Information")
    for item in report.key_business_information:
        st.markdown(f"- {item}")

    st.subheader("Potential Business Challenges")
    for item in report.potential_business_challenges:
        st.markdown(f"**{item.challenge}**")
        st.write(item.reasoning)

    st.subheader("AI Opportunities")
    for item in report.ai_opportunities:
        st.markdown(f"**{item.opportunity}**")
        st.write(f"Reasoning: {item.reasoning}")
        st.write(f"Expected impact: {item.expected_impact}")

    st.subheader("Personalized Pitch")
    st.write(report.personalized_pitch)

    st.subheader("Sources")
    for source in report.sources:
        st.markdown(f"- [{source.title}]({source.url})")
        st.caption(source.note)

    with st.expander("Show research notes"):
        st.write(result.research_notes)


def main():
    st.title("Unada AI-Powered Company Research & Recommendation Agent")
    st.write(
        "Enter a company name and the app will research public information, identify likely challenges, "
        "suggest AI opportunities, and write a short CEO-style pitch."
    )

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        st.warning("GROQ_API_KEY is not set. Add it to your environment or .env file before running the app.")

    with st.form("company_form"):
        company_name = st.text_input("Company name", placeholder="e.g. Sobha, Brigade Group, Adani Realty")
        submitted = st.form_submit_button("Generate Report")

    if submitted:
        if not company_name.strip():
            st.error("Please enter a company name.")
            return

        with st.spinner("Researching the company and building the report..."):
            try:
                result = build_company_report(company_name.strip())
            except Exception as exc:
                st.error(f"Could not generate report: {exc}")
                return

        render_report(result)


if __name__ == "__main__":
    main()
