import os
import logging
import getpass

logger = logging.getLogger(__name__)


def get_env_variable(name) -> str:
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        logger.info(message)
        return ""


def get_user() -> str:
    return getpass.getuser()
