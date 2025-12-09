# SQL Injection Demo - Single-File Vulnerabilities

This directory contains Python files designed to demonstrate SQL injection vulnerabilities where each vulnerability is contained within a single file (no cross-file data flow). The purpose is to showcase SAST (Static Application Security Testing) capabilities, including Snyk Agent Fix, which can automatically fix vulnerabilities that don't span multiple files.

## File Structure

- **app.py** - Main FastAPI application with HTTP endpoints containing SQL injection vulnerabilities (all self-contained)
- **database.py** - Database operations containing SQL injection vulnerabilities (all self-contained)
- **auth.py** - Authentication functions with SQL injection vulnerabilities (all self-contained)
- **utils.py** - Utility functions (kept for reference, but not used in vulnerable code paths)
- **models.py** - Pydantic models for request/response validation

## Vulnerability Structure

Each file contains self-contained SQL injection vulnerabilities where:
- User input flows directly from function parameter to SQL query
- No cross-file taint propagation
- All vulnerable code paths are within a single file

### app.py Vulnerabilities
- `/search` - F-string formatting vulnerability
- `/users/search` - String concatenation vulnerability
- `/login` - Multiple inputs in authentication query
- `/admin/users` - Complex query with f-string
- `/users/{user_id}` - % formatting vulnerability

### database.py Vulnerabilities
- `search_user()` - F-string formatting
- `search_user_by_email()` - String concatenation
- `get_user_by_id()` - % formatting
- `get_admin_users()` - Complex f-string query
- `authenticate_user_query()` - Multiple inputs
- `delete_user()` - DELETE statement vulnerability
- `update_user_secret()` - UPDATE statement vulnerability

### auth.py Vulnerabilities
- `authenticate_user()` - Authentication query with multiple inputs
- `check_user_permissions()` - Multiple inputs in permissions query
- `get_user_profile()` - Profile query with f-string
- `validate_session()` - Session validation query

## Vulnerability Patterns Demonstrated

1. **F-string formatting**: `f"SELECT * FROM users WHERE username = '{username}'"`
2. **String concatenation**: `"SELECT * FROM users WHERE username = '" + username + "'"`
3. **% formatting**: `"SELECT * FROM users WHERE id = %s" % user_id`
4. **Multiple inputs**: Both username and password in same query
5. **Non-SELECT queries**: DELETE and UPDATE statements

## Testing SQL Injection

Example payloads to test:
- `admin' OR '1'='1`
- `admin'--`
- `admin' UNION SELECT * FROM users--`
- `1' OR '1'='1`
- `admin'; DROP TABLE users--`

## Snyk Agent Fix Compatibility

These vulnerabilities are structured to be potentially fixable by Snyk Agent Fix because:
- Each vulnerability is contained within a single file
- User input flows directly from parameter to SQL query
- No complex inter-file data flow patterns
- Standard SQL injection patterns that can be automatically converted to parameterized queries

## Note

These files are intentionally vulnerable and should NEVER be used in production. They are designed solely for demonstrating SAST tool capabilities in detecting and automatically fixing SQL injection vulnerabilities.

