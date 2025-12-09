"""
Database operations - Contains SQL injection vulnerabilities
All vulnerabilities are self-contained within this file (no cross-file data flow)
"""
import sqlite3

DB_PATH = ":memory:"

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    setup_database(conn)
    return conn

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

def search_user(conn, username):
    """
    VULNERABLE FUNCTION - SQL Injection via f-string formatting
    All taint flow contained within this file
    """
    cursor = conn.cursor()
    
    # VULNERABILITY: Direct f-string interpolation - single file
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    return cursor.fetchall()

def search_user_by_email(conn, username, email):
    """
    VULNERABLE FUNCTION - SQL Injection via string concatenation
    All taint flow contained within this file
    """
    cursor = conn.cursor()
    
    # VULNERABILITY: String concatenation with multiple inputs - single file
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    
    if email:
        query += " AND email = '" + email + "'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    return cursor.fetchall()

def get_user_by_id(conn, user_id):
    """
    VULNERABLE FUNCTION - SQL Injection via % formatting
    All taint flow contained within this file
    """
    cursor = conn.cursor()
    
    # VULNERABILITY: % string formatting - single file
    query = "SELECT * FROM users WHERE id = %s" % user_id
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    return cursor.fetchone()

def get_admin_users(conn, admin_id):
    """
    VULNERABLE FUNCTION - SQL Injection in complex query
    All taint flow contained within this file
    """
    cursor = conn.cursor()
    
    # VULNERABILITY: f-string with additional SQL logic - single file
    query = f"SELECT username, email, secret_data FROM users WHERE is_admin = 1 AND id = '{admin_id}'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    return cursor.fetchall()

def authenticate_user_query(conn, username, password):
    """
    VULNERABLE FUNCTION - SQL Injection in authentication
    All taint flow contained within this file
    """
    cursor = conn.cursor()
    
    # VULNERABILITY: Multiple user inputs in query - single file
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    return cursor.fetchone()

def delete_user(conn, username):
    """
    VULNERABLE FUNCTION - SQL Injection in DELETE statement
    All taint flow contained within this file
    """
    cursor = conn.cursor()
    
    # VULNERABILITY: DELETE statement with user input - single file
    query = f"DELETE FROM users WHERE username = '{username}'"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    conn.commit()
    return cursor.rowcount

def update_user_secret(conn, user_id, new_secret):
    """
    VULNERABLE FUNCTION - SQL Injection in UPDATE statement
    All taint flow contained within this file
    """
    cursor = conn.cursor()
    
    # VULNERABILITY: UPDATE statement with user input - single file
    query = f"UPDATE users SET secret_data = '{new_secret}' WHERE id = {user_id}"
    
    print(f"[DEBUG] Executing: {query}")
    cursor.execute(query)
    conn.commit()
    return cursor.rowcount

