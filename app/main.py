from fastapi import FastAPI
from .routers.blog_route import blog_router

app = FastAPI()

app.include_router(blog_router)


@app.get("/")
def hello():
    return {"message": "API is working perfectly!"}
