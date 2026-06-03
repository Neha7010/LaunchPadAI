from typing import List
from config.constants import DOMAIN_CLASSIFICATION_RULES, DEFAULT_DOMAIN

def classify_project(technologies: List[str]) -> str:
    """
    Classifies a project domain based on matched keywords in its technology stack.
    Implements deterministic Python rules for project classification.
    """
    if not technologies:
        return DEFAULT_DOMAIN
        
    tech_scores = {domain: 0 for domain in DOMAIN_CLASSIFICATION_RULES}
    
    # Standardize technologies to lowercase for matching
    tech_lower = [t.lower().strip() for t in technologies]
    
    # Check for keyword matches in technology list
    for domain, keywords in DOMAIN_CLASSIFICATION_RULES.items():
        for tech in tech_lower:
            # Check for exact matches or substring matches
            for kw in keywords:
                if kw in tech:
                    # Give extra weight if it's a strong identifier
                    tech_scores[domain] += 2 if kw == tech else 1
                    
    # Find the domain with the highest score
    best_domain = DEFAULT_DOMAIN
    highest_score = 0
    
    for domain, score in tech_scores.items():
        if score > highest_score:
            highest_score = score
            best_domain = domain
            
    return best_domain
