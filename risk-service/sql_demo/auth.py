"""
Authentication module - Contains SQL injection vulnerabilities
All vulnerabilities are self-contained within this file (no cross-file data flow)
"""
import sqlite3

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

def authenticate_user(username, password):
    """
    Authenticate user - VULNERABLE FUNCTION
    All taint flow contained within this file
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY: Multiple user inputs in query - single file
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    user = cursor.fetchone()
    
    return user

def check_user_permissions(username, resource):
    """
    Check user permissions - VULNERABLE FUNCTION
    All taint flow contained within this file
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY: Both username and resource are user-controlled - single file
    query = f"SELECT permission_level FROM user_permissions WHERE username = '{username}' AND resource = '{resource}'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    return cursor.fetchone()

def get_user_profile(username):
    """
    Get user profile - VULNERABLE FUNCTION
    All taint flow contained within this file
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY: Direct f-string interpolation - single file
    query = f"SELECT username, email, secret_data FROM users WHERE username = '{username}'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    return cursor.fetchone()

def validate_session(session_id):
    """
    Validate session - VULNERABLE FUNCTION
    All taint flow contained within this file
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY: Session ID from user input - single file
    query = f"SELECT user_id, expires_at FROM sessions WHERE session_id = '{session_id}'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    return cursor.fetchone()

