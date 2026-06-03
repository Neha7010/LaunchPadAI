
# Launchpad AI — Project Recommendation & Blueprint Generator

Launchpad AI is a production-ready, AI-powered project recommendation and blueprint generation platform designed to help students discover and bootstrap their academic portfolio. The application leverages an **LLM + Rule-Based Validation Architecture** combining natural language reasoning with deterministic Python validations.

---

## 🛠️ Architecture

```
Student Profile
      │
      ▼
Profile Extraction (Gemini 2.5 Flash)
      │
      ▼
Research-Augmented Retrieval Layer (DuckDuckGo / Local Fallback)
      │
      ▼
Gemini Recommendations Engine (Recommends 3 distinct projects)
      │
      ▼
Python Validation Engine
 ├── Project Classifier (Rule-based categorization)
 ├── Complexity Analyzer (Score & difficulty tier calculations)
 ├── Cost Estimator (Monthly hosting, API, and hardware budgets)
 └── Resume Impact Analyzer (Demonstrated vs missing skills matching)
      │
      ▼
Starter Repository Generator (Creates README, requirements, folder layouts, and milestones)
      │
      ▼
Detailed Academic Report Generator (Full text expansions via Gemini)
      │
      ▼
Premium Glassmorphism Streamlit UI
```

---

## ✨ Features

1. **Lightweight Research-Augmented Generation**: Generates targeted DuckDuckGo searches based on student profile elements, gathering real-world project context. If offline, it seamlessly falls back to a curated local database (`research_contexts.json`).
2. **Deterministic Validation & Categorization**: Analyzes stack requirements to output clear warning notes and matches technologies to resume domains (Cloud, Security, Database, Testing, AI/ML).
3. **Budget Cost Estimator**: Calculates estimated hosting rates (AWS, Render, Heroku) and hardware parts requirements (ESP32, Raspberry Pi).
4. **Side-by-Side Comparison**: Compare up to three recommendations side-by-side inside a responsive layout.
5. **Saved Blueprint History**: Stored user details and reports inside a SQLite database.
6. **Starter GitHub Repository Downloader**: Generates standard workspace folders, READMEs, requirements files, and weekly milestone tracking, bundling them into a ZIP download.
7. **Academic Report Exports**: Save generated reports as a styled PDF, Markdown, or plain text file.

---

## 🚀 Setup & Installation

### Local Setup
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd launchpad-ai
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your API Key (Optional)**:
   You can export the API key in your terminal or type it directly into the application sidebar:
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key" # On Windows powershell: $env:GEMINI_API_KEY="your-gemini-api-key"
   ```

5. **Run the Streamlit Application**:
   ```bash
   streamlit run app.py
   ```


2. **Run the container**:
   ```bash
   docker run -d -p 7860:7860 -e GEMINI_API_KEY="your-gemini-key" launchpad-ai
   ```
   Open your browser to [http://localhost:7860](http://localhost:7860) to access the app.
