"""
Model specific exceptions are raised if the exception is related to
the stored domain data or data validation.
"""
from abc import ABC


class BaseException(Exception, ABC):
    def __init__(self, msg="", thrower=None):
        self.thrower = thrower
        msg_array = [
            self.__class__.__name__,
        ]
        msg_array.append(f"thrower: {self.thrower}") if self.thrower else None
        msg_array.append(
            f"traceback: {str(self.__traceback__)}"
        ) if self.__traceback__ else None
        msg_array.append(str(msg))

        msg = "|".join(msg_array)
        super().__init__(msg)


class DataValidatorException(BaseException):
    pass


class DomainObjectAlreadyRegisteredException(BaseException):
    pass


class InvalidCarSeatsParameterException(BaseException):
    pass


class CarNotFoundException(BaseException):
    pass


class JourneyNotFoundException(BaseException):
    pass


class EmptyCarListException(BaseException):
    pass


class InvalidPassangerNumberParameterException(BaseException):
    pass
