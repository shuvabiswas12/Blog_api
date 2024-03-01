from datetime import datetime
from typing import List, Union
from bson import ObjectId
from pymongo.collection import Collection


class GenericRepository:

    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def get(self, id: str) -> Union[dict, None]:
        result = self.collection.find_one({"_id": ObjectId(id)})
        if result is None:
            return None
        result["id"] = str(result.pop("_id", None))
        return result

    def get_all(self, **kwargs) -> List[dict]:
        results = self.collection.find(kwargs)
        parsed_result = []
        for result in results:
            if "_id" in result:
                result["id"] = str(result.pop("_id", None))
                parsed_result.append(result)
        return parsed_result

    def create(self, item: any) -> Union[dict, None]:
        try:
            item_dict = item.model_dump()
            item_dict["created_at"] = datetime.now()
            result = self.collection.insert_one(item_dict)
            item_dict["id"] = str(result.inserted_id)
            return item_dict
        except Exception as e:
            print(e)
            return None

    def delete(self, id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    def update(self, id: str, item: any) -> Union[dict, None]:
        item_dict = item.model_dump()
        item_dict["updated_at"] = datetime.now()
        self.collection.update_one({"_id": ObjectId(id)}, {"$set": item_dict})
        return self.get(id)
