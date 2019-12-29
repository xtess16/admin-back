from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def log_err(err):
    if settings.DEBUG:
        logger.error(err)
