import structlog
import logging

def set_arsenic_log_level():
    logger = logging.getLogger('arsenic')
    logger.setLevel(logging.FATAL)
    logging.disable()

    def logger_factory():
        return logger

    structlog.configure(logger_factory=logger_factory)



