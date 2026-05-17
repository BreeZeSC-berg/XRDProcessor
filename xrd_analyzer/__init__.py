# SPDX-License-Identifier: MIT

import logging
import os
import sys

from .log import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

if "QT_API" not in os.environ:
    try:
        import PyQt6.QtCore
    except ImportError:
        pass

from qtpy import QtWidgets, QtGui
from qt_material import apply_stylesheet

try:
    from ._version import version as __version__
except Exception:
    try:
        from importlib.metadata import version as _pkg_version
        __version__ = _pkg_version("xrd_analyzer")
    except Exception:
        __version__ = "0.1.0"

from .paths import resources_path, calibrants_path, icons_path, data_path, style_path
from .excepthook import excepthook
from .controller.MainController import MainController


theme_path = os.path.join(style_path, "light_blue.xml")


_dioptrin_available = False


def _check_dioptrin_license():
    try:
        import dioptrin
        dioptrin.validate_license()
        return True
    except ImportError:
        return False
    except Exception:
        return False


def main():
    global _dioptrin_available

    app = QtWidgets.QApplication([])

    apply_stylesheet(
        app,
        theme=theme_path,
        extra={"density_scale": -2},
    )
    sys.excepthook = excepthook
    logger.info("XRD Analyzer %s", __version__)

    _dioptrin_available = _check_dioptrin_license()

    if len(sys.argv) == 1:
        controller = MainController()
        controller.show_window()
        app.exec_()
    elif sys.argv[1] == "test":
        controller = MainController(use_settings=False)
        controller.show_window()
        app.exec_()
    elif sys.argv[1].startswith("version"):
        print(__version__)

    del app
