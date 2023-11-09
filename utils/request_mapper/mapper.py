"""
The request mapper handles the direct bind of request data into
DTO objects.
The mapper is implemented with the generic T type to provide 
flexibility for future changes.
The source of input data is decided by the content type of the request.
Currenlty only application/json and application/x-www-form-urlencoded
are supported.
"""

from .exceptions import (
    RequestMappingException,
    UnhandledContentTypeMappingException,
)
from typing import TypeVar, Type

T = TypeVar("T")


def map_request(request, mapping_type: Type[T]) -> T | list[T]:
    match request.content_type:
        case "application/json":
            try:
                if isinstance(request.json, list):
                    return [mapping_type(**item) for item in request.json]
                return mapping_type(**request.json)
            except Exception as e:
                raise RequestMappingException(e)

        case "application/x-www-form-urlencoded":
            parameters = []
            if len(request.form) > 0:
                for act_parameter in request.form:
                    if act_parameter not in mapping_type.__annotations__:
                        raise RequestMappingException(
                            f"Unexpected parameter: {act_parameter}"
                        )
                    if mapping_type.__annotations__[act_parameter] == int:
                        parsed_result = request.form.get(act_parameter, type=int)
                        if not parsed_result:
                            raise RequestMappingException(
                                f"Invalid value: {act_parameter}={request.form.get(act_parameter)}"
                            )
                        else:
                            parameters.append(parsed_result)
                    else:
                        parameters.append(request.form.get(act_parameter))
                return mapping_type(*parameters)
            else:
                raise RequestMappingException(f"Missing form data")

        case unhandled_content_type:
            raise UnhandledContentTypeMappingException(unhandled_content_type)
