# backend.py
import sqlite3

def setup_database():
    """Sets up a temporary in-memory database with dummy data."""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create a users table
    cursor.execute("CREATE TABLE users (id INTEGER, username TEXT, secret_data TEXT)")
    
    # Insert dummy data
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'SuperSecretAdminPassword')")
    cursor.execute("INSERT INTO users VALUES (2, 'guest', 'GuestWelcomeMessage')")
    cursor.execute("INSERT INTO users VALUES (3, 'alice', 'AlicePrivateNote')")
    
    conn.commit()
    return conn

def search_user_unsafe(conn, user_input):
    """
    VULNERABLE FUNCTION:
    Directly formatting the input string into the query creates an injection point.
    """
    cursor = conn.cursor()
    
    # THE VULNERABILITY: String concatenation (f-string)
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    
    print(f"\n[DEBUG] Executing SQL: {query}") # For demo visibility
    
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        return f"Database Error: {e}"