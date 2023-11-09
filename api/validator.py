"""
Data validator module to validate the parameters in the
data transfer objects.
"""

from cerberus import Validator
from models.exceptions import DataValidatorException


def validate(data_object):
    """
    Receives a DTO and matches its properties with the validation schema.
    """
    validator = Validator()
    result = validator.validate(data_object.__dict__, data_object.validation_schema)
    if result:
        return result
    raise DataValidatorException(validator.errors)
