# SPDX-License-Identifier: MIT

import os

from qtpy import QtWidgets, QtGui, QtCore

from .ConfigurationWidget import ConfigurationWidget
from .CalibrationWidget import CalibrationWidget
from .MaskWidget import MaskWidget
from .integration import IntegrationWidget
from .MapWidget import MapWidget
from .CustomWidgets import (
    VerticalSpacerItem,
    CheckableFlatButton,
    FlatButton,
    HorizontalLine,
)

from .. import icons_path


class MainWidget(QtWidgets.QWidget):
    """
    XRD Analyzer Main Window - Modern top-tab navigation design.
    Completely different UI from Dioptas while maintaining the same logical
    widget structure for controller compatibility.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("xrd_main_window")

        self._outer_layout = QtWidgets.QVBoxLayout()
        self._outer_layout.setContentsMargins(0, 0, 0, 0)
        self._outer_layout.setSpacing(0)

        self._create_top_navigation_bar()
        self._create_toolbar()
        self._create_content_area()
        self._create_mode_widgets()

        self._outer_layout.addWidget(self._top_nav_bar)
        self._outer_layout.addWidget(self._toolbar_widget)
        self._outer_layout.addWidget(self._content_stack, 100)

        self.setLayout(self._outer_layout)

        self._style_navigation()
        self.add_menu_popup()
        self.add_tooltips()

        self.setWindowIcon(QtGui.QIcon(os.path.join(icons_path, "icon.svg")))

    def _create_top_navigation_bar(self):
        """Create a modern top tab bar for mode switching (replaces left sidebar)."""
        self._top_nav_bar = QtWidgets.QWidget()
        self._top_nav_bar.setObjectName("mode_tab_bar")
        self._top_nav_bar.setFixedHeight(48)

        self._nav_layout = QtWidgets.QHBoxLayout()
        self._nav_layout.setContentsMargins(12, 0, 12, 0)
        self._nav_layout.setSpacing(0)

        # App title
        self._app_title = QtWidgets.QLabel("XRD Analyzer")
        self._app_title.setObjectName("nav_app_title")
        self._app_title.setStyleSheet(
            "color: #FFFFFF; font-weight: bold; font-size: 16px; padding-right: 24px;"
        )
        self._nav_layout.addWidget(self._app_title)

        # Mode buttons (top tabs style)
        self.mode_btn_group = QtWidgets.QButtonGroup()

        self.calibration_mode_btn = CheckableFlatButton("Calibration")
        self.calibration_mode_btn.setObjectName("calibration_mode_btn")
        self.calibration_mode_btn.setChecked(True)

        self.mask_mode_btn = CheckableFlatButton("Mask")
        self.mask_mode_btn.setObjectName("mask_mode_btn")

        self.integration_mode_btn = CheckableFlatButton("Integration")
        self.integration_mode_btn.setObjectName("integration_mode_btn")

        self.map_mode_btn = CheckableFlatButton("Map")
        self.map_mode_btn.setObjectName("map_mode_btn")

        for btn in [self.calibration_mode_btn, self.mask_mode_btn,
                     self.integration_mode_btn, self.map_mode_btn]:
            btn.setFixedHeight(48)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: rgba(255,255,255,0.7);
                    border: none;
                    border-bottom: 3px solid transparent;
                    border-radius: 0px;
                    padding: 12px 20px;
                    font-weight: bold;
                    font-size: 13px;
                    margin: 0 1px;
                }
                QPushButton:checked {
                    color: #FFFFFF;
                    border-bottom: 3px solid #FF6D00;
                    background: rgba(255,255,255,0.1);
                }
                QPushButton:hover:!checked {
                    color: rgba(255,255,255,0.9);
                    background: rgba(255,255,255,0.05);
                }
            """)

        self.mode_btn_group.addButton(self.calibration_mode_btn)
        self.mode_btn_group.addButton(self.mask_mode_btn)
        self.mode_btn_group.addButton(self.integration_mode_btn)
        self.mode_btn_group.addButton(self.map_mode_btn)

        self._nav_layout.addWidget(self.calibration_mode_btn)
        self._nav_layout.addWidget(self.mask_mode_btn)
        self._nav_layout.addWidget(self.integration_mode_btn)
        self._nav_layout.addWidget(self.map_mode_btn)
        self._nav_layout.addStretch()

        # Menu and config buttons on the right side of nav bar
        self.menu_btn = QtWidgets.QPushButton("Project")
        self.menu_btn.setObjectName("nav_menu_btn")
        self.menu_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.15);
                color: #FFFFFF;
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 4px;
                padding: 6px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.25);
            }
        """)

        self.show_configuration_menu_btn = CheckableFlatButton("Config")
        self.show_configuration_menu_btn.setObjectName("show_config_btn")
        self.show_configuration_menu_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.1);
                color: #FFFFFF;
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                margin-left: 6px;
            }
            QPushButton:checked {
                background: #FF6D00;
                border-color: #FF6D00;
            }
            QPushButton:hover:!checked {
                background: rgba(255,255,255,0.2);
            }
        """)
        self.show_configuration_menu_btn.setFixedHeight(32)

        self._nav_layout.addWidget(self.menu_btn)
        self._nav_layout.addWidget(self.show_configuration_menu_btn)

        self._top_nav_bar.setLayout(self._nav_layout)

    def _create_toolbar(self):
        """Create a toolbar with quick-access buttons below the nav bar."""
        self._toolbar_widget = QtWidgets.QWidget()
        self._toolbar_widget.setObjectName("main_toolbar")
        self._toolbar_widget.setFixedHeight(44)

        self._toolbar_layout = QtWidgets.QHBoxLayout()
        self._toolbar_layout.setContentsMargins(12, 4, 12, 4)
        self._toolbar_layout.setSpacing(8)

        self.save_btn = FlatButton("Save Project")
        self.load_btn = FlatButton("Open Project")
        self.reset_btn = FlatButton("Reset")

        for btn in [self.save_btn, self.load_btn, self.reset_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background: #FFFFFF;
                    border: 1px solid #BDBDBD;
                    border-radius: 4px;
                    padding: 5px 14px;
                    color: #424242;
                    font-weight: 500;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: #E3F2FD;
                    border-color: #1565C0;
                }
            """)

        self._toolbar_layout.addWidget(self.save_btn)
        self._toolbar_layout.addWidget(self.load_btn)
        self._toolbar_layout.addWidget(self.reset_btn)

        self._toolbar_layout.addWidget(HorizontalLine())
        self._toolbar_layout.addStretch()

        self._external_actions_layout = QtWidgets.QHBoxLayout()
        self._toolbar_layout.addLayout(self._external_actions_layout)

        self._toolbar_widget.setLayout(self._toolbar_layout)

    def _create_content_area(self):
        """Create the content area that will hold the stacked mode widgets."""
        self._content_stack = QtWidgets.QStackedWidget()
        self._content_stack.setObjectName("content_panel")

        # Configuration widget at top of content (collapsible)
        self.configuration_widget = ConfigurationWidget(self)
        self.configuration_widget.setVisible(False)
        self.configuration_widget.setMaximumHeight(32)

        self._content_inner = QtWidgets.QWidget()
        self._content_inner_layout = QtWidgets.QVBoxLayout()
        self._content_inner_layout.setContentsMargins(0, 0, 0, 0)
        self._content_inner_layout.setSpacing(0)
        self._content_inner_layout.addWidget(self.configuration_widget)

        self.main_frame = QtWidgets.QWidget()
        self._layout_main_frame = QtWidgets.QVBoxLayout()
        self._layout_main_frame.setContentsMargins(0, 0, 0, 0)
        self._layout_main_frame.setSpacing(0)
        self.main_frame.setLayout(self._layout_main_frame)

        self._content_inner_layout.addWidget(self.main_frame, 100)
        self._content_inner.setLayout(self._content_inner_layout)

        self._content_stack.addWidget(self._content_inner)

    def _create_mode_widgets(self):
        """Create all mode widgets and add them to the main frame stack."""
        self.calibration_widget = CalibrationWidget(self)
        self.mask_widget = MaskWidget(self)
        self.integration_widget = IntegrationWidget(self)
        self.map_widget = MapWidget(self)

        self._layout_main_frame.addWidget(self.calibration_widget)
        self._layout_main_frame.addWidget(self.mask_widget)
        self._layout_main_frame.addWidget(self.integration_widget)
        self._layout_main_frame.addWidget(self.map_widget)

        self.mask_widget.setVisible(False)
        self.integration_widget.setVisible(False)
        self.map_widget.setVisible(False)

    def _style_navigation(self):
        """Apply styling to the navigation bar and toolbar."""
        self._top_nav_bar.setStyleSheet("""
            #mode_tab_bar {
                background-color: #1565C0;
                border: none;
                border-bottom: 1px solid #0D47A1;
            }
        """)

        self._toolbar_widget.setStyleSheet("""
            #main_toolbar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E0E0E0;
            }
        """)

    def add_menu_popup(self):
        self.menu_btn.clicked.connect(self.show_menu_popup)

    def show_menu_popup(self):
        widget = MenuPopup(self, [self.load_btn, self.save_btn, self.reset_btn])
        btn = self.menu_btn
        widget.adjustSize()
        position = self.mapToGlobal(
            QtCore.QPoint(btn.x(), btn.y() + btn.height() + 4)
        )
        widget.move(position)
        widget.show()

    def add_tooltips(self):
        self.menu_btn.setToolTip("Project Menu")
        self.show_configuration_menu_btn.setToolTip("Show/Hide Configuration Panel")
        self.calibration_mode_btn.setToolTip("Calibration Mode - Calibrate detector geometry")
        self.mask_mode_btn.setToolTip("Mask Mode - Create and edit masks")
        self.integration_mode_btn.setToolTip(
            "Integration Mode - Integrate images and analyze patterns"
        )
        self.map_mode_btn.setToolTip("Map Mode - 2D mapping and scanning")

    def create_external_actions(self, quick_actions):
        self.external_action_btns = {}
        for action in quick_actions:
            btn = QtWidgets.QPushButton(action["name"])
            btn.setStyleSheet("""
                QPushButton {
                    background: #1565C0;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px 14px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #1976D2;
                }
            """)
            self.external_action_btns[action["name"]] = btn
            self._external_actions_layout.addWidget(btn)


class MenuPopup(QtWidgets.QFrame):
    def __init__(self, parent=None, menu_items=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setObjectName("MenuPopup")
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(0.97)
        self.setFixedWidth(180)
        self.setStyleSheet("""
            QFrame#MenuPopup {
                background: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton {
                background: #FFFFFF;
                border: none;
                border-radius: 4px;
                padding: 10px 16px;
                text-align: left;
                color: #212121;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #E3F2FD;
                color: #1565C0;
            }
        """)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(4, 4, 4, 4)
        self._layout.setSpacing(2)
        self.setLayout(self._layout)

        if menu_items:
            for item in menu_items:
                self._layout.addWidget(item)
