"""
Data transfer objects are direct maps of the interface (in this case the REST Api)
input. Each endpoint is bind to one DTO that validates the type and value of
the input. The validation is executed by the cerberus module based on the
validation_schema stored in the DTO model.
"""

from dataclasses import dataclass
from abc import ABC


@dataclass
class BaseDTO(ABC):
    pass


@dataclass
class RegisterCarItemDTO(BaseDTO):
    id: int
    seats: int

    validation_schema = {
        "id": {"type": "integer", "min": 1},
        "seats": {"type": "integer", "allowed": [4, 5, 6]},
    }


@dataclass
class RegisterCarsDTO(list):
    data: list[RegisterCarItemDTO]

    def __init__(self, data: list):
        self.data = [RegisterCarItemDTO(**item) for item in data]

    def __iter__(self):
        return iter(self.data)

    def __next__(self):
        return next(self.data)


@dataclass
class RegisterJourneyDTO(BaseDTO):
    id: int
    people: int

    validation_schema = {
        "id": {"type": "integer", "min": 1},
        "people": {"type": "integer", "min": 1, "maxlength": 6},
    }


@dataclass
class DropOffDTO(BaseDTO):
    ID: int

    validation_schema = {"ID": {"type": "integer", "min": 1, "required": True}}


@dataclass
class LocateDTO(BaseDTO):
    ID: int

    validation_schema = {"ID": {"type": "integer", "min": 1}}


@dataclass
class LocateResponseDTO(BaseDTO):
    id: int
    seats: int

    validation_schema = {
        "id": {"type": "integer", "min": 1},
        "seats": {"type": "integer", "allowed": [4, 5, 6]},
    }
