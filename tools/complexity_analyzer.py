from typing import List, Dict, Any

def analyze_complexity(technologies: List[str], hardware: List[str] = None) -> Dict[str, Any]:
    """
    Deterministically computes a complexity score (1-10) and assigns a difficulty tier
    (Beginner, Intermediate, Advanced) based on technology counts and features.
    """
    if not hardware:
        hardware = []
        
    score = 3.0 # Base score for any software project
    
    # Standardize inputs to lowercase
    tech_lower = [t.lower().strip() for t in technologies]
    hw_lower = [h.lower().strip() for h in hardware]
    
    # 1. Size of Tech Stack
    num_techs = len(tech_lower)
    score += min(num_techs * 0.5, 3.0) # Up to +3.0
    
    # 2. AI Complexity
    ai_keywords = ["tensorflow", "pytorch", "keras", "transformers", "llm", "gemini", "openai", "huggingface", "onnx", "ml", "deep learning", "nlp", "rag"]
    has_ai = any(any(kw in tech for kw in ai_keywords) for tech in tech_lower)
    if has_ai:
        score += 1.5
        
    # 3. Hardware / IoT Complexity
    if hw_lower and not (len(hw_lower) == 1 and hw_lower[0] in ["none", ""]):
        score += 1.0
        
    # 4. Deployment / Cloud Complexity
    cloud_keywords = ["docker", "kubernetes", "aws", "gcp", "azure", "ec2", "s3", "ecs", "eks", "ci/cd", "github actions"]
    has_cloud = any(any(kw in tech for kw in cloud_keywords) for tech in tech_lower)
    if has_cloud:
        score += 1.0
        
    # 5. Database Multiplicity
    db_keywords = ["postgresql", "mysql", "mongodb", "sqlite", "redis", "dynamodb", "supabase"]
    has_db = any(any(kw in tech for kw in db_keywords) for tech in tech_lower)
    if has_db:
        score += 0.5
        
    # Cap score at 10.0 and round
    final_score = min(round(score, 1), 10.0)
    
    # Assign Difficulty Tier
    if final_score < 5.0:
        difficulty = "Beginner"
    elif final_score < 8.0:
        difficulty = "Intermediate"
    else:
        difficulty = "Advanced"
        
    return {
        "complexity_score": final_score,
        "difficulty": difficulty,
        "metrics": {
            "tech_count": num_techs,
            "has_ai": has_ai,
            "has_hardware": len(hw_lower) > 0 and hw_lower[0] not in ["none", ""],
            "has_cloud": has_cloud
        }
    }
