from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt, json, os

SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
ROLES_FILE = "app/storage/roles.json"

# Ensure roles file exists
if not os.path.exists(ROLES_FILE):
    default_roles = {
        "admin": ["view_users", "view_articles", "create", "update", "delete"],
        "user": ["create", "update"]
    }
    with open(ROLES_FILE, "w") as f:
        json.dump(default_roles, f, indent=4)


def create_token(data: dict):
    return {
        "access_token": jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM),
        "token_type": "bearer"
    }


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


def permission_required(permission: str):
    def checker(user=Depends(get_current_user)):
        with open(ROLES_FILE) as f:
            roles = json.load(f)

        role = user.get("role")
        if role not in roles or permission not in roles[role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        return user
    return checker
