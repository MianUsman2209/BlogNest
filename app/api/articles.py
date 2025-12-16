from fastapi import APIRouter, Depends, HTTPException
from app.schemas.article import ArticleCreateSchema, ArticleUpdateSchema
from app.utils.auth import get_current_user
import json, os

router = APIRouter(prefix="/articles", tags=["Articles"])
ART_FILE = "app/storage/articles.json"

def load_articles():
    if not os.path.exists(ART_FILE):
        return []
    return json.load(open(ART_FILE, "r"))

def save_articles(data):
    json.dump(data, open(ART_FILE, "w"), indent=4)

@router.get("")
def list_articles():
    return load_articles()

@router.post("")
def create_article(article: ArticleCreateSchema, user=Depends(get_current_user)):
    data = load_articles()
    data.append({
        "id": len(data) + 1,
        "title": article.title,
        "content": article.content,
        "published_date": article.published_date.isoformat(),  # ✅ use published_date
        "author": user["username"]
    })
    save_articles(data)
    return {"message": "Article created"}

@router.put("/{id}")
def update_article(id: int, article: ArticleUpdateSchema, user=Depends(get_current_user)):
    data = load_articles()
    for a in data:
        if a["id"] == id and a["author"] == user["username"]:
            if article.title is not None:
                a["title"] = article.title
            if article.content is not None:
                a["content"] = article.content
            if article.published_date is not None:
                a["published_date"] = article.published_date.isoformat()
            save_articles(data)
            return {"message": "Article updated"}
    raise HTTPException(status_code=403, detail="Not allowed")

@router.delete("/{id}")
def delete_article(id: int, user=Depends(get_current_user)):
    data = load_articles()
    new_data = [a for a in data if not (a["id"] == id and a["author"] == user["username"])]
    save_articles(new_data)
    return {"message": "Article deleted"}
