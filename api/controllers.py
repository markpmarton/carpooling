"""
The controller module contains the access points for the car-pooling API.
I didn't change the API structure described in the README.md, but generalized
the common commands and implemented proper exception handling.
"""
from flask import Response, request

from utils.request_mapper import map_request
from utils.request_mapper.exceptions import (
    RequestMappingException,
    UnhandledContentTypeMappingException,
)
from models.exceptions import (
    DataValidatorException,
    DomainObjectAlreadyRegisteredException,
    InvalidCarSeatsParameterException,
    JourneyNotFoundException,
    CarNotFoundException,
    EmptyCarListException,
)
from models.constants import ExceptionMessages
from models.dto import (
    LocateResponseDTO,
    RegisterJourneyDTO,
    RegisterCarItemDTO,
    DropOffDTO,
    LocateDTO,
)
from .services import CarHandler, JourneyHandler
from .validator import validate


def bind_controllers(app):
    """
    This function is called by the app module to define the API endpoints.
    It returns the modified Flask app object.

    By creating the data transfer objects the automated data type and value
    validation of the parameters is executed (with cerberus).

    Flows different from the optimal execution are forwarded to the controller
    by raising specific Exceptions. The catching of them are separated by the
    HTTP status code to return.

    The additional 500 status code branch never should be called normally.
    If this status code still appear, the logs can provide further info
    about the bug.
    """

    @app.route("/status", methods=["GET"])
    def status_controller():
        """
        Status endpoint to verify the app is running.
        """
        return Response(status=200)

    @app.route("/cars", methods=["PUT"])
    def register_cars_controller():
        """
        Registers a list of car objects based on the JSON list in request.
        From the JSON list the request_mapper creates a list of RegisterCarDTO objects.

        Required Content-Type: application/json
        """
        try:
            car_dto_items = map_request(request, RegisterCarItemDTO)
            if len(car_dto_items) == 0:
                raise EmptyCarListException()
            [validate(act_dto_item) for act_dto_item in car_dto_items]
            CarHandler.register_cars(car_dto_items)
            return Response(status=200)
        except (
            DataValidatorException,
            RequestMappingException,
            UnhandledContentTypeMappingException,
            DomainObjectAlreadyRegisteredException,
            InvalidCarSeatsParameterException,
            EmptyCarListException,
        ) as e:
            app.logger.error(e)
            return Response(status=400)
        except Exception as e:
            app.logger.critical(e)
            return Response(status=500)

    @app.route("/journey", methods=["POST"])
    def journey_controller():
        """
        Registers a journey objects based on the JSON parameters in request.
        From the JSON the request_mapper creates a RegisterJourneyDTO object.

        Required Content-Type: application/json
        """

        try:
            journey_dto = map_request(request, RegisterJourneyDTO)
            validate(journey_dto)
            JourneyHandler.register_journey(journey_dto)
            return Response(status=200)
        except (
            DataValidatorException,
            RequestMappingException,
            UnhandledContentTypeMappingException,
            DomainObjectAlreadyRegisteredException,
        ) as e:
            app.logger.error(e)
            return Response(status=400)
        except Exception as e:
            app.logger.critical(e)
            return Response(status=500)

    @app.route("/dropoff", methods=["POST"])
    def dropoff_controller():
        """
        Removes the already registered journey object if the given id is found.
        If no journey can be found with the given id, status 404 returns.

        From the given form data the request_mapper creates a DropOffDTO object.

        Required Content-Type: application/x-www-form-urlencoded
        """
        try:
            dropoff_dto = map_request(request, DropOffDTO)
            validate(dropoff_dto)
            removed_journey = JourneyHandler.dropoff(dropoff_dto)
            if not removed_journey:
                raise JourneyNotFoundException(
                    ExceptionMessages.JourneyNotFound.value.format(dropoff_dto.ID)
                )
            return Response(status=200)
        except (
            DataValidatorException,
            RequestMappingException,
            UnhandledContentTypeMappingException,
            CarNotFoundException,
        ) as e:
            app.logger.error(e)
            return Response(status=400)
        except JourneyNotFoundException as e:
            app.logger.info(e)
            return Response(status=404)
        except Exception as e:
            app.logger.critical(e)
            return Response(status=500)

    @app.route("/locate", methods=["POST"])
    def locate_controller():
        """
        If the journey with the given id if assigned to a car it returns
        the assigned car object parameters in JSON.
        If no cars were assignes to the journey yet, it returns status 204.
        In case of no journeys can be found with the given id, status 400
        returns.

        From the given form data the request_mapper creates a LocateDTO object.

        Required Content-Type: application/x-www-form-urlencoded
        """
        try:
            locate_dto = map_request(request, LocateDTO)
            validate(locate_dto)
            assigned_car = JourneyHandler.locate(locate_dto)
            if assigned_car:
                response = LocateResponseDTO(
                    id=assigned_car.id, seats=assigned_car.max_seats
                )
                app.logger.debug(f"Returned car: {response}")

                return response.__dict__, 200
            else:
                raise CarNotFoundException(
                    ExceptionMessages.CarForJourneyNotFound.value.format(locate_dto.ID)
                )
        except (
            DataValidatorException,
            RequestMappingException,
            UnhandledContentTypeMappingException,
        ) as e:
            app.logger.error(e)
            return Response(status=400)
        except JourneyNotFoundException as e:
            app.logger.info(e)
            return Response(status=404)
        except CarNotFoundException as e:
            app.logger.error(e)
            return Response(status=204)
        except Exception as e:
            app.logger.critical(e)
            return Response(status=500)

    return app
