"""
Data models - Pydantic models for request/response
These models receive user input that flows to vulnerable database functions
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class User(BaseModel):
    """User model - receives tainted input"""
    id: Optional[int] = None
    username: str = Field(..., description="Username - flows to SQL query")
    email: Optional[str] = None
    password: Optional[str] = None

class SearchRequest(BaseModel):
    """Search request model - contains tainted fields"""
    query: str = Field(..., description="Search query - vulnerable to SQL injection")
    filters: Optional[List[str]] = None
    limit: Optional[int] = 10

class UpdateRequest(BaseModel):
    """Update request model - multiple tainted fields"""
    user_id: str = Field(..., description="User ID - flows to WHERE clause")
    field: str = Field(..., description="Field name - flows to SET clause")
    value: str = Field(..., description="Value - flows to SET clause")

class FilterRequest(BaseModel):
    """Filter request model - builds SQL filters"""
    field_name: str
    field_value: str
    operator: str = "="

