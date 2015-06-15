from PyQt4 import QtGui, QtCore
import cv2
import copy
import ConfigParser
import os
import odml
from ui.TabFileBatch import TabFileBatch
from ui.TabFile import TabFile

class Controller(object):
    def __init__(self, ui):
        self._ui = ui
        self.tracker = None

        # self.preset_options()
        self.track_file = ""
        self.track_directory = ""
        self.last_selected_folder = "/home"

        self.template_file = ""
        self.last_selected_template_folder = "/home"

        self.output_directory = ""
        self.output_is_input = False

        # ROI variables
        self.first_frame_numpy = None
        self.roi_preview_draw_numpy = None
        self.preview_is_set = False
        self.roi_preview_displayed = False
        return

    def connect_to_tracker(self, tracker):
        self.tracker = tracker

    def btn_to_batch_clicked(self):
        batch_tab = TabFileBatch()
        batch_tab.retranslate_tab_file_batch()
        batch_tab.connect_widgets(self)

        self.ui.tab_widget_options.removeTab(0)
        self.ui.tab_widget_options.insertTab(0, batch_tab, "File")
        self.ui.tab_widget_options.setCurrentWidget(batch_tab)

        self.ui.tab_file = batch_tab

        self.ui.batch_tracking_enabled = True

    def btn_to_single_clicked(self):
        file_tab = TabFile()
        file_tab.retranslate_tab_file()
        file_tab.connect_widgets(self)

        self.ui.tab_widget_options.removeTab(0)
        self.ui.tab_widget_options.insertTab(0, file_tab, "File")
        self.ui.tab_widget_options.setCurrentWidget(file_tab)

        self.ui.tab_file = file_tab

        self.ui.batch_tracking_enabled = False

    def browse_file(self):
        self.roi_preview_displayed = False

        self.track_file = QtGui.QFileDialog.getOpenFileName(self.ui, 'Open file', self.last_selected_folder)
        if self.track_file == "":
            return
        self.ui.tab_file.lnEdit_file_path.setText(self.track_file)

        self.set_first_frame_numpy()
        self.display_roi_preview()
        # self.display_starting_area_preview()

    def btn_browse_directory_clicked(self):
        self.roi_preview_displayed = False

        file_dialog = QtGui.QFileDialog()
        file_dialog.setFileMode(QtGui.QFileDialog.Directory)
        if file_dialog.exec_():
            self.track_directory = file_dialog.selectedFiles()[0]
        if self.track_directory == "":
            return
        self.ui.tab_file.lnEdit_file_path.setText(self.track_directory)


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
        if not self.preview_is_set:
            return
        self.roi_preview_draw_numpy = copy.copy(self.first_frame_numpy)
        for roi in self.tracker.roim.roi_list:
            roi_input_box = self.ui.tab_roi.get_roi_input_box(roi.name)
            cv2.rectangle(self.roi_preview_draw_numpy, (roi.x1, roi.y1), (roi.x2, roi.y2), roi_input_box.color, 2)
        # convert numpy-array to qimage
        output_qimg = QtGui.QImage(self.roi_preview_draw_numpy, self.first_frame_numpy.shape[1], self.first_frame_numpy.shape[0], QtGui.QImage.Format_RGB888)
        output_pixm = QtGui.QPixmap.fromImage(output_qimg)
        # fit picture to window size
        width = self.ui.tab_widget_options.geometry().width()*0.65
        height = int(width)
        size = QtCore.QSize(width, height)
        output_pixm_rescaled = output_pixm.scaled(size, QtCore.Qt.KeepAspectRatio)
        # display picture
        self.ui.tab_roi.lbl_roi_preview_label.setPixmap(output_pixm_rescaled)
        self.roi_preview_displayed = True
        self.ui.tab_roi.adjust_all_sizes()

    def update_progress(self, cap, frame_counter):
        max_frames = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        progress = "{0:s} %".format(str(frame_counter/max_frames*100)[0:6])
        self.ui.lbl_progress.setText("Progress: {0:s}".format(progress))

    def preset_options(self):
        # video file
        # self.lnEdit_file_path.setText(self.tracker.video_file)
        # self.ui.tab_file.cbx_enable_nix_output.setChecked(self.ui.tracker.nix_io)

        # meta
        # self.ui.tab_meta.ln_edit_experimenter.setText(self.ui.tracker.mm.experimenter)
        # self.ui.tab_meta.ln_edit_fish_id.setText(self.ui.tracker.mm.fish_id)

        # frame waittime
        self.ui.tab_adv.spinBox_frame_waittime.setValue(self.ui.tracker.frame_waittime)

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

    def add_new_roi_clicked(self):
        roi_name_lnedit = self.ui.tab_roi.lnEdit_new_roi_name.text()
        if " " in roi_name_lnedit:
            self.ui.tab_roi.lnEdit_new_roi_name.setText("no spaces allowed!")
            return
        elif roi_name_lnedit == "":
            self.ui.tab_roi.lnEdit_new_roi_name.setText("enter a name for new roi!")
            return
        elif roi_name_lnedit in [n.name for n in self.tracker.roim.roi_list]:
            self.ui.tab_roi.lnEdit_new_roi_name.setText("roi with that name already exists!")
            return
        else:
            self.tracker.roim.add_roi(0, 0, 50, 50, roi_name_lnedit, self)
            if self.preview_is_set:
                self.display_roi_preview()
        return

    def delete_roi_clicked(self):
        roi_name_lnedit = self.ui.tab_roi.lnEdit_new_roi_name.text()
        if roi_name_lnedit == "tracking_area":
            self.ui.tab_roi.lnEdit_new_roi_name.setText("can't remove tracking_area!")
            return
        if roi_name_lnedit == "starting_area":
            self.ui.tab_roi.lnEdit_new_roi_name.setText("can't remove starting_area!")
            return
        if " " in roi_name_lnedit:
            self.ui.tab_roi.lnEdit_new_roi_name.setText("no spaces allowed!")
            return
        elif roi_name_lnedit == "":
            self.ui.tab_roi.lnEdit_new_roi_name.setText("enter a name of existing roi!")
            return
        elif roi_name_lnedit not in [n.name for n in self.tracker.roim.roi_list]:
            self.ui.tab_roi.lnEdit_new_roi_name.setText("roi with that name doesn't exist!")
            return
        else:
            self.tracker.roim.remove_roi(roi_name_lnedit, self)
            if self.preview_is_set:
                self.display_roi_preview()
        return

    def roi_added_to_tracker(self, roi):
        self.ui.tab_roi.add_roi_input_box(roi, self)
        return

    def roi_removed_from_tracker(self, roi_name):
        self.ui.tab_roi.remove_roi_input_box(roi_name, self)
        return

    def set_all_roi_input_boxes(self):
        for box in self.ui.tab_roi.roi_input_boxes:
            self.preset_roi_input_box(box)

        if self.preview_is_set:
            self.display_roi_preview()

    def preset_roi_input_box(self, box):
        # roi_name = "_".join(box.name.split("_")[1:])
        roi_name = box.name
        box.spinBox_roi_x2.setValue(self.tracker.roim.get_roi(roi_name).x2)
        box.spinBox_roi_y2.setValue(self.tracker.roim.get_roi(roi_name).y2)
        box.spinBox_roi_x1.setValue(self.tracker.roim.get_roi(roi_name).x1)
        box.spinBox_roi_y1.setValue(self.tracker.roim.get_roi(roi_name).y1)

    def metadata_entry_added(self, meta_entry):
        self.ui.tab_meta.add_tab_meta_entry(meta_entry)
        return

    def metadata_entry_removed(self, name):
        self.ui.tab_meta.remove_tab_meta_entry(name)
        return

    def btn_template_browse_clicked(self):
        self.template_file = QtGui.QFileDialog.getOpenFileName(self.ui, 'Open file', self.last_selected_template_folder)
        if self.template_file != "":
            self.last_selected_template_folder = "/".join(str(self.template_file).split("/")[:-1])
            print self.last_selected_template_folder
        self.ui.tab_meta.ln_edit_browse_template.setText(self.template_file)

    def btn_template_add_clicked(self):
        path = str(self.ui.tab_meta.ln_edit_browse_template.text())
        name = path.split("/")[-1].split(".")[0]
        try:
            odml.tools.xmlparser.load(path)
        except Exception as e:
            print "odml error: {0:s}".format(str(e))
            self.ui.tab_meta.ln_edit_browse_template.setText("{0:s} <-- not valid".format(str(self.ui.tab_meta.ln_edit_browse_template.text())))
            return
        self.tracker.mm.add_meta_entry(name, path, self)

    def btn_template_remove_clicked(self):
        template = str(self.ui.tab_meta.ln_edit_remove_template.text())
        self.tracker.mm.remove_meta_entry(template, self)

    def btn_remove_self_clicked(self):
        for entry in self.ui.tab_meta.meta_entry_tabs:
            if entry.delete_me:
                self.tracker.mm.remove_meta_entry(entry.name, self)
                break

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

    def change_output_is_input(self):
        checked = self.ui.tab_file.cbx_output_is_input.isChecked()
        if checked:
            self.ui.tracker.unset_output_path()
            self.ui.tab_file.lnEdit_output_path.setText("Output = Input Folder")
        self.output_is_input = checked

    def change_roi_values(self):
        for box in self.ui.tab_roi.roi_input_boxes:
            x1, y1, x2, y2 = box.get_values()
            area_name = box.name
            self.tracker.roim.set_roi(x1, y1, x2, y2, area_name)
            box.spinBox_roi_x1.setMaximum(box.spinBox_roi_x2.value()-1)
            box.spinBox_roi_x2.setMinimum(box.spinBox_roi_x1.value()+1)
            box.spinBox_roi_y1.setMaximum(box.spinBox_roi_y2.value()-1)
            box.spinBox_roi_y2.setMinimum(box.spinBox_roi_y1.value()+1)

        if self.preview_is_set:
            self.display_roi_preview()
            # self.display_starting_area_preview()

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
            self.ui.tab_file.lnEdit_file_path.setText(self.ui.tab_file.lnEdit_file_path.text() + " <-- FILE DOES NOT EXIST")
            return
        if not self.output_is_input:
            if not os.path.exists(self.output_directory):
                self.ui.tab_file.lnEdit_output_path.setText(self.ui.tab_file.lnEdit_output_path.text() + " <-- DIRECTORY DOES NOT EXIST")
                return
        self.ui.btn_abort_tracking.setDisabled(False)
        self.ui.btn_start_tracking.setDisabled(True)
        self.ui.tracker.run()
        self.ui.set_new_tracker(self)
        self.ui.controller.preset_options()

    def abort_tracking(self):
        self.ui.tracker.ui_abort_button_pressed = True
        self.ui.set_new_tracker(self)
        self.ui.btn_abort_tracking.setDisabled(True)
        self.ui.btn_start_tracking.setDisabled(False)

    @property
    def ui(self):
        return self._ui