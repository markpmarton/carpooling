"""
Generates the configuration object based on which
ConfigType was selected in the main.py file.
"""

from enum import Enum
from .types import DevelopmentConfig, ProductionConfig, TestingConfig, BaseConfig
from .exceptions import InvalidConfigTypeException


class ConfigType(Enum):
    """Enum for config types."""

    Development = "Development"
    Production = "Production"
    Testing = "Testing"


class ConfigFactory:
    """Factory for creating config objects."""

    @staticmethod
    def create_config(config_type: ConfigType):
        match config_type:
            case ConfigType.Development:
                return DevelopmentConfig()
            case ConfigType.Production:
                return ProductionConfig()
            case ConfigType.Testing:
                return TestingConfig()
            case invalid_config_type:
                raise InvalidConfigTypeException(invalid_config_type)


def get_config_class_full_namespace(config: BaseConfig):
    """
    Returns the full namespace of the config class.
    """
    return f"{config.__module__}.{config.__class__.__name__}"


def create_config(config_type: ConfigType):
    """
    Returns the generated config object.
    """
    return ConfigFactory.create_config(config_type)
