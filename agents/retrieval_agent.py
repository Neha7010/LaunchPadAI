from typing import List, Dict, Any
from services.search_service import retrieve_context

def generate_search_query(profile: Dict[str, Any]) -> str:
    """Formulates a search query tailored to the student's profile."""
    skills = profile.get("skills", [])
    interests = profile.get("interests", [])
    career_goal = profile.get("career_goal", "Software Developer")
    
    # Select key elements to make a focused query
    tech_keywords = ", ".join(skills[:2]) if skills else "Python"
    interest_keywords = ", ".join(interests[:2]) if interests else "Software Development"
    
    # Example: "AI Engineer projects agriculture IoT Python PyTorch"
    query = f"highly demanded projects for {career_goal} in {interest_keywords} using {tech_keywords}"
    return query

def run_retrieval(profile: Dict[str, Any]) -> List[str]:
    """Generates a query, retrieves context, and returns snippets."""
    query = generate_search_query(profile)
    
    # Collect keys for local fallback matching
    domain_keys = []
    domain_keys.extend(profile.get("interests", []))
    domain_keys.append(profile.get("career_goal", ""))
    domain_keys.append(profile.get("major", ""))
    
    # Retrieve snippets
    snippets = retrieve_context(query, domain_keys=domain_keys, max_results=4)
    return snippets
