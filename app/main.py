from fastapi import FastAPI
from app.api import user, user_registration, articles, admin

app = FastAPI(title="Personal Blog", version="0.1.0")

# Include routers
app.include_router(user_registration.router)
app.include_router(user.router)
app.include_router(articles.router)
app.include_router(admin.router)
