"""
Contains the error messages and the BI specific static values.
"""

from enum import Enum


class ExceptionMessages(Enum):
    CarAlreadyExists = "Car with id %s already exists."
    InvalidNumberOfSeats = "Car can only have 4, 5 or 6 seats"
    CarNotFound = "Car with id: %s not found"
    CarForJourneyNotFound = "Car for journey with id: %s not found"
    JourneyNotFound = "Journey with id: %s not found"
    NumberOfPassangersInterval = "Journey can only have 1 to %s passangers"
    JourneyIdAlreadyExists = "Journey with id %s already exists"


class StaticParams(Enum):
    MAX_SEAT_NUMBER = 6
    """Only journeys with 6 or less passengers can be served."""
