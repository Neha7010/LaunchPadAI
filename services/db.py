import sqlite3
import hashlib
import json
from datetime import datetime
from config.settings import DB_PATH

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if tables don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    
    # Create generated_projects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS generated_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        project_title TEXT NOT NULL,
        project_type TEXT NOT NULL,
        score REAL NOT NULL,
        complexity TEXT NOT NULL,
        report TEXT NOT NULL, -- JSON formatted report content
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Helper to hash passwords using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(username: str, password: str) -> bool:
    """Registers a new user. Returns True if successful, False otherwise."""
    username = username.strip().lower()
    if not username or not password:
        return False
        
    conn = get_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    created_at = datetime.utcnow().isoformat()
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, password_hash, created_at)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username: str, password: str):
    """Logs in a user. Returns the user dict if successful, None otherwise."""
    username = username.strip().lower()
    conn = get_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    
    cursor.execute(
        "SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
        (username, password_hash)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None

def save_project(user_id: int, project_title: str, project_type: str, score: float, complexity: str, report_data: dict) -> bool:
    """Saves a generated project to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_json = json.dumps(report_data)
    
    try:
        cursor.execute(
            """
            INSERT INTO generated_projects (user_id, project_title, project_type, score, complexity, report, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, project_title, project_type, score, complexity, report_json, created_at)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving project to DB: {e}")
        return False
    finally:
        conn.close()

def get_user_projects(user_id: int):
    """Retrieves all generated projects for a specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, project_title, project_type, score, complexity, report, created_at FROM generated_projects WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    projects = []
    for row in rows:
        proj = dict(row)
        # Parse the JSON report string
        try:
            proj['report'] = json.loads(proj['report'])
        except Exception:
            proj['report'] = {}
        projects.append(proj)
    return projects

# Initialize DB on import
init_db()
