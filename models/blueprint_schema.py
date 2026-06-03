from pydantic import BaseModel, Field
from typing import List, Optional

class ImplementationPhase(BaseModel):
    phase_name: str = Field(..., description="Name of the phase, e.g., 'Phase 1: Database Setup and Basic API'")
    duration: str = Field(..., description="Duration or week marker, e.g., 'Week 1'")
    tasks: List[str] = Field(..., description="Detailed technical tasks for this week/phase")

class ProjectBlueprint(BaseModel):
    project_title: str = Field(..., description="The recommended project title")
    problem_statement: str = Field(..., description="Clear problem statement explaining what the project solves")
    why_recommended: List[str] = Field(
        ..., 
        description="Detailed bullet points explaining why this project is recommended based on the student's skills, interests, career goal, and market context."
    )
    key_features: List[str] = Field(..., description="3 to 5 core features of the project")
    suggested_technologies: List[str] = Field(..., description="A complete list of technologies, frameworks, libraries, databases, and deployment platforms to be used.")
    architecture_description: str = Field(..., description="Short explanation of how the frontend, backend, database, and AI models interact.")
    text_architecture_diagram: str = Field(
        ..., 
        description="A text-based or ASCII flow diagram showing the software components (e.g. User Interface -> FastAPI Gateway -> PostgreSQL DB)."
    )
    implementation_phases: List[ImplementationPhase] = Field(
        ..., 
        description="A weekly roadmap containing exactly 4 phases (Week 1, Week 2, Week 3, Week 4) with detailed tasks."
    )
    estimated_hardware: Optional[List[str]] = Field(
        default_factory=list, 
        description="List of hardware components, microcontrollers, or physical accessories required, if any. Leave empty if none are required."
    )
    novelty_factors: List[str] = Field(
        ..., 
        description="Factors explaining the novelty of the project, including existing competition, tech uniqueness, and industry relevance."
    )
