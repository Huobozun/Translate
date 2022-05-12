import functools
import logging
import time
from stopwatch import Stopwatch

logger = logging.getLogger(__name__)


class trace_time_elapsed:
    def __init__(self, logger: logging.Logger, log_level=logging.INFO):
        self.func_logger = logger
        self.log_level = log_level

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            stopwatch = Stopwatch()
            logger.log(
                self.log_level,
                f"[{self.func_logger.name}] function:{func.__name__} started",
            )
            stopwatch.start()
            result = func(*args, **kwargs)
            stopwatch.stop()
            logger.log(
                self.log_level,
                f"[{self.func_logger.name}] function:{func.__name__} finished",
            )
            elapsed = "{:.3f}".format(stopwatch.elapsed)
            logger.log(
                self.log_level,
                f"[{self.func_logger.name}] run function:{func.__name__}  take {elapsed} secs",
            )
            return result

        return wrapper


class min_exe_time:
    def __init__(self, logger: logging.Logger, log_level=logging.INFO, secs: float = 0):
        self.func_logger = logger
        self.log_level = log_level
        self.secs = secs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            stopwatch = Stopwatch()
            logger.log(
                self.log_level,
                f"[{self.func_logger.name}] function:{func.__name__} started",
            )
            stopwatch.start()
            result = func(*args, **kwargs)
            logger.log(
                self.log_level,
                f"[{self.func_logger.name}] function:{func.__name__} finished",
            )
            elapsed = "{:.3f}".format(stopwatch.elapsed)
            logger.log(
                self.log_level,
                f"[{self.func_logger.name}] run function:{func.__name__}  take {elapsed} secs",
            )
            stopwatch.stop()
            time_to_sleep = self.secs - stopwatch.elapsed
            if time_to_sleep > 0:
                logger.info(
                    f"[{self.func_logger.name}] function:{func.__name__} sleep {time_to_sleep} secs"
                )
                time.sleep(time_to_sleep)
            return result

        return wrapper
