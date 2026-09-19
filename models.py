from typing import List, Optional
from pydantic import BaseModel, Field


# =========================================================
# STUDENT PROFILE
# =========================================================

class StudentProfile(BaseModel):

    skills: List[str] = Field(default_factory=list)

    certificates: List[str] = Field(default_factory=list)

    projects: List[str] = Field(default_factory=list)

    achievements: List[str] = Field(default_factory=list)

    interests: List[str] = Field(default_factory=list)

    education: Optional[str] = ""

    experience: Optional[str] = ""


# =========================================================
# RECOMMENDATION
# =========================================================

class Recommendation(BaseModel):

    title: str

    company: str

    match_score: float

    type: str

    location: str

    description: str

    matched_skills: List[str]

    missing_skills: List[str]

    eligibility: str

    link: str


# =========================================================
# API RESPONSE
# =========================================================

class RecommendationResponse(BaseModel):

    success: bool

    count: int

    recommendations: List[Recommendation]