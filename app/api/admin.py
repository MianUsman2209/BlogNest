from fastapi import APIRouter, Depends, HTTPException
from app.utils.auth import permission_required
import json, os

router = APIRouter(prefix="/admin", tags=["Admin"])

USERS_FILE = "app/storage/users.json"
ART_FILE = "app/storage/articles.json"


@router.get("/users")
def get_users(user=Depends(permission_required("delete"))):
    with open(USERS_FILE) as f:
        return json.load(f)


@router.get("/articles")
def get_articles(user=Depends(permission_required("delete"))):
    if not os.path.exists(ART_FILE):
        return []
    return json.load(open(ART_FILE))


@router.put("/articles/{id}")
def admin_update_article(id: int, article: dict, user=Depends(permission_required("update"))):
    data = json.load(open(ART_FILE))
    for a in data:
        if a["id"] == id:
            a.update(article)
            json.dump(data, open(ART_FILE, "w"), indent=4)
            return {"message": "Article updated"}
    raise HTTPException(404, "Article not found")


@router.delete("/articles/{id}")
def admin_delete_article(id: int, user=Depends(permission_required("delete"))):
    data = json.load(open(ART_FILE))
    new_data = [a for a in data if a["id"] != id]
    json.dump(new_data, open(ART_FILE, "w"), indent=4)
    return {"message": "Article deleted"}
