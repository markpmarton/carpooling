"""
The service handlers execute the logic to provide result for the controller.
For this it uses the domain object properties and methods.

The Car and Journey functons are separated to give the possibility to run
the in separate services.
"""

from typing import Optional
from flask import current_app as app

from .decorators import run_waiting_list_after, run_waiting_list_before

from models.data import Car, Journey
from models.dto import LocateDTO, RegisterCarsDTO, RegisterJourneyDTO, DropOffDTO


class CarHandler:
    @staticmethod
    @run_waiting_list_after
    def register_cars(register_car_items: RegisterCarsDTO) -> list[Car]:
        car_objects = [Car(id=item.id, seats=item.seats) for item in register_car_items]
        return car_objects


class JourneyHandler:
    @staticmethod
    @run_waiting_list_before
    def register_journey(register_journey_dto: RegisterJourneyDTO) -> Journey:
        journey_object = Journey(
            id=register_journey_dto.id, passangers=register_journey_dto.people
        )
        return journey_object

    @staticmethod
    @run_waiting_list_after
    def dropoff(drop_off_dto: DropOffDTO) -> Journey:
        journey = Journey.get_journey_from_storage_by_id(drop_off_dto.ID)
        if journey:
            car = Car.get_car_by_id(journey.car_id)
            Car.release_car_seats(car, journey.passangers)
        else:
            journey = Journey.get_journey_from_waiting_list_by_id(drop_off_dto.ID)

        journey.remove_journey()
        return journey

    @staticmethod
    def locate(locate_dto: LocateDTO) -> Optional[Car]:
        journey = Journey.get_journey_from_storage_by_id(locate_dto.ID)
        if not journey:
            journey = Journey.get_journey_from_waiting_list_by_id(locate_dto.ID)
        else:
            return Car.get_car_by_id(journey.car_id)
