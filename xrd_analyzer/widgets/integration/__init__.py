# SPDX-License-Identifier: MIT

CLICKED_COLOR = '#1565C0'

from qtpy import QtWidgets, QtCore

from ..UtilityWidgets import FileInfoWidget
from ..EpicsWidgets import MoveStageWidget
from .BatchWidget import BatchWidget

from .CustomWidgets import MouseCurrentAndClickedWidget, MouseUnitCurrentAndClickedWidget
from .control import IntegrationControlWidget
from .display.ImgWidget import IntegrationImgDisplayWidget
from .display.PatternWidget import IntegrationPatternWidget
from .display.StatusWidget import IntegrationStatusWidget


class IntegrationWidget(QtWidgets.QWidget):
    """
    Redesigned Integration Widget for XRD Analyzer.
    Uses a modern 3-panel layout: Image | Controls+Pattern | Status
    with a completely different visual arrangement than Dioptas.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('integration_widget')

        self._create_widgets()
        self._setup_layout()
        self._create_shortcuts()
        self._style_widgets()
        self._setup_additional_widgets()

        self.img_frame_size = QtCore.QSize(400, 500)
        self.img_frame_position = QtCore.QPoint(0, 0)
        self.img_mode = 'Image'

    def _create_widgets(self):
        """Create all sub-widgets."""
        self.integration_image_widget = IntegrationImgDisplayWidget()
        self.integration_control_widget = IntegrationControlWidget()
        self.integration_pattern_widget = IntegrationPatternWidget()
        self.integration_status_widget = IntegrationStatusWidget()

    def _setup_layout(self):
        """Modern 3-panel layout: Image (left) | Controls + Pattern (right) | Status (bottom)."""
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(4, 4, 4, 0)

        # Main horizontal splitter: Image | (Controls + Pattern)
        self.horizontal_splitter = QtWidgets.QSplitter()
        self.horizontal_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.horizontal_splitter.setHandleWidth(3)

        # Left side: Image with vertical splitter (Image display | extra panels)
        self.vertical_splitter_left = QtWidgets.QSplitter()
        self.vertical_splitter_left.setOrientation(QtCore.Qt.Vertical)
        self.vertical_splitter_left.addWidget(self.integration_image_widget)

        # Right side: Controls on top, Pattern on bottom
        self.vertical_splitter = QtWidgets.QSplitter()
        self.vertical_splitter.setOrientation(QtCore.Qt.Vertical)
        self.vertical_splitter.addWidget(self.integration_control_widget)
        self.vertical_splitter.addWidget(self.integration_pattern_widget)

        self.vertical_splitter.setStretchFactor(0, 2)
        self.vertical_splitter.setStretchFactor(1, 8)

        self.horizontal_splitter.addWidget(self.vertical_splitter_left)
        self.horizontal_splitter.addWidget(self.vertical_splitter)

        # Default ratio: image 55%, right panel 45%
        self.horizontal_splitter.setSizes([550, 450])

        self._layout.addWidget(self.horizontal_splitter, 10)
        self._layout.addWidget(self.integration_status_widget, 0)
        self.setLayout(self._layout)

    def _style_widgets(self):
        """Apply theme-specific styling."""
        self.setStyleSheet("""
            #integration_widget {
                background-color: #FAFAFA;
            }
            QSplitter::handle {
                background-color: #E0E0E0;
            }
            QSplitter::handle:hover {
                background-color: #1565C0;
            }
        """)

        # Hide some elements that are duplicated or not needed in new layout
        self.bkg_image_scale_sb.setKeyboardTracking(False)
        self.bkg_image_offset_sb.setKeyboardTracking(False)
        self.qa_bkg_pattern_inspect_btn.setVisible(False)
        self.mask_transparent_cb.setVisible(False)

    def _setup_additional_widgets(self):
        """Set up file info, move stage, and batch widgets as floating panels."""
        self.file_info_widget = FileInfoWidget(self)
        self.move_widget = MoveStageWidget(self)
        self.batch_widget = BatchWidget(self)

    def _create_shortcuts(self):
        """Create shortcuts to deeply nested widgets for controller access.
        These MUST match the names expected by the controllers.
        """
        # --- Image control shortcuts ---
        img_control_widget = self.integration_control_widget.img_control_widget.file_widget
        self.image_control_widget = img_control_widget
        self.load_img_btn = img_control_widget.load_btn
        self.autoprocess_cb = img_control_widget.file_cb
        self.img_step_file_widget = img_control_widget.step_file_widget
        self.img_step_series_widget = img_control_widget.step_series_widget
        self.img_filename_txt = img_control_widget.file_txt
        self.img_directory_txt = img_control_widget.directory_txt
        self.img_directory_btn = img_control_widget.directory_btn
        self.file_info_btn = self.integration_control_widget.img_control_widget.file_info_btn
        self.move_btn = self.integration_control_widget.img_control_widget.move_btn
        self.move_widget_btn = self.integration_control_widget.img_control_widget.move_btn

        # Batch mode radio buttons
        icw = self.integration_control_widget.img_control_widget
        self.img_batch_mode_integrate_rb = icw.batch_mode_integrate_rb
        self.img_batch_mode_add_rb = icw.batch_mode_add_rb
        self.img_batch_mode_average_rb = icw.batch_mode_average_rb
        self.img_batch_mode_image_save_rb = icw.batch_mode_image_save_rb

        # --- Pattern control shortcuts ---
        pattern_file_widget = self.integration_control_widget.pattern_control_widget.file_widget
        self.pattern_load_btn = pattern_file_widget.load_btn
        self.pattern_autocreate_cb = pattern_file_widget.file_cb
        self.pattern_previous_btn = pattern_file_widget.step_file_widget.previous_btn
        self.pattern_next_btn = pattern_file_widget.step_file_widget.next_btn
        self.pattern_browse_step_txt = pattern_file_widget.step_file_widget.step_txt
        self.pattern_browse_by_name_rb = pattern_file_widget.step_file_widget.browse_by_name_rb
        self.pattern_browse_by_time_rb = pattern_file_widget.step_file_widget.browse_by_time_rb
        self.pattern_filename_txt = pattern_file_widget.file_txt
        self.pattern_directory_txt = pattern_file_widget.directory_txt
        self.pattern_directory_btn = pattern_file_widget.directory_btn

        pciw = self.integration_control_widget.pattern_control_widget
        self.pattern_header_xy_cb = pciw.xy_cb
        self.pattern_header_chi_cb = pciw.chi_cb
        self.pattern_header_dat_cb = pciw.dat_cb
        self.pattern_header_fxye_cb = pciw.fxye_cb
        self.pattern_headers = [
            self.pattern_header_xy_cb,
            self.pattern_header_chi_cb,
            self.pattern_header_dat_cb,
            self.pattern_header_fxye_cb,
        ]

        # --- Phase control shortcuts ---
        phase_control_widget = self.integration_control_widget.phase_control_widget
        self.phase_widget = phase_control_widget
        self.phase_add_btn = phase_control_widget.add_btn
        self.phase_edit_btn = phase_control_widget.edit_btn
        self.phase_del_btn = phase_control_widget.delete_btn
        self.phase_clear_btn = phase_control_widget.clear_btn
        self.phase_save_list_btn = phase_control_widget.save_list_btn
        self.phase_load_list_btn = phase_control_widget.load_list_btn
        self.phase_tw = phase_control_widget.phase_tw
        self.phase_pressure_step_msb = phase_control_widget.pressure_step_msb
        self.phase_temperature_step_msb = phase_control_widget.temperature_step_msb
        self.phase_apply_to_all_cb = phase_control_widget.apply_to_all_cb

        # --- Overlay control shortcuts ---
        overlay_control_widget = self.integration_control_widget.overlay_control_widget
        self.overlay_widget = overlay_control_widget
        self.overlay_add_btn = overlay_control_widget.add_btn
        self.overlay_del_btn = overlay_control_widget.delete_btn
        self.overlay_clear_btn = overlay_control_widget.clear_btn
        self.overlay_move_up_btn = overlay_control_widget.move_up_btn
        self.overlay_move_down_btn = overlay_control_widget.move_down_btn
        self.overlay_tw = overlay_control_widget.overlay_tw
        self.overlay_scale_step_msb = overlay_control_widget.scale_step_msb
        self.overlay_offset_step_msb = overlay_control_widget.offset_step_msb
        self.waterfall_separation_msb = overlay_control_widget.waterfall_separation_msb
        self.waterfall_btn = overlay_control_widget.waterfall_btn
        self.reset_waterfall_btn = overlay_control_widget.waterfall_reset_btn
        self.overlay_set_as_bkg_btn = overlay_control_widget.set_as_bkg_btn

        # --- Corrections shortcuts ---
        corrections_control_widget = self.integration_control_widget.corrections_control_widget
        self.cbn_groupbox = corrections_control_widget.cbn_seat_gb
        self.cbn_param_tw = corrections_control_widget.cbn_param_tw
        self.cbn_plot_btn = corrections_control_widget.cbn_seat_plot_btn
        self.oiadac_groupbox = corrections_control_widget.oiadac_gb
        self.oiadac_param_tw = corrections_control_widget.oiadac_param_tw
        self.oiadac_plot_btn = corrections_control_widget.oiadac_plot_btn
        self.transfer_gb = corrections_control_widget.transfer_gb
        self.transfer_load_original_btn = corrections_control_widget.transfer_load_original_btn
        self.transfer_load_response_btn = corrections_control_widget.transfer_load_response_btn
        self.transfer_plot_btn = corrections_control_widget.transfer_plot_btn
        self.transfer_original_filename_lbl = corrections_control_widget.transfer_original_filename_lbl
        self.transfer_response_filename_lbl = corrections_control_widget.transfer_response_filename_lbl
        self.slab_groupbox = corrections_control_widget.slab_gb
        self.slab_formula_txt = corrections_control_widget.slab_formula_txt
        self.slab_param_tw = corrections_control_widget.slab_param_tw
        self.slab_mu_lbl = corrections_control_widget.slab_mu_lbl
        self.slab_plot_btn = corrections_control_widget.slab_plot_btn
        self.cylinder_groupbox = corrections_control_widget.cylinder_gb
        self.cylinder_formula_txt = corrections_control_widget.cylinder_formula_txt
        self.cylinder_param_tw = corrections_control_widget.cylinder_param_tw
        self.cylinder_container_formula_txt = corrections_control_widget.cylinder_container_formula_txt
        self.cylinder_container_param_tw = corrections_control_widget.cylinder_container_param_tw
        self.cylinder_mu_lbl = corrections_control_widget.cylinder_mu_lbl
        self.cylinder_plot_btn = corrections_control_widget.cylinder_plot_btn
        self.sphere_groupbox = corrections_control_widget.sphere_gb
        self.sphere_formula_txt = corrections_control_widget.sphere_formula_txt
        self.sphere_param_tw = corrections_control_widget.sphere_param_tw
        self.sphere_mu_lbl = corrections_control_widget.sphere_mu_lbl
        self.sphere_plot_btn = corrections_control_widget.sphere_plot_btn
        self.plate_groupbox = corrections_control_widget.plate_gb
        self.plate_formula_txt = corrections_control_widget.plate_formula_txt
        self.plate_param_tw = corrections_control_widget.plate_param_tw
        self.plate_mu_lbl = corrections_control_widget.plate_mu_lbl
        self.plate_plot_btn = corrections_control_widget.plate_plot_btn
        self.flat_field_gb = corrections_control_widget.flat_field_gb
        self.flat_field_load_btn = corrections_control_widget.flat_field_load_btn
        self.flat_field_filename_lbl = corrections_control_widget.flat_field_filename_lbl
        self.flat_field_plot_btn = corrections_control_widget.flat_field_plot_btn

        # --- Background shortcuts ---
        background_control_widget = self.integration_control_widget.background_control_widget
        self.bkg_image_load_btn = background_control_widget.load_image_btn
        self.bkg_image_filename_lbl = background_control_widget.filename_lbl
        self.bkg_image_delete_btn = background_control_widget.remove_image_btn
        self.bkg_image_scale_sb = background_control_widget.scale_sb
        self.bkg_image_scale_step_msb = background_control_widget.scale_step_msb
        self.bkg_image_offset_sb = background_control_widget.offset_sb
        self.bkg_image_offset_step_msb = background_control_widget.offset_step_msb
        self.bkg_pattern_gb = background_control_widget.pattern_background_gb
        self.bkg_pattern_smooth_width_sb = background_control_widget.smooth_with_sb
        self.bkg_pattern_iterations_sb = background_control_widget.iterations_sb
        self.bkg_pattern_poly_order_sb = background_control_widget.poly_order_sb
        self.bkg_pattern_x_min_txt = background_control_widget.x_range_min_txt
        self.bkg_pattern_x_max_txt = background_control_widget.x_range_max_txt
        self.bkg_pattern_inspect_btn = background_control_widget.inspect_btn
        self.bkg_pattern_save_btn = background_control_widget.save_btn
        self.bkg_pattern_as_overlay_btn = background_control_widget.as_overlay

        # --- Options shortcuts ---
        options_control_widget = self.integration_control_widget.integration_options_widget
        self.bin_count_txt = options_control_widget.bin_count_txt
        self.automatic_binning_cb = options_control_widget.bin_count_cb
        self.correct_solid_angle_cb = options_control_widget.correct_solid_angle_cb
        self.supersampling_sb = options_control_widget.supersampling_sb
        self.oned_full_range_btn = options_control_widget.oned_full_toggle_btn
        self.oned_azimuth_min_txt = options_control_widget.oned_azimuth_min_txt
        self.oned_azimuth_max_txt = options_control_widget.oned_azimuth_max_txt

        # --- Status / Mouse position shortcuts ---
        isw = self.integration_status_widget
        self.mouse_x_lbl = isw.mouse_pos_widget.cur_pos_widget.x_pos_lbl
        self.mouse_y_lbl = isw.mouse_pos_widget.cur_pos_widget.y_pos_lbl
        self.mouse_int_lbl = isw.mouse_pos_widget.cur_pos_widget.int_lbl
        self.click_x_lbl = isw.mouse_pos_widget.clicked_pos_widget.x_pos_lbl
        self.click_y_lbl = isw.mouse_pos_widget.clicked_pos_widget.y_pos_lbl
        self.click_int_lbl = isw.mouse_pos_widget.clicked_pos_widget.int_lbl
        self.mouse_tth_lbl = isw.mouse_unit_widget.cur_unit_widget.tth_lbl
        self.mouse_q_lbl = isw.mouse_unit_widget.cur_unit_widget.q_lbl
        self.mouse_d_lbl = isw.mouse_unit_widget.cur_unit_widget.d_lbl
        self.mouse_azi_lbl = isw.mouse_unit_widget.cur_unit_widget.azi_lbl
        self.click_tth_lbl = isw.mouse_unit_widget.clicked_unit_widget.tth_lbl
        self.click_q_lbl = isw.mouse_unit_widget.clicked_unit_widget.q_lbl
        self.click_d_lbl = isw.mouse_unit_widget.clicked_unit_widget.d_lbl
        self.click_azi_lbl = isw.mouse_unit_widget.clicked_unit_widget.azi_lbl
        self.bkg_name_lbl = isw.bkg_name_lbl

        # --- Pattern widget shortcuts ---
        pw = self.integration_pattern_widget
        self.qa_save_pattern_btn = pw.save_pattern_btn
        self.qa_set_as_overlay_btn = pw.as_overlay_btn
        self.qa_set_as_background_btn = pw.as_bkg_btn
        self.load_calibration_btn = pw.load_calibration_btn
        self.calibration_lbl = pw.calibration_lbl
        self.pattern_tth_btn = pw.tth_btn
        self.pattern_q_btn = pw.q_btn
        self.pattern_d_btn = pw.d_btn
        self.qa_bkg_pattern_btn = pw.background_btn
        self.qa_bkg_pattern_inspect_btn = pw.background_inspect_btn
        self.set_wavelnegth_btn = pw.set_wavelength_btn
        self.wavelength_lbl = pw.wavelength_lbl
        self.antialias_btn = pw.antialias_btn
        self.pattern_log_btn = pw.log_btn
        self.pattern_sqrt_btn = pw.sqrt_btn
        self.pattern_auto_range_btn = pw.auto_range_btn
        self.pattern_widget = pw.pattern_view

        # --- Image widget shortcuts ---
        iw = self.integration_image_widget
        self.qa_save_img_btn = iw.save_image_btn
        self.img_frame = iw
        self.img_roi_btn = iw.roi_btn
        self.img_mode_btn = iw.mode_btn
        self.img_mask_btn = iw.mask_btn
        self.img_phases_btn = iw.phases_btn
        self.cake_shift_azimuth_sl = iw.cake_shift_azimuth_sl
        self.mask_transparent_cb = iw.transparent_cb
        self.img_autoscale_btn = iw.autoscale_btn
        self.img_dock_btn = iw.undock_btn
        self.img_widget = iw.img_view
        self.cake_widget = iw.cake_view
        self.img_show_background_subtracted_btn = iw.show_background_subtracted_img_btn

        # --- Frame image position widget ---
        self.frame_img_positions_widget = self.integration_image_widget.position_and_unit_widget
        self.tabWidget = self.integration_control_widget

        # --- Image mouse position shortcuts ---
        self.img_widget_mouse_x_lbl = iw.mouse_pos_widget.cur_pos_widget.x_pos_lbl
        self.img_widget_mouse_y_lbl = iw.mouse_pos_widget.cur_pos_widget.y_pos_lbl
        self.img_widget_mouse_int_lbl = iw.mouse_pos_widget.cur_pos_widget.int_lbl
        self.img_widget_click_x_lbl = iw.mouse_pos_widget.clicked_pos_widget.x_pos_lbl
        self.img_widget_click_y_lbl = iw.mouse_pos_widget.clicked_pos_widget.y_pos_lbl
        self.img_widget_click_int_lbl = iw.mouse_pos_widget.clicked_pos_widget.int_lbl
        self.img_widget_mouse_tth_lbl = iw.mouse_unit_widget.cur_unit_widget.tth_lbl
        self.img_widget_mouse_q_lbl = iw.mouse_unit_widget.cur_unit_widget.q_lbl
        self.img_widget_mouse_d_lbl = iw.mouse_unit_widget.cur_unit_widget.d_lbl
        self.img_widget_mouse_azi_lbl = iw.mouse_unit_widget.cur_unit_widget.azi_lbl
        self.img_widget_click_tth_lbl = iw.mouse_unit_widget.clicked_unit_widget.tth_lbl
        self.img_widget_click_q_lbl = iw.mouse_unit_widget.clicked_unit_widget.q_lbl
        self.img_widget_click_d_lbl = iw.mouse_unit_widget.clicked_unit_widget.d_lbl
        self.img_widget_click_azi_lbl = iw.mouse_unit_widget.clicked_unit_widget.azi_lbl

        self.footer_img_mouse_position_widget = isw.mouse_pos_widget
        self.change_view_btn = isw.change_view_btn

    def switch_to_cake(self):
        self.img_widget.img_view_box.setAspectLocked(False)
        self.img_widget.activate_vertical_line()

    def switch_to_img(self):
        self.img_widget.img_view_box.setAspectLocked(True)
        self.img_widget.deactivate_vertical_line()

    def dock_img(self, bool_value):
        if not bool_value:
            self.img_dock_btn.setText('Dock')
            self.horizontal_splitter_state = self.horizontal_splitter.saveState()
            self.vertical_splitter_left_state = self.vertical_splitter_left.saveState()

            self.img_frame.setParent(self)
            self.img_frame.setWindowFlags(
                QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint |
                QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint
            )
            self.frame_img_positions_widget.show()
            self.img_frame.resize(self.img_frame_size)
            self.img_frame.move(self.img_frame_position)
            self.footer_img_mouse_position_widget.hide()
            self.img_frame.show()
        elif bool_value:
            self.img_dock_btn.setText('Undock')
            self.img_frame_size = self.img_frame.size()
            self.img_frame_position = self.img_frame.pos()

            self.footer_img_mouse_position_widget.show()
            self.frame_img_positions_widget.hide()

            self.img_frame.setParent(self.vertical_splitter_left)
            self.vertical_splitter_left.insertWidget(1, self.img_frame)

            self.horizontal_splitter.restoreState(self.horizontal_splitter_state)
            self.vertical_splitter_left.restoreState(self.vertical_splitter_left_state)

    def get_progress_dialog(self, message, abort_text, num_points):
        progress_dialog = QtWidgets.QProgressDialog(
            message, abort_text, 0, num_points, self
        )
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        pos = self.pattern_widget.pg_layout.mapToGlobal(
            self.pattern_widget.pg_layout.rect().center()
        )
        progress_dialog.move(
            int(pos.x() - progress_dialog.size().width() / 2.0),
            int(pos.y() - progress_dialog.size().height() / 2.0),
        )
        progress_dialog.show()
        return progress_dialog

    def show_error_msg(self, msg):
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowFlags(QtCore.Qt.Tool)
        msg_box.setText(msg)
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle('Error')
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()
