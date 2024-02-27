from datetime import datetime
from typing import Generic, List, TypeVar, Union
from bson import ObjectId
from pydantic import BaseModel
from pymongo.collection import Collection

T_RequestModel = TypeVar("T_RequestModel", bound=BaseModel)
T_ResponseModel = TypeVar("T_ResponseModel", bound=BaseModel)


class GenericRepository(Generic[T_RequestModel, T_ResponseModel]):

    def __init__(self, collection: Collection, requestModelType: T_RequestModel, responseModelType: T_ResponseModel) -> None:
        self.collection = collection
        self.T_RequestModel = requestModelType
        self.T_ResponseModel = responseModelType

    def get(self, id: str) -> Union[T_ResponseModel, None]:
        result = self.collection.find_one({"_id": ObjectId(id)})
        if result is None:
            return None
        result["id"] = str(result.pop("_id", None))
        return self.T_ResponseModel.model_validate(result)

    def get_all(self) -> List[T_ResponseModel]:
        results = self.collection.find()
        parsed_result = []
        for result in results:
            if "_id" in result:
                result["id"] = str(result.pop("_id", None))
                parsed_result.append(result)
        return [self.T_ResponseModel.model_validate(item) for item in parsed_result]

    def create(self, item: T_RequestModel) -> Union[T_ResponseModel, None]:
        try:
            item_dict = item.model_dump()
            item_dict["created_at"] = datetime.now()
            result = self.collection.insert_one(item_dict)
            item_dict["id"] = str(result.inserted_id)
            return self.T_ResponseModel.model_validate(item_dict)
        except Exception as e:
            print(e)
            return None

    def delete(self, id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    def update(self, id: str, item: T_RequestModel) -> Union[T_ResponseModel, None]:
        item_dict = item.model_dump()
        item_dict["updated_at"] = datetime.now()
        self.collection.update_one({"_id": ObjectId(id)}, {"$set": item_dict})
        return self.get(id)
