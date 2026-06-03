# Project Classification Rules
DOMAIN_CLASSIFICATION_RULES = {
    "Advanced Intelligent Agent": ["tensorflow", "pytorch", "keras", "scikit-learn", "llm", "gemini", "openai", "transformers", "huggingface", "nlp", "rag", "langchain", "llama", "nlp", "computer vision", "spacy", "nltk"],
    "Cyber-Physical System": ["arduino", "esp32", "esp8266", "raspberry pi", "iot", "sensor", "actuator", "microcontroller", "firmware", "embedded", "gpio", "modbus", "ble", "zigbee"],
    "Full Stack Application": ["react", "vue", "angular", "flask", "django", "fastapi", "mysql", "postgresql", "mongodb", "sqlite", "node.js", "express", "next.js", "bootstrap", "css", "html", "javascript", "typescript", "tailwind"],
    "Data Science & Analytics": ["pandas", "numpy", "matplotlib", "seaborn", "plotly", "tableau", "spark", "hadoop", "sql", "data pipeline", "etl", "data visualization", "statsmodels"]
}

# General fallback domain if nothing matches
DEFAULT_DOMAIN = "General Software Application"

# Complexity Thresholds
COMPLEXITY_THRESHOLDS = {
    "beginner_max_techs": 3,
    "intermediate_max_techs": 6
}

# Cost Estimation Constants (in USD)
COST_RATES = {
    "hosting": {
        "Vercel (Free Tier)": 0.0,
        "Render (Free/Hobby)": 7.0,
        "AWS EC2 (t2.micro)": 8.5,
        "Heroku Eco": 5.0,
        "Hugging Face Spaces (Free)": 0.0
    },
    "database": {
        "SQLite (Local/Free)": 0.0,
        "MongoDB Atlas (Free Tier)": 0.0,
        "Render PostgreSQL": 7.0,
        "Supabase (Free Tier)": 0.0
    },
    "apis": {
        "Gemini 2.5 Flash (Free Tier)": 0.0,
        "Gemini 2.5 Flash (Pay-as-you-go)": 0.05, # estimated per 100 blueprint generations
        "DuckDuckGo Search (Free)": 0.0
    },
    "hardware": {
        "ESP32 Microcontroller": 10.0,
        "Raspberry Pi 4 / 5": 45.0,
        "Basic Sensor Kit": 15.0,
        "Camera Module": 20.0,
        "None": 0.0
    }
}

# Core resume analysis keywords
RESUME_KEYWORDS = {
    "Cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "cloud", "s3", "ec2", "serverless", "lambda"],
    "Security": ["auth", "jwt", "oauth", "security", "encryption", "hash", "ssl", "https", "cybersecurity", "firewall", "cryptography"],
    "Database": ["sql", "nosql", "postgres", "mysql", "mongodb", "sqlite", "redis", "database", "orm", "prisma", "sqlalchemy"],
    "Testing": ["pytest", "unittest", "testing", "ci/cd", "github actions", "jest", "selenium", "mock"],
    "AI/ML": ["ml", "ai", "deep learning", "nlp", "llm", "neural network", "prediction", "classification", "regression", "inference"]
}
