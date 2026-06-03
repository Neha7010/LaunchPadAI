import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.getenv("LAUNCHPAD_DB_PATH", str(BASE_DIR / "launchpad.db"))
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# API Keys
# Prioritizes environment variables (for Hugging Face Secrets), falls back to empty
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Gemini Settings
GEMINI_MODEL = "gemini-2.5-flash"

# Default fallback settings
DEFAULT_THEME = "dark"
PORT = int(os.getenv("PORT", 7860))
