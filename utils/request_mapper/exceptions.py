"""
Request mapping specific exceptions.
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


class RequestMappingException(BaseException):
    pass


class UnhandledContentTypeMappingException(BaseException):
    pass


class JsonMappingException(BaseException):
    pass
