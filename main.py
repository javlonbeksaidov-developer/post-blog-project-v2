from fastapi import FastAPI

from app.category import Category, router_category  # noqa: F401
from app.comment import Comment, router_comment  # noqa: F401
from app.core.database import Base, engine
from app.like import Like, router_like  # noqa: F401
from app.post import Post, router_post  # noqa: F401
from app.user import User, router_user  # noqa: F401

app = FastAPI(title="Blog Post FastAPI")
""" ROUTERS """
app.include_router(router_user)
app.include_router(router_category)
app.include_router(router_post)
app.include_router(router_comment)
app.include_router(router_like)

Base.metadata.create_all(bind=engine)


@app.get("/")
def welcome():
    return {
        "project name": "post bilog project v2",
        "author": "Javlon Saidov Alijon o'g'li",
        "github": "https://github.com/javlonbeksaidov-developer",
    }
