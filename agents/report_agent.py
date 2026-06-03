from typing import Dict, Any
from services.gemini_service import generate_text

REPORT_SYSTEM_INSTRUCTION = """
You are a senior technical writer and computer science professor. Your job is to expand a structured project blueprint into a comprehensive, publication-quality academic project report.
Ensure the report uses formal, professional language and is organized into clear markdown headers.
Avoid placeholders; write detailed descriptions for each section.
"""

def generate_long_form_report(
    profile: Dict[str, Any], 
    blueprint: Dict[str, Any], 
    api_key: str
) -> str:
    """
    Expands a project blueprint into a comprehensive project report.
    """
    prompt = f"""
    Generate a long-form academic project report based on the following details:

    Student Profile:
    - Name: {profile.get('name', 'Student')}
    - Major: {profile.get('major', 'General')}
    - Target Career Goal: {profile.get('career_goal', 'Software Developer')}

    Project Blueprint Details:
    - Title: {blueprint.get('project_title')}
    - Problem Statement: {blueprint.get('problem_statement')}
    - Why Recommended: {", ".join(blueprint.get('why_recommended', []))}
    - Key Features: {", ".join(blueprint.get('key_features', []))}
    - Suggested Technologies: {", ".join(blueprint.get('suggested_technologies', []))}
    - Architecture Description: {blueprint.get('architecture_description')}
    - Text Architecture Diagram:
    ```
    {blueprint.get('text_architecture_diagram')}
    ```
    - Novelty Factors: {", ".join(blueprint.get('novelty_factors', []))}

    Your output report MUST contain the following sections in Markdown:
    
    # PROJECT REPORT: [Insert Project Title Here]
    
    ## 1. ABSTRACT
    A formal 150-250 word summary of the project, including the problem addressed, the proposed system, and key technological findings.
    
    ## 2. INTRODUCTION & BACKGROUND
    A deep dive into the problem background. Cite standard industry challenges and current trends based on the technologies recommended.
    
    ## 3. OBJECTIVES & REQUIREMENTS
    Clear objectives of the system. Split into Functional Requirements and Non-Functional Requirements (Performance, Security, Reliability).
    
    ## 4. METHODOLOGY & TECH STACK
    Explain why this particular technology stack ({", ".join(blueprint.get('suggested_technologies', []))}) was selected. Detail how these technologies cooperate to achieve the goals.
    
    ## 5. SYSTEM ARCHITECTURE
    Explain the software architecture and communication flow. Discuss data ingestion, processing, AI inference, and rendering layers. Describe the relationship of elements shown in the architecture flow:
    {blueprint.get('architecture_description')}
    
    ## 6. IMPLEMENTATION ROADMAP
    Provide a weekly development schedule. Give specific actions, milestones, and testing tasks for:
    - Week 1
    - Week 2
    - Week 3
    - Week 4
    
    ## 7. RESUME IMPACT & BULLET POINTS
    Provide 3-4 high-impact resume bullet points (using the Action-Context-Result framework) describing this project for the student's CV.
    Also highlight which crucial skills this project demonstrates, and list any areas where they might want to expand later (e.g. cloud security or microservices).
    
    ## 8. FUTURE SCOPE & CONCLUSION
    Discuss how this project can scale. Mention edge computing, production deployment, additional ML model training, or automation extensions. Conclude with summary remarks.
    """
    
    try:
        report_text = generate_text(
            prompt=prompt,
            api_key=api_key,
            system_instruction=REPORT_SYSTEM_INSTRUCTION
        )
        return report_text
    except Exception as e:
        raise e
