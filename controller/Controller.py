from PyQt4 import QtGui, QtCore
import cv2
import copy
import ConfigParser
import os

class Controller(object):
    def __init__(self, ui):
        self._ui = ui

        self.preset_options()
        self.track_file = ""
        self.last_selected_folder = "/home"

        self.output_directory = ""
        self.output_is_input = False

        # ROI variables
        self.first_frame_numpy = None
        self.roi_preview_draw_numpy = None
        self.preview_is_set = False
        self.roi_preview_displayed = False
        return

    def browse_file(self):
        self.roi_preview_displayed = False

        self.track_file = QtGui.QFileDialog.getOpenFileName(self.ui, 'Open file', self.last_selected_folder)
        if self.track_file == "":
            return
        self.ui.tab_file.lnEdit_file_path.setText(self.track_file)

        self.set_first_frame_numpy()
        self.display_roi_preview()
        # self.display_starting_area_preview()

    def set_first_frame_numpy(self):
        cap = cv2.VideoCapture(str(self.track_file))

        while cap.isOpened():
            ret, frame = cap.read()
            if frame is not None:
                self.first_frame_numpy = frame
                # cv2.imshow("roi preview", frame)
                break
        cap.release()

        self.preview_is_set = True

    def display_roi_preview(self):
        roi = self.ui.tracker.roim.get_roi("tracking_area")
        self.roi_preview_draw_numpy = copy.copy(self.first_frame_numpy)
        cv2.rectangle(self.roi_preview_draw_numpy, (roi.x1, roi.y1), (roi.x2, roi.y2), (255, 0, 255), 2)
        if self.roi_preview_displayed:
            cv2_output = copy.copy(self.first_frame_numpy[roi.y1:roi.y2, roi.x1:roi.x2])
            cv2.imshow("roi preview", cv2_output)
        # convert numpy-array to qimage
        output_qimg = QtGui.QImage(self.roi_preview_draw_numpy, self.first_frame_numpy.shape[1], self.first_frame_numpy.shape[0], QtGui.QImage.Format_RGB888)
        output_pixm = QtGui.QPixmap.fromImage(output_qimg)
        # fit picture to window size
        width = self.ui.tab_widget_options.geometry().width() - 20
        height = int(width)
        size = QtCore.QSize(width, height)
        output_pixm_rescaled = output_pixm.scaled(size, QtCore.Qt.KeepAspectRatio)
        # display picture
        self.ui.tab_roi.lbl_roi_preview_label.setPixmap(output_pixm_rescaled)
        self.roi_preview_displayed = True

    def preset_options(self):
        # video file
        # self.lnEdit_file_path.setText(self.tracker.video_file)
        self.ui.tab_file.cbx_enable_nix_output.setChecked(self.ui.tracker.nix_io)

        # meta
        self.ui.tab_meta.ln_edit_experimenter.setText(self.ui.tracker.mm.experimenter)
        self.ui.tab_meta.ln_edit_fish_id.setText(self.ui.tracker.mm.fish_id)

        # region of interest
        self.ui.tab_roi.spinBox_roi_x1.setValue(self.ui.tracker.roim.get_roi("tracking_area").x1)
        self.ui.tab_roi.spinBox_roi_x2.setValue(self.ui.tracker.roim.get_roi("tracking_area").x2)
        self.ui.tab_roi.spinBox_roi_y1.setValue(self.ui.tracker.roim.get_roi("tracking_area").y1)
        self.ui.tab_roi.spinBox_roi_y2.setValue(self.ui.tracker.roim.get_roi("tracking_area").y2)
        self.ui.tab_roi.spinBox_roi_x1.setMaximum(self.ui.tab_roi.spinBox_roi_x2.value()-1)
        self.ui.tab_roi.spinBox_roi_x2.setMinimum(self.ui.tab_roi.spinBox_roi_x1.value()+1)
        self.ui.tab_roi.spinBox_roi_y1.setMaximum(self.ui.tab_roi.spinBox_roi_y2.value()-1)
        self.ui.tab_roi.spinBox_roi_y2.setMinimum(self.ui.tab_roi.spinBox_roi_y1.value()+1)

        # frame waittime
        self.ui.tab_adv.spinBox_frame_waittime.setValue(self.ui.tracker.frame_waittime)

        # starting area spinboxes
        self.ui.tab_adv.spinBox_starting_x1_factor.setValue(self.ui.tracker.roim.get_roi("starting_area").x1)
        self.ui.tab_adv.spinBox_starting_x2_factor.setValue(self.ui.tracker.roim.get_roi("starting_area").x2)
        self.ui.tab_adv.spinBox_starting_y1_factor.setValue(self.ui.tracker.roim.get_roi("starting_area").y1)
        self.ui.tab_adv.spinBox_starting_y2_factor.setValue(self.ui.tracker.roim.get_roi("starting_area").y2)
        self.ui.tab_adv.spinBox_starting_x1_factor.setMaximum(self.ui.tab_adv.spinBox_starting_x2_factor.value()-1)
        self.ui.tab_adv.spinBox_starting_x2_factor.setMinimum(self.ui.tab_adv.spinBox_starting_x1_factor.value()+1)
        self.ui.tab_adv.spinBox_starting_y1_factor.setMaximum(self.ui.tab_adv.spinBox_starting_y2_factor.value()-1)
        self.ui.tab_adv.spinBox_starting_y2_factor.setMinimum(self.ui.tab_adv.spinBox_starting_y1_factor.value()+1)

        # starting orientation
        self.ui.tab_adv.spinBox_start_orientation.setValue(self.ui.tracker.start_ori)

        # fish size thresholds
        self.ui.tab_adv.spinBox_fish_threshold.setValue(self.ui.tracker.fish_size_threshold)
        self.ui.tab_adv.spinBox_fish_max_threshold.setValue(self.ui.tracker.fish_max_size_threshold)
        self.ui.tab_adv.cbx_enable_max_size_thresh.setChecked(self.ui.tracker.enable_max_size_threshold)

        # image morphing
        self.ui.tab_visual.spinBox_erosion.setValue(self.ui.tracker.erosion_iterations)
        self.ui.tab_visual.spinBox_dilation.setValue(self.ui.tracker.dilation_iterations)

        # image processing steps
        self.ui.tab_visual.cbx_show_bgsub_img.setChecked(self.ui.tracker.im.show_bg_sub_img)
        self.ui.tab_visual.cbx_show_morph_img.setChecked(self.ui.tracker.im.show_morphed_img)
        self.ui.tab_visual.cbx_show_contour.setChecked(self.ui.tracker.im.draw_contour)
        self.ui.tab_visual.cbx_show_ellipse.setChecked(self.ui.tracker.im.draw_ellipse)

        # visualization
        self.ui.tab_visual.spinBox_circle_size.setValue(self.ui.tracker.im.circle_size)
        self.ui.tab_visual.spinBox_lineend_offset.setValue(self.ui.tracker.im.lineend_offset)

    def browse_output_directory(self):
        if self.output_is_input:
            self.ui.tab_file.lnEdit_output_path.setText("Output Directory same as Input-Folder!!")
            return
        dial = QtGui.QFileDialog()
        dial.setFileMode(QtGui.QFileDialog.Directory)
        dial.setViewMode(QtGui.QFileDialog.List)
        if dial.exec_():
            self.output_directory = dial.selectedFiles()[0] + "/"
        self.ui.tab_file.lnEdit_output_path.setText(self.output_directory)
        return

    def set_tracker_video_file(self):
        self.track_file = self.ui.tab_file.lnEdit_file_path.text()
        self.ui.tracker.video_file = str(self.track_file) # FIXME you should make video_file a property in Tracker
        self.set_last_selected_folder(self.track_file)

    def set_output_directory(self):
        if not self.output_is_input:
            self.output_directory = str(self.ui.tab_file.lnEdit_output_path.text())
            self.ui.tracker.set_output_path(self.output_directory)

    def set_last_selected_folder(self, path_string):
        slash_pos = 0
        for i in range(len(path_string)-1, 0, -1):
            if path_string[i] == "/":
                slash_pos = i
                break
        self.last_selected_folder = path_string[0:slash_pos]


    def display_starting_area_preview(self):
        roi = self.ui.tracker.roim.get_roi("tracking_area")
        starting_area = self.ui.tracker.roim.get_roi("starting_area")

        roi_only_draw_numpy = copy.copy(self.first_frame_numpy[roi.y1:roi.y2, roi.x1:roi.x2])
        height, width, depth = roi_only_draw_numpy.shape
        x1 = starting_area.x1
        x2 = starting_area.x2
        y1 = starting_area.y1
        y2 = starting_area.y2
        cv2.rectangle(roi_only_draw_numpy, (x1, y1), (x2, y2), (255, 0, 255), 2)
        # convert to qimage
        sa_qimg = QtGui.QImage(roi_only_draw_numpy, roi_only_draw_numpy.shape[1], roi_only_draw_numpy.shape[0], QtGui.QImage.Format_RGB888)
        sa_pixm = QtGui.QPixmap.fromImage(sa_qimg)
        # fit img to size
        max_width = self.ui.tab_widget_options.geometry().width() - 20
        max_height = int(max_width * 0.5)
        size = QtCore.QSize(max_width, max_height)
        sa_pixm_rescaled = sa_pixm.scaled(size, QtCore.Qt.KeepAspectRatio)
        # display img
        # following line doesn't work because of %4-bug noone knows... -.-
        # self.lbl_starting_area_preview_label.setPixmap(sa_pixm_rescaled)
        cv2.imshow("starting area", roi_only_draw_numpy)

    def change_enable_nix_output(self):
        self.ui.tracker.nix_io = self.ui.tab_file.cbx_enable_nix_output.isChecked()

    def change_output_is_input(self):
        checked = self.ui.tab_file.cbx_output_is_input.isChecked()
        if checked:
            self.ui.tracker.unset_output_path()
            self.ui.tab_file.lnEdit_output_path.setText("Output = Input Folder")
        self.output_is_input = checked

    def change_tracking_roi_values(self):
        x1 = self.ui.tab_roi.spinBox_roi_x1.value()
        y1 = self.ui.tab_roi.spinBox_roi_y1.value()
        x2 = self.ui.tab_roi.spinBox_roi_x2.value()
        y2 = self.ui.tab_roi.spinBox_roi_y2.value()
        self.ui.tracker.roim.set_roi(x1, y1, x2, y2, "tracking_area")
        self.ui.tab_roi.spinBox_roi_x1.setMaximum(self.ui.tab_roi.spinBox_roi_x2.value()-1)
        self.ui.tab_roi.spinBox_roi_x2.setMinimum(self.ui.tab_roi.spinBox_roi_x1.value()+1)
        self.ui.tab_roi.spinBox_roi_y1.setMaximum(self.ui.tab_roi.spinBox_roi_y2.value()-1)
        self.ui.tab_roi.spinBox_roi_y2.setMinimum(self.ui.tab_roi.spinBox_roi_y1.value()+1)

        if self.preview_is_set:
            self.display_roi_preview()
            # self.display_starting_area_preview()

    def change_starting_area_factors(self):
        x1 = self.ui.tab_adv.spinBox_starting_x1_factor.value()
        x2 = self.ui.tab_adv.spinBox_starting_x2_factor.value()
        y1 = self.ui.tab_adv.spinBox_starting_y1_factor.value()
        y2 = self.ui.tab_adv.spinBox_starting_y2_factor.value()
        self.ui.tracker.roim.set_roi(x1, y1, x2, y2, "starting_area")
        self.ui.tab_adv.spinBox_starting_x1_factor.setMaximum(self.ui.tab_adv.spinBox_starting_x2_factor.value()-1)
        self.ui.tab_adv.spinBox_starting_x2_factor.setMinimum(self.ui.tab_adv.spinBox_starting_x1_factor.value()+1)
        self.ui.tab_adv.spinBox_starting_y1_factor.setMaximum(self.ui.tab_adv.spinBox_starting_y2_factor.value()-1)
        self.ui.tab_adv.spinBox_starting_y2_factor.setMinimum(self.ui.tab_adv.spinBox_starting_y1_factor.value()+1)

        if self.preview_is_set:
            self.display_starting_area_preview()
        return

    def change_frame_waittime(self, value):
        self.ui.tracker.frame_waittime = value

    def change_start_orientation(self, value):
        self.ui.tracker.start_ori = value

    def change_min_fish_threshold(self, value):
        self.ui.tracker.fish_size_threshold = value

    def change_max_fish_threshold(self, value):
        self.ui.tracker.fish_max_size_threshold = value

    def change_enable_max_size_threshold(self):
        self.ui.tracker.enable_max_size_threshold = self.ui.tab_adv.cbx_enable_max_size_thresh.isChecked()

    def change_erosion_factor(self, value):
        self.ui.tracker.erosion_iterations = value

    def change_dilation_factor(self, value):
        self.ui.tracker.dilation_iterations = value

    def change_show_bg_sub_img(self):
        self.ui.tracker.im.show_bg_sub_img = self.ui.tab_visual.cbx_show_bgsub_img.isChecked()

    def change_show_morphed_img(self):
        self.ui.tracker.im.show_morphed_img = self.ui.tab_visual.cbx_show_morph_img.isChecked()

    def change_draw_contour(self):
        self.ui.tracker.im.draw_contour = self.ui.tab_visual.cbx_show_contour.isChecked()

    def change_draw_ellipse(self):
        self.ui.tracker.im.draw_ellipse = self.ui.tab_visual.cbx_show_ellipse.isChecked()

    def change_lineend_offset(self, value):
        self.ui.tracker.im.lineend_offset = value

    def change_circle_size(self, value):
        self.ui.tracker.im.circle_size = value

    def set_experimenter(self, value):
        self.ui.tracker.mm.experimenter = value

    def set_fish_id(self, value):
        self.ui.tracker.mm.fish_id = value

    def start_tracking(self):
        self.set_tracker_video_file()
        self.set_output_directory()
        if self.track_file == "":
            self.ui.tab_file.lnEdit_file_path.setText("--- NO FILE SELECTED ---")
            return
        if not self.output_is_input:
            if self.output_directory == "":
                self.ui.tab_file.lnEdit_output_path.setText("--- NO DIRECTORY SELECTED ---")
                return
        if not os.path.exists(self.track_file):
            self.ui.tab_file.lnEdit_file_path.setText(self.ui.lnEdit_file_path.text() + " <-- FILE DOES NOT EXIST")
            return
        if not self.output_is_input:
            if not os.path.exists(self.output_directory):
                self.ui.tab_file.lnEdit_output_path.setText(self.ui.lnEdit_output_path.text() + " <-- DIRECTORY DOES NOT EXIST")
                return
        self.ui.tracker.run()
        self.ui.set_new_tracker()
        self.ui.controller.preset_options()  # make sure options match tracker-object (esp. nix-output option)

    def abort_tracking(self):
        self.ui.tracker.ui_abort_button_pressed = True
        self.ui.set_new_tracker()

    @property
    def ui(self):
        return self._ui