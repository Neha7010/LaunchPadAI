from typing import List, Dict, Any
from config.constants import COST_RATES

def estimate_project_cost(technologies: List[str], hardware: List[str] = None) -> Dict[str, Any]:
    """
    Estimates project costs based on the technologies and hardware selected.
    Returns details on monthly hosting, database, API costs, and one-time hardware costs.
    """
    if not hardware:
        hardware = []
        
    tech_lower = [t.lower().strip() for t in technologies]
    hw_lower = [h.lower().strip() for h in hardware]
    
    hosting_cost = 0.0
    hosting_desc = "Vercel / Hugging Face (Free Tier)"
    db_cost = 0.0
    db_desc = "SQLite / MongoDB Atlas (Free Tier)"
    api_cost = 0.0
    api_desc = "Gemini API (Free Tier / Developer Console)"
    hardware_cost = 0.0
    hardware_items = []
    
    # 1. Estimate Hosting Cost
    if "aws" in tech_lower or "ec2" in tech_lower:
        hosting_cost = COST_RATES["hosting"]["AWS EC2 (t2.micro)"]
        hosting_desc = "AWS EC2 t2.micro Instance"
    elif "render" in tech_lower:
        hosting_cost = COST_RATES["hosting"]["Render (Free/Hobby)"]
        hosting_desc = "Render Hobby Web Service"
    elif "heroku" in tech_lower:
        hosting_cost = COST_RATES["hosting"]["Heroku Eco"]
        hosting_desc = "Heroku Eco Dyno"
    else:
        # Default hosting is free (Vercel, Streamlit Community Cloud, or Hugging Face)
        hosting_cost = 0.0
        hosting_desc = "Hugging Face / Streamlit Cloud (Free)"
        
    # 2. Estimate Database Cost
    if "postgresql" in tech_lower and ("render" in tech_lower or "cloud" in tech_lower):
        db_cost = COST_RATES["database"]["Render PostgreSQL"]
        db_desc = "Render PostgreSQL Managed DB"
    elif "supabase" in tech_lower:
        db_cost = COST_RATES["database"]["Supabase (Free Tier)"]
        db_desc = "Supabase Database (Free)"
    elif "sqlite" in tech_lower:
        db_cost = COST_RATES["database"]["SQLite (Local/Free)"]
        db_desc = "SQLite Local DB"
    else:
        # Check if database is mentioned, default to Free MongoDB / Supabase
        db_keywords = ["postgres", "mysql", "mongodb", "database"]
        if any(any(db_kw in tech for db_kw in db_keywords) for tech in tech_lower):
            db_cost = 0.0
            db_desc = "Cloud Database (Free Tier)"
            
    # 3. Estimate API Cost
    if "gemini" in tech_lower or "llm" in tech_lower:
        # Small allowance for pay-as-you-go during development
        api_cost = COST_RATES["apis"]["Gemini 2.5 Flash (Pay-as-you-go)"]
        api_desc = "Gemini 2.5 Flash API (Pay-as-you-go)"
    else:
        api_cost = 0.0
        api_desc = "No external paid APIs expected"
        
    # 4. Estimate Hardware Cost
    for hw in hw_lower:
        if not hw or hw in ["none", "n/a"]:
            continue
        if "esp32" in hw or "esp8266" in hw:
            hardware_cost += COST_RATES["hardware"]["ESP32 Microcontroller"]
            hardware_items.append("ESP32 Dev Module ($10)")
        elif "raspberry" in hw or "pi" in hw:
            hardware_cost += COST_RATES["hardware"]["Raspberry Pi 4 / 5"]
            hardware_items.append("Raspberry Pi Board ($45)")
        elif "sensor" in hw or "dht" in hw or "ldr" in hw or "soil" in hw:
            hardware_cost += COST_RATES["hardware"]["Basic Sensor Kit"]
            hardware_items.append("Sensor Interface Kit ($15)")
        elif "camera" in hw or "vision" in hw or "webcam" in hw:
            hardware_cost += COST_RATES["hardware"]["Camera Module"]
            hardware_items.append("Camera Module ($20)")
            
    total_monthly = hosting_cost + db_cost + api_cost
    total_one_time = hardware_cost
    total_budget = total_one_time + total_monthly # initial launch budget
    
    return {
        "monthly_hosting": hosting_cost,
        "hosting_description": hosting_desc,
        "monthly_database": db_cost,
        "database_description": db_desc,
        "monthly_api": api_cost,
        "api_description": api_desc,
        "one_time_hardware": total_one_time,
        "hardware_items": hardware_items,
        "total_monthly": round(total_monthly, 2),
        "total_one_time": round(total_one_time, 2),
        "initial_budget": round(total_budget, 2)
    }
