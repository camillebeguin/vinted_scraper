##### Imports
import json
import logging
import sys
import os

DEV_MODE = os.environ.get("DEV_MODE", "").upper() == "TRUE"

#### Log formatter to ease development and debugging
class HybridLogFormatter(logging.Formatter):
    """Declare a new logging formatter."""

    # The background is set with 40 plus the number of the color,
    # and the foreground with 30
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    BASE = 30

    # These are the sequences need to get colored ouput
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"
    BOLD_SEQ = "\033[1m"
    COLORS = {
        "WARNING": YELLOW,
        "INFO": CYAN,
        "DEBUG": BLUE,
        "CRITICAL": RED,
        "ERROR": RED,
    }

    MAX_NAME_LENGTH = 30

    def format(self, record):
        date = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        levelname = record.levelname
        message = record.getMessage()
        name = record.name

        if not DEV_MODE:
            log = json.dumps(
                {
                    "severity": levelname,
                    "message": message,
                    "name": record.name,
                    "timestamp": date,
                }
            )
        else:
            color = self.COLORS.get(levelname, "INFO")
            name = name[: self.MAX_NAME_LENGTH - 3] + (
                "..."
                if name[self.MAX_NAME_LENGTH :]
                else name[self.MAX_NAME_LENGTH - 3 :]
            )
            name = name.ljust(self.MAX_NAME_LENGTH)
            log = f"{self.COLOR_SEQ % (self.BASE + color)}[{date}][{name}] {levelname.ljust(8)} {message}{self.RESET_SEQ}"

        return log


class _MaxLevelFilter(object):
    def __init__(self, highest_log_level):
        self._highest_log_level = highest_log_level

    def filter(self, log_record):
        return log_record.levelno <= self._highest_log_level


class _ApplicationFilter(object):
    def __init__(self, app_name):
        self.app_name = app_name

    def filter(self, log_record):
        return (
            log_record.name.startswith(self.app_name) or log_record.name == "__main__"
        )

# A handler for low level logs that should be sent to STDOUT
info_handler = logging.StreamHandler(sys.stdout)
info_handler.setLevel(logging.DEBUG)
info_handler.addFilter(_MaxLevelFilter(logging.WARNING))
info_handler.addFilter(_ApplicationFilter(__name__.split(".")[0]))

# A handler for high level logs that should be sent to STDERR
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.ERROR)

# Json formatter
formatter = HybridLogFormatter()
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

logging.basicConfig(level="DEBUG", handlers=[info_handler, error_handler])

logger = logging.getLogger(__name__)