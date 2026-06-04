from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class SourceItem(BaseModel):
    title: str = Field(..., description="Readable title of the source")
    url: str = Field(..., description="Public URL of the source")
    note: str = Field(..., description="Why this source is relevant")


class ChallengeItem(BaseModel):
    challenge: str = Field(..., description="Likely business challenge")
    reasoning: str = Field(..., description="Why this challenge is likely")


class OpportunityItem(BaseModel):
    opportunity: str = Field(..., description="Specific AI opportunity")
    reasoning: str = Field(..., description="Why this fits the company")
    expected_impact: str = Field(..., description="Practical business impact")


class ReportOutput(BaseModel):
    company_overview: str = Field(..., description="Short summary of the company")
    key_business_information: List[str] = Field(
        ..., description="Main offerings, recent developments, and expansion details"
    )
    potential_business_challenges: List[ChallengeItem] = Field(
        ..., description="Likely challenges backed by reasoning"
    )
    ai_opportunities: List[OpportunityItem] = Field(
        ..., description="Company-specific AI recommendations"
    )
    personalized_pitch: str = Field(
        ..., description="One-page CEO-style pitch written in business language"
    )
    sources: List[SourceItem] = Field(
        ..., description="Public sources used for research"
    )

