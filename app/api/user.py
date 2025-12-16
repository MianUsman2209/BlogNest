from fastapi import APIRouter, HTTPException
from app.schemas.login import UserLoginSchema
from app.utils.auth import create_token
from passlib.context import CryptContext
import json

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USERS_FILE = "app/storage/users.json"


@router.post("/login")
def login(data: UserLoginSchema):
    with open(USERS_FILE) as f:
        users = json.load(f)

    for user in users:
        if user["username"] == data.username:
            if pwd_context.verify(data.password, user["password"]):
                token = create_token({
                    "username": user["username"],
                    "role": user["role"]
                })
                return token

    raise HTTPException(status_code=401, detail="Invalid credentials")
