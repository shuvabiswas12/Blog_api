from bson import ObjectId


def check_objectId(v: str) -> bool:
    if not ObjectId.is_valid(v):
        raise ValueError("Invalid user ID!")
    return True
