from fastapi import FastAPI

from app.routers.user_route import user_router
from app.routers.blog_route import blog_router

app = FastAPI()

app.include_router(blog_router)
app.include_router(user_router)


@app.get("/")
def hello():
    return {"message": "API is working perfectly!"}
