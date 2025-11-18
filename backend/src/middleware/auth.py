from typing import Optional, Callable
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..models.user import UserModel


class AuthMiddleware:
    def __init__(self):
        self.security = HTTPBearer(auto_error=False)

    async def __call__(self, request: Request, call_next: Callable):
        # Mock authentication - in real app, verify JWT token
        # For development, allow requests without auth header
        auth_header = request.headers.get("authorization")
        user_id = request.headers.get("x-user-id")
        user_email = request.headers.get("x-user-email")

        # If user info is provided in headers, fetch the user
        if user_id or user_email:
            try:
                if user_id:
                    user = await UserModel.find_by_id(user_id)
                elif user_email:
                    user = await UserModel.find_by_email(user_email)
                else:
                    user = None
                
                if user:
                    request.state.user = user
                else:
                    # Mock user if not found
                    request.state.user = {
                        "id": "user123",
                        "role": request.headers.get("x-user-role", "student"),
                        "email": "test@example.com",
                        "firstName": "Test",
                        "lastName": "User"
                    }
            except:
                # Fallback to mock user
                request.state.user = {
                    "id": "user123",
                    "role": request.headers.get("x-user-role", "student"),
                    "email": "test@example.com",
                    "firstName": "Test",
                    "lastName": "User"
                }
        else:
            # Mock user - in real app, decode JWT and get user from database
            request.state.user = {
                "id": "user123",
                "role": request.headers.get("x-user-role", "student"),
                "email": "test@example.com",
                "firstName": "Test",
                "lastName": "User"
            }

        response = await call_next(request)
        return response


# Dependency function for FastAPI
async def get_current_user(request: Request) -> dict:
    """Get current user from request state"""
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return request.state.user


async def require_instructor(request: Request) -> dict:
    """Require instructor or admin role"""
    user = await get_current_user(request)
    if user.get("role") not in ["instructor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Instructor access required"
        )
    return user

