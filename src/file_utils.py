import os
import json
from typing import TypeVar
from pydantic import BaseModel


# Save a pydantic model to a json file
def save_json(data: BaseModel, file_path: str):
    os.makedirs("output", exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data.model_dump(), f, indent=2)


# Load a pydantic model from a json file
T = TypeVar("T", bound=BaseModel)


def load_json(file_path: str, model_class: type[T]) -> T:
    with open(file_path, "r") as f:
        data = json.load(f)
        return model_class(**data)
