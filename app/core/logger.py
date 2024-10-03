import logging
import sys
from logging import Logger, StreamHandler
from typing import TextIO

logger: Logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler: StreamHandler[TextIO] = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
