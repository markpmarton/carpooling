import logging
import os


class LoggerFactory:
    """
    Generic logger factory to return a fully set up logger.

    [Source: https://medium.com/geekculture/create-a-reusable-logger-factory-for-python-projects-419ad408665d]
    """

    @staticmethod
    def __create_logger(log_path, level, working_dir):
        format = "%(asctime)s|%(levelname)s|%(message)s"
        formatter = logging.Formatter(format)

        full_log_path = os.path.join(working_dir, log_path)

        LoggerFactory._level = level
        LoggerFactory._log_path = full_log_path
        LoggerFactory._logger = logging.getLogger("carpool_logger")

        logging.basicConfig(
            level=logging.INFO, format=format, datefmt="%Y-%m-%d %H:%M:%S"
        )

        match level:
            case "INFO":
                LoggerFactory._logger.setLevel(logging.INFO)
            case "ERROR":
                LoggerFactory._logger.setLevel(logging.ERROR)
            case "DEBUG":
                LoggerFactory._logger.setLevel(logging.DEBUG)
            case "WARNING":
                LoggerFactory._logger.setLevel(logging.WARNING)
            case "CRITICAL":
                LoggerFactory._logger.setLevel(logging.CRITICAL)

        file_handler = logging.FileHandler(
            full_log_path, mode="a", encoding="utf-8", delay=False
        )
        file_handler.setLevel(LoggerFactory._logger.level)
        file_handler.setFormatter(formatter)
        LoggerFactory._logger.addHandler(file_handler)

        return LoggerFactory._logger

    @staticmethod
    def get_logger(log_path, log_level, working_dir):
        """
        Passes parameters and returns a generated logger object.
        """
        log_path = log_path
        level = log_level
        working_dir = working_dir
        logger = LoggerFactory.__create_logger(log_path, level, working_dir)
        return logger
