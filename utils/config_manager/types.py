"""
Config definitions that can be used.
"""
from abc import ABC


class BaseConfig(ABC):
    DEBUG = False
    TESTING = False
    HOST = "0.0.0.0"
    PORT = 8080
    LOG_WORKING_DIR = "logs"
    LOG_FILE = "log.log"
    LOG_LEVEL = "INFO"


class ProductionConfig(BaseConfig):
    LOG_FILE = "prod.log"
    LOG_LEVEL = "ERROR"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOG_FILE = "dev.log"
    LOG_LEVEL = "DEBUG"


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    LOG_FILE = "test.log"
    LOG_LEVEL = "DEBUG"
