"""
The domain object models (or data models) contain the main logic of the application.
Through the Car and Journey models the service registers, modifies or removes the
objects storing the parameters received from the API interface.
The models are also responsible for storing and classification of existing domain objects.

Car: represents a car with specified capacity.
Journey: represents the group of people willing to travel by car.
"""

from collections import deque
from typing import Optional

from flask import current_app as app

from .exceptions import (
    DomainObjectAlreadyRegisteredException,
    InvalidCarSeatsParameterException,
    CarNotFoundException,
    JourneyNotFoundException,
    InvalidPassangerNumberParameterException,
)

from .constants import ExceptionMessages, StaticParams


class Car:
    """
    Object properties:
        id: Unique identifier of the car
        max_seats: The maximum number of seats the car has
        free_seats: The number of free seats in the car

    Static properties:
        __storage: Contains the registered car objects in {car.id: Car} format
        __free_seats: Contains the registered car ids in {car.free_seats: [car_ids]} format
    """

    __storage = {}
    __free_seats = {i: deque() for i in range(StaticParams.MAX_SEAT_NUMBER.value + 1)}

    def __init__(self, id: int, seats: int):
        if id in Car.__storage:
            app.logger.debug(ExceptionMessages.CarAlreadyExists.value % id)
            raise DomainObjectAlreadyRegisteredException(
                ExceptionMessages.CarAlreadyExists.value % id
            )
        if seats in [4, 5, 6]:
            """Only cars with capacity of 4, 5 and 6 are allowed"""
            self.id = id
            self.max_seats = seats
            self.free_seats = seats
        else:
            raise InvalidCarSeatsParameterException(
                ExceptionMessages.InvalidNumberOfSeats.value % id
            )

        Car.__storage[id] = self
        Car.__free_seats[seats].append(id)

    @staticmethod
    def get_car_by_seats(seats: int) -> Optional["Car"]:
        """
        Gets a car object from the free_seats storage based on the given seats number.
        If there is no car with the required free capacity, it looks for a higher
        capacity one until it reaches the maximum.
        """
        while seats <= 6:
            if len(Car.__free_seats[seats]) > 0:
                return Car.__storage[Car.__free_seats[seats].pop()]
            else:
                seats += 1
        return None

    @staticmethod
    def get_car_by_id(id: int) -> "Car":
        """
        Returns the Car object represented by the given id, or None if no car was found.
        """
        car = Car.__storage.get(id)
        if car:
            return car
        else:
            raise CarNotFoundException(ExceptionMessages.CarNotFound.value % id)

    @staticmethod
    def lock_car_seats(car: "Car", locked_seats: int):
        """
        If a journey is getting assigned to a car, the used seats need to be locked.

        The car objects free_seats property is updated and will be moved to the lower
        free_seats storage.
        """
        app.logger.debug(
            f"pre: car: {car.id}, locked_seats: {locked_seats}, free_seats: {Car.__free_seats}"
        )
        car.free_seats -= locked_seats
        Car.__free_seats[car.free_seats].append(car.id)
        app.logger.debug(
            f"post: car: {car.id}, locked_seats: {locked_seats}, free_seats: {Car.__free_seats}"
        )

    @staticmethod
    def release_car_seats(car: "Car", released_seats: int):
        """
        The opposite of the lock_car_seats method. Dropped off journeys release
        previously locked seats.

        The car objects free_seats property is updated and will be moved to the higher
        free_seats storage.
        """
        app.logger.debug(
            f"pre: car: {car.id}, released_seats: {released_seats}, free_seats: {Car.__free_seats}"
        )
        Car.__free_seats[car.free_seats].remove(car.id)
        car.free_seats += released_seats
        Car.__free_seats[car.free_seats].append(car.id)
        app.logger.debug(
            f"post: car: {car.id}, released_seats: {released_seats}, free_seats: {Car.__free_seats}"
        )


class Journey:
    """
    Object properties:
        id: Unique identifier of the journey
        passangers: The number of people in the journey
        car_id: The id of the car assigned to the journey

    Static properties:
        __storage: Contains the registered journey objects assigned to cars in
            {journey.id: Journey} format
        __waiting_list: Contains the registered journey objects waiting to be
            assigned to a car. All registered Journey objects are placed here first.
            When a car with proper capacity will be allowed, it will be updated and
            moved to __storage.

    """

    __storage = {}
    __waiting_list = []

    def __init__(self, id: int, passangers: int):
        app.logger.debug(
            f"journey: {id}, {passangers}; Journey.__storage: {Journey.__storage}; Journey.__waiting_list: {Journey.__waiting_list}"
        )

        if passangers > StaticParams.MAX_SEAT_NUMBER.value:
            raise InvalidPassangerNumberParameterException(
                ExceptionMessages.NumberOfPassangersInterval.value
                % StaticParams.MAX_SEAT_NUMBER.value
            )

        if id in Journey.__storage or id in [
            item.id for item in Journey.__waiting_list
        ]:
            raise DomainObjectAlreadyRegisteredException(
                ExceptionMessages.JourneyIdAlreadyExists.value % id
            )
        self.id = int(id)
        self.passangers = passangers
        self.car_id = None

        Journey.__waiting_list.append(self)
        Journey.run_waiting_list()

    @staticmethod
    def run_waiting_list():
        """
        The method handling car assingment on journeys in __waiting_list.
        In most cases no direct call is required, with the run_waiting_list_after
        and run_waiting_list_before decorators it can be called before/after
        executing other functions.
        """
        filled_seats = {
            i: False for i in range(1, StaticParams.MAX_SEAT_NUMBER.value + 1)
        }
        app.logger.debug(f"waiting list beginning: {Journey.__waiting_list}")
        app.logger.debug(
            f"storage beginning: { [{'id':act_item, 'car_id': Journey.__storage[act_item].car_id } for act_item in Journey.__storage ]}"
        )
        for act_journey in Journey.__waiting_list:
            if not filled_seats[act_journey.passangers]:
                car = Car.get_car_by_seats(act_journey.passangers)
                if car is not None:
                    act_journey.car_id = car.id
                    Car.lock_car_seats(car, act_journey.passangers)
                    Journey.__storage[act_journey.id] = act_journey
                    Journey.__waiting_list.remove(act_journey)
                else:
                    filled_seats[act_journey.passangers] = True
        app.logger.debug(f"waiting list end: {Journey.__waiting_list}")
        app.logger.debug(
            f"storage ending: { [{'id':act_item, 'car_id': Journey.__storage[act_item].car_id } for act_item in Journey.__storage ]}"
        )

    @staticmethod
    def get_journey_from_storage_by_id(id):
        """
        Returns the Journey object represented by the given id if in __storage, or None if
        journey was not found.
        """
        try:
            return Journey.__storage[id]
        except KeyError:
            return None

    @staticmethod
    def get_journey_from_waiting_list_by_id(id):
        """
        Returns the Journey object represented by the given id if in __waiting_list, or None if
        journey was not found.

        While looking for a journey by id, the service searches first in the __storage then in
        __waiting_list. If the search in __waiting_list does not return a journey, the journey
        is not in the system, a JourneyNotFoundException can be raised.
        """
        for act_journey in Journey.__waiting_list:
            if act_journey.id == int(id):
                return act_journey
        raise JourneyNotFoundException(ExceptionMessages.JourneyNotFound.value % id)

    def remove_journey(self):
        """
        Removes the journey from both of the storages.
        """
        storage_match = (
            Journey.__storage.pop(self.id) if self.id in Journey.__storage else None
        )
        if not storage_match:
            Journey.__waiting_list.remove(self)
