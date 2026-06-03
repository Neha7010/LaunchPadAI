from models.profile_schema import StudentProfile
from services.gemini_service import generate_structured_data
from typing import Dict, Any

PROFILE_SYSTEM_INSTRUCTION = """
You are a career and academic advisor assistant. Your task is to process raw student descriptions, resume text, or profile forms, and extract a clean, structured JSON student profile.
- Standardize language names (e.g. 'js' -> 'JavaScript', 'py' -> 'Python').
- Standardize interests and career goals into neat, readable titles.
- Fill in missing fields with sensible inferences if possible (e.g., if major is 'CS' and interests are neural networks, career goal could be 'AI Engineer').
"""

def extract_profile(raw_text: str, api_key: str) -> StudentProfile:
    """Uses Gemini to extract a structured StudentProfile from raw text input."""
    prompt = f"Extract a student profile from the following details:\n\n{raw_text}"
    return generate_structured_data(
        prompt=prompt,
        schema=StudentProfile,
        api_key=api_key,
        system_instruction=PROFILE_SYSTEM_INSTRUCTION
    )

def standardize_form_profile(form_data: Dict[str, Any], api_key: str) -> StudentProfile:
    """Uses Gemini to standardize and clean up raw manual text entries from form inputs."""
    # Convert lists to strings for the prompt
    skills_str = ", ".join(form_data.get("skills", [])) if isinstance(form_data.get("skills"), list) else str(form_data.get("skills", ""))
    interests_str = ", ".join(form_data.get("interests", [])) if isinstance(form_data.get("interests"), list) else str(form_data.get("interests", ""))
    
    raw_summary = f"""
    Name: {form_data.get('name', 'Student')}
    Major: {form_data.get('major', 'General Studies')}
    Skills/Technologies: {skills_str}
    Interests/Domains: {interests_str}
    Target Career Goal: {form_data.get('career_goal', 'Software Engineer')}
    """
    
    return extract_profile(raw_summary, api_key)
