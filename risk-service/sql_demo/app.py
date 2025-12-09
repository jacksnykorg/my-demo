"""
Main application file - Entry point for user requests
Demonstrates SQL injection vulnerabilities (single-file, no cross-file data flow)
"""
from fastapi import FastAPI, Request, Query
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI(title="SQL Injection Demo API")

# Database setup
DB_PATH = ":memory:"
_conn = None

def get_connection():
    """Get database connection"""
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH)
        setup_database(_conn)
    return _conn

def setup_database(conn):
    """Initialize database schema and sample data"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            email TEXT,
            password TEXT,
            is_admin INTEGER,
            secret_data TEXT
        )
    """)
    
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'admin@example.com', 'admin123', 1, 'SuperSecretAdminKey')")
    cursor.execute("INSERT INTO users VALUES (2, 'alice', 'alice@example.com', 'password', 0, 'AlicePrivateData')")
    cursor.execute("INSERT INTO users VALUES (3, 'bob', 'bob@example.com', 'bobpass', 0, 'BobConfidentialInfo')")
    
    conn.commit()

class UserSearchRequest(BaseModel):
    username: str
    email: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/search")
async def search_users(request: Request, username: str = Query(...)):
    """
    Search for users by username - VULNERABLE ENDPOINT
    SQL injection within single file (no cross-file data flow)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY: Direct f-string interpolation - all in one file
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    results = cursor.fetchall()
    
    return {"results": results}

@app.post("/users/search")
async def search_users_post(request: UserSearchRequest):
    """
    Search users via POST - VULNERABLE ENDPOINT
    SQL injection with string concatenation - all in one file
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY: String concatenation with multiple inputs - all in one file
    query = "SELECT * FROM users WHERE username = '" + request.username + "'"
    
    if request.email:
        query += " AND email = '" + request.email + "'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    results = cursor.fetchall()
    
    return {"users": results}

@app.post("/login")
async def login(request: LoginRequest):
    """
    Login endpoint - VULNERABLE ENDPOINT
    SQL injection in authentication - all in one file
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY: Multiple user inputs in query - all in one file
    query = f"SELECT * FROM users WHERE username = '{request.username}' AND password = '{request.password}'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    user = cursor.fetchone()
    
    if user:
        return {"status": "success", "user": user}
    else:
        return {"status": "failed"}

@app.get("/admin/users")
async def admin_get_users(admin_id: str = Query(...)):
    """
    Admin endpoint - VULNERABLE ENDPOINT
    SQL injection with complex query - all in one file
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY: f-string with additional SQL logic - all in one file
    query = f"SELECT username, email, secret_data FROM users WHERE is_admin = 1 AND id = '{admin_id}'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    admin_users = cursor.fetchall()
    
    return {"admin_users": admin_users}

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: str):
    """
    Get user by ID - VULNERABLE ENDPOINT
    SQL injection via % formatting - all in one file
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY: % string formatting - all in one file
    query = "SELECT * FROM users WHERE id = %s" % user_id
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    user = cursor.fetchone()
    
    return {"user": user}

