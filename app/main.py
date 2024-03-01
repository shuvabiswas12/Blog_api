from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.helpers.user_defined_api_routes import extract_routes_with_tags, get_user_defined_routes
from app.routers.like_route import like_router

from app.routers.user_route import user_router
from app.routers.blog_route import blog_router

app = FastAPI()

app.include_router(blog_router)
app.include_router(user_router)
app.include_router(like_router)

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Initialize Jinja2 templates
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@app.get("/")
def hello(request: Request):
    api_routes = extract_routes_with_tags(get_user_defined_routes(app))
    return templates.TemplateResponse("index.html", {"request": request, "docs": str(request.url) + "docs", "api_routes": api_routes})
