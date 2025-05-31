from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if token != "valid_token":
            raise HTTPException(status_code=401, detail="Invalid credentials")
        response = await call_next(request)
        return response
