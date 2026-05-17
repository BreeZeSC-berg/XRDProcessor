# SPDX-License-Identifier: MIT

import collections
import logging
import os
import sys


_configured = False

_BUFFER_SIZE = 200


class RecentLogHandler(logging.Handler):
    def __init__(self, maxlen=_BUFFER_SIZE):
        super().__init__()
        self.records = collections.deque(maxlen=maxlen)

    def emit(self, record):
        self.records.append(self.format(record))

    def get_recent(self, n=None):
        if n is None:
            return list(self.records)
        return list(self.records)[-n:]


_recent_handler = None


def get_recent_log(n=50):
    if _recent_handler is None:
        return []
    return _recent_handler.get_recent(n)


def setup_logging(level=None):
    global _configured, _recent_handler
    if _configured:
        return
    _configured = True

    if level is None:
        level = os.environ.get("XRD_LOG_LEVEL", "WARNING")

    root = logging.getLogger("xrd_analyzer")
    root.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stderr)
    console.setLevel(level)
    console.setFormatter(fmt)
    root.addHandler(console)

    _recent_handler = RecentLogHandler(maxlen=_BUFFER_SIZE)
    _recent_handler.setLevel(logging.DEBUG)
    _recent_handler.setFormatter(fmt)
    root.addHandler(_recent_handler)

    log_file = os.environ.get("XRD_LOG_FILE")
    if log_file:
        try:
            from logging.handlers import RotatingFileHandler
            os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
            file_handler = RotatingFileHandler(
                log_file, maxBytes=5 * 1024 * 1024, backupCount=3
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(fmt)
            root.addHandler(file_handler)
        except OSError:
            root.warning("Could not open log file %s for writing", log_file)
