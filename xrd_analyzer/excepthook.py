# SPDX-License-Identifier: MIT

import logging
import traceback

from io import StringIO

from .widgets.UtilityWidgets import ErrorMessageBox
from . import __version__
from .log import get_recent_log

logger = logging.getLogger(__name__)


def excepthook(exc_type, exc_value, traceback_obj):
    separator = '-' * 80
    notice = (
        "An unhandled exception occurred. Please report the bug under:\n"
        "\thttps://github.com/xrd-analyzer/issues\n\n"
        "Please include the information below when reporting.\n\n"
    )

    tb_info_file = StringIO()
    traceback.print_tb(traceback_obj, None, tb_info_file)
    tb_info_file.seek(0)
    tb_info = tb_info_file.read()
    errmsg = '%s: \n%s' % (str(exc_type), str(exc_value))

    sections = [
        "XRD Analyzer Version: %s" % __version__,
        separator,
        "Error:",
        errmsg,
        separator,
        "Traceback:",
        tb_info,
    ]

    recent = get_recent_log(50)
    if recent:
        sections.append(separator)
        sections.append("Recent activity log:")
        sections.extend(recent)

    msg = '\n'.join(sections)

    logger.critical(
        "Unhandled exception (XRD Analyzer %s)\n%s", __version__, errmsg,
        exc_info=(exc_type, exc_value, traceback_obj),
    )

    errorbox = ErrorMessageBox()
    errorbox.setText(str(notice) + str(msg))
    errorbox.exec_()
