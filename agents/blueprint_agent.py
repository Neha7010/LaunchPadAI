from typing import List, Dict, Any
from pydantic import BaseModel, Field
from models.blueprint_schema import ProjectBlueprint
from services.gemini_service import generate_structured_data

class RecommendationsList(BaseModel):
    recommendations: List[ProjectBlueprint] = Field(
        ..., 
        description="A list of exactly three recommended projects tailored to the student's profile."
    )

BLUEPRINT_SYSTEM_INSTRUCTION = """
You are an expert academic mentor and AI software architect. Your job is to analyze a student's profile (name, major, skills, interests, career goal) and retrieved web research context snippets, then recommend exactly THREE distinct projects.

For each project, generate a detailed blueprint matching the ProjectBlueprint schema:
1. 'project_title': Unique, eye-catching title indicating technical depth.
2. 'problem_statement': Clear description of what the project solves.
3. 'why_recommended': Mandatory bullet points explaining exactly why this project fits the student's skills, interests, career goals, and the retrieved research context.
4. 'key_features': 3-5 core functionalities.
5. 'suggested_technologies': Python libraries, frontend frameworks, backend microservices, database, and deployment platforms (e.g. PyTorch, FastAPI, Streamlit, PostgreSQL, Docker, HF Spaces).
6. 'architecture_description': Brief text summarizing the architectural flow.
7. 'text_architecture_diagram': Text-based flow or ASCII diagram indicating communication flow (e.g., UI [Streamlit] -> backend [FastAPI] -> ML inference [PyTorch] -> SQLite database).
8. 'implementation_phases': Exactly 4 weekly phases detailing tasks for Week 1, Week 2, Week 3, and Week 4.
9. 'estimated_hardware': Optional hardware (e.g. ESP32, sensors) if the project has embedded elements. Otherwise, leave empty.
10. 'novelty_factors': 2-3 factors outlining industry relevance, existing competition, and unique elements.

Make sure the projects represent varying complexity (e.g. one web-focused, one machine learning-heavy, one domain-specific IoT/data analytics) based on the student's background.
"""

def generate_project_recommendations(
    profile: Dict[str, Any], 
    retrieved_context: List[str], 
    api_key: str
) -> List[ProjectBlueprint]:
    """
    Generates three structured project recommendations based on student profile 
    and web retrieval context snippets.
    """
    context_str = "\n".join([f"- {c}" for c in retrieved_context]) if retrieved_context else "No external context retrieved."
    
    prompt = f"""
    Student Profile:
    - Name: {profile.get('name', 'Student')}
    - Major: {profile.get('major', 'General')}
    - Technical Skills: {', '.join(profile.get('skills', []))}
    - Interests: {', '.join(profile.get('interests', []))}
    - Career Goal: {profile.get('career_goal', 'Software Developer')}

    Retrieved Research Context (Research-Augmented Project Generation):
    {context_str}

    Based on the profile and context above, generate exactly THREE tailored project recommendations.
    """
    
    try:
        result = generate_structured_data(
            prompt=prompt,
            schema=RecommendationsList,
            api_key=api_key,
            system_instruction=BLUEPRINT_SYSTEM_INSTRUCTION
        )
        return result.recommendations
    except Exception as e:
        # Re-raise to let UI handle errors
        raise e
