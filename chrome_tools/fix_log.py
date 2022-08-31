import structlog
import logging

def set_arsenic_log_level(level=logging.FATAL):
    logger = logging.getLogger('arsenic')
    logger.setLevel(logging.FATAL)

    def logger_factory():
        return logger

    structlog.configure(logger_factory=logger_factory)



