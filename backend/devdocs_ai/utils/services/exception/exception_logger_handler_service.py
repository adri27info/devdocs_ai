from utils.logger_utils import LoggerUtils

LOGGER = LoggerUtils().get_logger()


class ExceptionLoggerHandlerService:
    """
    Service to log exceptions and optionally re-raise them.
    """

    @staticmethod
    def run(*, message=None, exc=None, raise_exception=False):
        """
        Log the exception and optionally raise it.

        Args:
            message (str, optional): Custom message to log and raise.
            exc (Exception, optional): Exception instance to log.
            raise_exception (bool, optional): Whether to raise the exception after logging.
        """
        if not exc:
            LOGGER.info("No exception found")
            return

        log_func = LOGGER.info if exc.__class__.__name__ != "Exception" else LOGGER.error

        if message:
            log_func(message)
            if raise_exception:
                raise Exception(message) from exc
        else:
            log_func(str(exc))
            if raise_exception:
                raise Exception(str(exc)) from exc
