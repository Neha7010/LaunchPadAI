import json
import logging
from typing import List, Dict, Any
from pathlib import Path
from duckduckgo_search import DDGS
from config.settings import DATA_DIR

logger = logging.getLogger(__name__)

def get_local_contexts() -> Dict[str, List[str]]:
    """Loads fallback context dictionary from JSON file."""
    path = DATA_DIR / "research_contexts.json"
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading local research contexts: {e}")
    
    # Minimal static fallback in case file read fails
    return {
        "cybersecurity": ["phishing detection systems", "network anomaly detection", "vulnerability scanning"],
        "healthcare": ["patient vital sign monitoring", "disease prediction models", "medical image classification"],
        "agriculture": ["crop disease detection", "smart irrigation systems", "crop yield prediction"],
        "finance": ["algorithmic trading strategies", "fraud detection engines", "expense classification"],
        "education": ["intelligent tutoring systems", "automated grading assistants", "quiz builders"]
    }

def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Searches DuckDuckGo for matching web snippets."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return [
                {
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "href": r.get("href", "")
                }
                for r in results
            ]
    except Exception as e:
        logger.warning(f"DuckDuckGo search failed for query '{query}': {e}. Falling back to local context.")
        return []

def retrieve_context(query: str, domain_keys: List[str], max_results: int = 5) -> List[str]:
    """
    Main retrieval entry point. Tries web search. If empty or failed,
    applies local fallback lookup by matching domain keywords.
    """
    snippets = []
    
    # 1. Primary: DuckDuckGo
    web_results = search_duckduckgo(query, max_results=max_results)
    if web_results:
        for item in web_results:
            if item.get("snippet"):
                snippets.append(f"{item['title']}: {item['snippet']} (Source: {item['href']})")
                
    # 2. Fallback: Local curated contexts
    if not snippets:
        local_data = get_local_contexts()
        matched = False
        
        # Check domain_keys (e.g., interests or career goal keywords) against local context keys
        for key in domain_keys:
            key_clean = key.lower().strip()
            for db_key, db_snippets in local_data.items():
                if db_key in key_clean or db_clean_match(db_key, key_clean):
                    snippets.extend(db_snippets)
                    matched = True
                    
        # If no key matches, return general default snippets
        if not matched:
            # Gather a sample of general snippets
            for db_snippets in local_data.values():
                snippets.extend(db_snippets[:2])
                if len(snippets) >= max_results:
                    break
                    
        # Annotate sources for fallback
        snippets = [f"{s} (Source: Curated Local Context)" for s in snippets[:max_results]]
        
    return snippets

def db_clean_match(k1: str, k2: str) -> bool:
    """Helper to check sub-word inclusion."""
    return k1 in k2 or k2 in k1
