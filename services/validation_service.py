from typing import List, Dict, Any
from config.constants import RESUME_KEYWORDS

def validate_tech_stack(technologies: List[str]) -> Dict[str, Any]:
    """
    Validates a suggested technology stack using rule-based checks.
    Analyzes missing components, compatibility warnings, and resume impact.
    """
    tech_lower = [t.lower().strip() for t in technologies]
    warnings = []
    
    # 1. Compatibility & Architecture Validation Rules
    has_frontend = any(x in tech_lower for x in ["react", "vue", "angular", "next.js", "html", "css", "bootstrap", "tailwind"])
    has_backend = any(x in tech_lower for x in ["flask", "django", "fastapi", "node.js", "express", "spring boot", "asp.net"])
    has_db = any(x in tech_lower for x in ["postgresql", "mysql", "mongodb", "sqlite", "redis", "dynamodb", "supabase", "sql"])
    
    if has_frontend and not has_backend:
        warnings.append("Frontend technologies are suggested, but no backend framework (like FastAPI or Flask) is listed. Consider adding a backend service.")
        
    if has_backend and not has_db:
        warnings.append("Backend server framework is suggested, but no database (like SQLite or PostgreSQL) is listed. You may need local persistence.")
        
    # Check for library duplicates / overlaps
    if "tensorflow" in tech_lower and "pytorch" in tech_lower:
        warnings.append("Both PyTorch and TensorFlow are listed. Usually, it's best to stick to one deep learning library to keep packages clean.")
        
    # 2. Resume Impact Analysis (Demonstrated vs Missing Skills)
    demonstrated_categories = {}
    missing_categories = []
    
    for category, keywords in RESUME_KEYWORDS.items():
        matched_skills = []
        for tech in technologies:
            tech_clean = tech.lower().strip()
            # If any keyword matches a technology substring
            for kw in keywords:
                if kw in tech_clean:
                    matched_skills.append(tech)
                    break
        
        if matched_skills:
            # We take the unique set of matched skills
            demonstrated_categories[category] = list(set(matched_skills))
        else:
            missing_categories.append(category)
            
    return {
        "is_valid": len(warnings) == 0,
        "warnings": warnings,
        "demonstrated_categories": demonstrated_categories,
        "missing_categories": missing_categories
    }
