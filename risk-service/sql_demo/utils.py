"""
Utility functions - Process user input before passing to database
These functions don't sanitize input, allowing taint to propagate
"""
import re

def process_search_input(user_input):
    """
    Process search input - DOES NOT SANITIZE
    Taint propagates through this function
    """
    # Trim whitespace but don't sanitize SQL
    processed = user_input.strip()
    
    # Add some processing that doesn't remove SQL injection patterns
    if processed:
        processed = processed.lower()
    
    return processed

def sanitize_input(input_str):
    """
    FAKE SANITIZATION - Doesn't actually prevent SQL injection
    This function claims to sanitize but doesn't remove dangerous characters
    """
    # Only removes leading/trailing spaces - doesn't prevent SQL injection
    sanitized = input_str.strip()
    
    # This regex doesn't catch SQL injection patterns
    sanitized = re.sub(r'[^\w\s@.-]', '', sanitized)
    
    return sanitized

def format_search_query(username):
    """
    Format search query - Taint propagates
    Adds formatting but doesn't escape SQL special characters
    """
    # Format the query but don't escape single quotes
    formatted = username
    
    # Add wildcard support (but doesn't prevent injection)
    if '*' in formatted or '%' in formatted:
        formatted = formatted.replace('*', '%')
    
    return formatted

def prepare_login_data(username, password):
    """
    Prepare login data - Taint propagates through both fields
    Processes both username and password without sanitization
    """
    # Process both inputs without sanitization
    processed_username = username.strip()
    processed_password = password.strip()
    
    # Some business logic that doesn't prevent SQL injection
    if len(processed_username) > 50:
        processed_username = processed_username[:50]
    
    if len(processed_password) > 100:
        processed_password = processed_password[:100]
    
    return {
        'username': processed_username,
        'password': processed_password
    }

def process_user_id(user_id):
    """
    Process user ID - Taint propagates
    Attempts to validate but doesn't prevent SQL injection
    """
    # Try to convert to int, but if it fails, return as string
    # This allows SQL injection if input is not numeric
    try:
        int_id = int(user_id)
        return str(int_id)  # Convert back to string - still vulnerable!
    except ValueError:
        # If not numeric, return as-is - VULNERABLE!
        return user_id

def build_search_filter(field, value):
    """
    Build search filter - Taint propagates
    Constructs SQL WHERE clause fragment without proper escaping
    """
    # Builds SQL fragment without parameterization
    filter_clause = f"{field} = '{value}'"
    return filter_clause

def combine_filters(filters):
    """
    Combine multiple filters - Taint propagates
    Combines SQL fragments without sanitization
    """
    if not filters:
        return ""
    
    # Combine filters with AND - all tainted
    combined = " AND ".join(filters)
    return combined

