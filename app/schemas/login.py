from pydantic import BaseModel

# For user registration
class UserRegisterSchema(BaseModel):
    username: str
    password: str
    role: str  # e.g., "admin" or "user"

# For user login
class UserLoginSchema(BaseModel):
    username: str
    password: str

# JWT token response
class TokenSchema(BaseModel):
    access_token: str
    token_type: str
