import io
import zipfile
from typing import List, Dict, Any

def get_suggested_structure(category: str) -> str:
    """Returns a directory structure map based on the project category."""
    if category == "Advanced Intelligent Agent":
        return """Project-Root/
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   ├── model_definition.py
│   └── checkpoint_placeholder.txt
├── notebooks/
│   └── research_sandbox.ipynb
├── src/
│   ├── __init__.py
│   ├── inference.py
│   └── train.py
├── api/
│   ├── app.py
│   └── schemas.py
├── requirements.txt
└── README.md
"""
    elif category == "Cyber-Physical System":
        return """Project-Root/
├── firmware/
│   ├── src/
│   │   └── main.cpp
│   └── platformio.ini
├── gateway/
│   ├── config.json
│   └── listener.py
├── dashboard/
│   ├── app.py
│   └── index.css
├── docs/
│   └── wiring_diagram.png
├── requirements.txt
└── README.md
"""
    elif category == "Full Stack Application":
        return """Project-Root/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   ├── models/
│   │   └── routes/
│   ├── index.js
│   └── package.json
├── database/
│   ├── schema.sql
│   └── seeds.sql
├── docker-compose.yml
├── requirements.txt
└── README.md
"""
    else: # Data Science & Analytics or Default
        return """Project-Root/
├── data/
│   ├── dataset.csv
│   └── README.md
├── notebooks/
│   └── exploration.ipynb
├── src/
│   ├── data_loader.py
│   ├── feature_engineering.py
│   └── plotting.py
├── reports/
│   └── figures/
├── requirements.txt
└── README.md
"""

def generate_repo_files(blueprint: Dict[str, Any], category: str) -> Dict[str, str]:
    """Generates file contents for the repository starter kit."""
    title = blueprint.get("project_title", "Starter Project")
    problem = blueprint.get("problem_statement", "No problem statement provided.")
    techs = blueprint.get("suggested_technologies", [])
    features = blueprint.get("key_features", [])
    phases = blueprint.get("implementation_phases", [])
    
    # 1. Generate README.md
    readme = f"""# {title}

## Overview
{problem}

## Core Features
{chr(10).join([f"- {feat}" for feat in features])}

## Technology Stack
The project is built using:
{chr(10).join([f"- {tech}" for tech in techs])}

## Folder Structure
Refer to the `folder_structure.txt` for details.

## How to Run
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server / setup script. (Refer to milestones.md for week-by-week setup details).
"""

    # 2. Generate requirements.txt contents
    # Guess requirements based on techs
    reqs_list = []
    techs_lower = [t.lower().strip() for t in techs]
    
    # Python standard packages or framework dependencies
    if any("fastapi" in t for t in techs_lower):
        reqs_list.extend(["fastapi", "uvicorn", "pydantic"])
    if any("flask" in t for t in techs_lower):
        reqs_list.extend(["flask", "Werkzeug"])
    if any("streamlit" in t for t in techs_lower):
        reqs_list.append("streamlit")
    if any("pytorch" in t or "torch" in t for t in techs_lower):
        reqs_list.extend(["torch", "torchvision"])
    if any("tensorflow" in t for t in techs_lower):
        reqs_list.append("tensorflow")
    if any("pandas" in t for t in techs_lower):
        reqs_list.append("pandas")
    if any("numpy" in t for t in techs_lower):
        reqs_list.append("numpy")
    if any("scikit-learn" in t or "sklearn" in t for t in techs_lower):
        reqs_list.append("scikit-learn")
    if any("requests" in t for t in techs_lower):
        reqs_list.append("requests")
    if any("postgres" in t or "psycopg" in t for t in techs_lower):
        reqs_list.append("psycopg2-binary")
    if any("mongodb" in t or "pymongo" in t for t in techs_lower):
        reqs_list.append("pymongo")
    if any("gemini" in t or "generativeai" in t for t in techs_lower):
        reqs_list.append("google-generativeai")
        
    if not reqs_list:
        reqs_list = ["streamlit", "requests", "pydantic"]
        
    requirements = "\n".join(sorted(list(set(reqs_list)))) + "\n"
    
    # 3. Generate folder_structure.txt
    structure = get_suggested_structure(category)
    
    # 4. Generate milestones.md
    milestones_content = f"# Development Milestones - {title}\n\n"
    for phase in phases:
        p_name = phase.get("phase_name", "Phase")
        p_dur = phase.get("duration", "Week")
        p_tasks = phase.get("tasks", [])
        
        milestones_content += f"## {p_name} ({p_dur})\n"
        for task in p_tasks:
            milestones_content += f"- [ ] {task}\n"
        milestones_content += "\n"
        
    return {
        "README.md": readme,
        "requirements.txt": requirements,
        "folder_structure.txt": structure,
        "milestones.md": milestones_content
    }

def create_zip_archive(blueprint: Dict[str, Any], category: str) -> bytes:
    """Compiles the starter kit files into a ZIP archive and returns the bytes."""
    files = generate_repo_files(blueprint, category)
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for filename, content in files.items():
            zip_file.writestr(filename, content)
            
    return zip_buffer.getvalue()
