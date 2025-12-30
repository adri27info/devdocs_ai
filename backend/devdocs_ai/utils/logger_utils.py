import logging

from utils.general_utils import GeneralUtils


class LoggerUtils:
    """
    Utility class for configuring and retrieving custom loggers.
    """

    __KEY_LOGGER = "devdocsai_logger"

    def __init__(self, *, key_logger=None):
        """
        Initializes the LoggerUtils instance.

        Args:
            key_logger (str, optional): Custom logger name. If not provided, the
            default logger name ("devdocsai_logger") will be used.
        """
        logger_name = GeneralUtils.use_default_if_none(
            value=key_logger,
            default=self.__KEY_LOGGER
        )
        self.logger = logging.getLogger(logger_name)

    def get_logger(self):
        """
        Retrieves the configured logger instance.

        Returns:
            logging.Logger: The logger instance associated with this utility.
        """
        return self.logger
