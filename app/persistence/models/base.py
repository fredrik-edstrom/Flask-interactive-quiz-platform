from abc import ABC

from pymongo.collection import Collection

from app.shared.resultlist import ResultList


class Document(dict, ABC):
    collection: Collection | None = None

    def __init__(self, data):
        super().__init__()
        if "_id" not in data:
            self._id = None
        self.__dict__.update(data)

    def __repr__(self) -> str:
        attributes = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attributes})"

    def __str__(self) -> str:
        attributes = "\n".join(f"\t{k}: {v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}:\n{attributes}"

    def __bool__(self) -> bool:
        return self.__dict__ != {}

    def save(self) -> None:
        if not self._id:
            del self.__dict__["_id"]
            self.collection.insert_one(self.__dict__)
        else:
            self.update_with(self.__dict__)

    def update_with(self, new_values: dict) -> None:
        self.__dict__.update(new_values)
        self.collection.replace_one({"_id": self._id}, self.__dict__)

    def delete(self) -> None:
        self.collection.delete_one({"_id": self._id})

    def delete_field(self, field: str) -> None:
        self.collection.update_one({"_id": self._id}, {"$unset": {field: ""}})

    def to_dict(self) -> dict:
        data = {k: v for (k, v) in self.__dict__.items() if k != "_id"}
        data["id"] = self.id
        return data

    @property
    def id(self) -> str:
        return str(self._id)

    @classmethod
    def find(cls, **kwargs):
        return ResultList(cls(item) for item in cls.collection.find(kwargs))

    @classmethod
    def delete_many(cls, **kwargs):
        cls.collection.delete_many(kwargs)
