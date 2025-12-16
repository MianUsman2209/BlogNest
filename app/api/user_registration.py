from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.login import UserRegisterSchema, TokenSchema
from passlib.context import CryptContext
from app.utils.auth import create_token
import json
import os

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Storage paths
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "storage")
USERS_FILE = os.path.join(STORAGE_DIR, "users.json")

# Ensure storage directory exists
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

# Ensure users.json exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f, indent=4)


@router.post("/register", response_model=TokenSchema)
def register(user: UserRegisterSchema):
    # Load existing users
    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    # Check if username exists
    if any(u["username"] == user.username for u in users):
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password and store
    hashed_password = pwd_context.hash(user.password)
    users.append({"username": user.username, "password": hashed_password, "role": user.role})

    # Write back to file
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

    # Create JWT token
    token = create_token({"username": user.username, "role": user.role})
    return token


@router.post("/login", response_model=TokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Load users
    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    # Find user
    db_user = next((u for u in users if u["username"] == form_data.username), None)
    if not db_user or not pwd_context.verify(form_data.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create token
    token = create_token({"username": db_user["username"], "role": db_user["role"]})
    return token
