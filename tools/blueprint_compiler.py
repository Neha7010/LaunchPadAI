from typing import Dict, Any
from tools.project_classifier import classify_project
from tools.complexity_analyzer import analyze_complexity
from tools.cost_estimator import estimate_project_cost
from services.validation_service import validate_tech_stack
from tools.repo_generator import create_zip_archive

def compile_project_blueprint(blueprint_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compiles raw project recommendation blueprint from Gemini and applies 
    deterministic Python rules to classify, score, and validate it.
    """
    techs = blueprint_data.get("suggested_technologies", [])
    hardware = blueprint_data.get("estimated_hardware", [])
    
    # 1. Category Classification
    category = classify_project(techs)
    
    # 2. Complexity Analysis
    complexity_info = analyze_complexity(techs, hardware)
    comp_score = complexity_info["complexity_score"]
    difficulty = complexity_info["difficulty"]
    
    # 3. Cost Estimation
    cost_info = estimate_project_cost(techs, hardware)
    
    # 4. Tech Stack Validation & Resume Impact
    validation_info = validate_tech_stack(techs)
    
    # 5. Deterministic Project Score (out of 10)
    # Combine complexity, resume categories demonstrated, and deductions
    num_resume_cats = len(validation_info["demonstrated_categories"])
    warnings_deduction = min(len(validation_info["warnings"]) * 0.5, 1.5)
    
    raw_project_score = 4.0 + (comp_score * 0.3) + (num_resume_cats * 0.8) - warnings_deduction
    project_score = min(round(raw_project_score, 1), 10.0)
    
    # 6. Deterministic Novelty Score (out of 10)
    # Based on classification, tech list, and factors count
    novelty_base = 5.0
    techs_lower = [t.lower() for t in techs]
    
    if category == "Advanced Intelligent Agent":
        novelty_base += 1.5
    if any(x in techs_lower for x in ["gemini", "openai", "transformers", "huggingface", "llm", "rag"]):
        novelty_base += 1.5
    if len(blueprint_data.get("novelty_factors", [])) >= 3:
        novelty_base += 1.0
    elif len(blueprint_data.get("novelty_factors", [])) >= 2:
        novelty_base += 0.5
        
    novelty_score = min(round(novelty_base, 1), 10.0)
    
    # 7. Generate Repo Starter Pack
    # Note: ZIP bytes are excluded from JSON serialization when saving to SQLite,
    # but we compile them here to be available for downloads.
    zip_bytes = create_zip_archive(blueprint_data, category)
    
    return {
        "project_title": blueprint_data.get("project_title"),
        "problem_statement": blueprint_data.get("problem_statement"),
        "why_recommended": blueprint_data.get("why_recommended", []),
        "key_features": blueprint_data.get("key_features", []),
        "suggested_technologies": techs,
        "estimated_hardware": hardware,
        "architecture_description": blueprint_data.get("architecture_description"),
        "text_architecture_diagram": blueprint_data.get("text_architecture_diagram"),
        "novelty_factors": blueprint_data.get("novelty_factors", []),
        "implementation_phases": blueprint_data.get("implementation_phases", []),
        
        # Symbolic Analysis Fields
        "project_type": category,
        "difficulty": difficulty,
        "complexity_score": comp_score,
        "novelty_score": novelty_score,
        "project_score": project_score,
        
        # Validation & Costs
        "validation": validation_info,
        "costs": cost_info,
        
        # Downloadable Artifact Bytes
        "zip_bytes": zip_bytes
    }
