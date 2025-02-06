from fastapi import Request, status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from auth.auth import SECRET_KEY, ALGORITHM

ROUTES_EXEMPT = ['login', 'register']

class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM

    async def dispatch(self, request: Request, call_next):
        url = str(request.url).split('/', maxsplit=3)[-1]
        request.state.user = None
        if url in ROUTES_EXEMPT:
            response = await call_next(request)
            return response
        
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            jwt_token = request.headers.get("JWT")
            if not jwt_token:
                return JSONResponse(
                    {"message": "Token absent ou incorrect"},
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
            try:
                payload = jwt.decode(jwt_token, self.secret_key, algorithms=[self.algorithm])
                request.state.user = payload
            except JWTError:
                return JSONResponse(
                    {"message": "Token incorrect ou invalide"},
                    status_code=status.HTTP_401_UNAUTHORIZED
                )

        response = await call_next(request)
        return response
    