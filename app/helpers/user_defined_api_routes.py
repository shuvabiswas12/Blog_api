from fastapi import FastAPI
from fastapi.routing import APIRoute
from typing import List, Dict


def get_user_defined_routes(app: FastAPI) -> List[APIRoute]:
    """Retrieve all user-defined routes from a FastAPI application."""
    user_defined_routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            user_defined_routes.append(route)
    return user_defined_routes


def extract_routes_with_tags(user_defined_routes: List[APIRoute]) -> List[Dict[str, List[Dict[str, str]]]]:
    """Extract routes with their corresponding tags."""
    routes_with_tags = {}
    for route in user_defined_routes:
        for tag in route.tags:
            if tag in routes_with_tags:
                routes_with_tags[tag].append(
                    {"path": route.path, "method": list(route.methods)[0]})
            else:
                routes_with_tags[tag] = [
                    {"path": route.path, "method": list(route.methods)[0]}]
    return [routes_with_tags]
