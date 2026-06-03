from pydantic import BaseModel, Field
from typing import List

class StudentProfile(BaseModel):
    name: str = Field(..., description="The student's name")
    major: str = Field(..., description="The student's academic major/field of study")
    skills: List[str] = Field(default_factory=list, description="List of technical skills, programming languages, frameworks, or tools")
    interests: List[str] = Field(default_factory=list, description="List of fields or topics the student is interested in (e.g. Finance, Healthcare, Cyber Security, Games)")
    career_goal: str = Field(..., description="The student's target role or career goal (e.g. AI Engineer, Full-Stack Developer, Data Analyst)")
