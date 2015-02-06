# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tracker_ui.ui'
#
# Created: Mon Dec  1 12:45:22 2014
#      by: PyQt4 ui code generator 4.10.4

from PyQt4 import QtCore, QtGui
from core.Tracker import Tracker
from Controller import Controller
import os
import sys
import numpy as np
import cv2
import copy
import ConfigParser

from TabFile import TabFile
from TabRoi import TabRoi
from TabAdv import TabAdv


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class TrackerUserInterface(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.setupUi(self)

        self.tracker = Tracker()
        self.controller = Controller(self)

        self.controller.preset_options()
        self.connect_widgets()
        self.set_shortcuts()

    def setupUi(self, tracker_main_widget):
        #main widget
        tracker_main_widget.setObjectName(_fromUtf8("tracker_main_widget"))
        tracker_main_widget.resize(1400/2, 835)
        tracker_main_widget.setMinimumSize(QtCore.QSize(900/2, 770))

        # main vertical layout
        self.vertLO_main = QtGui.QVBoxLayout(tracker_main_widget)
        self.vertLO_main.setObjectName(_fromUtf8("vertLO_main"))
        # horizontal layout video + options
        self.hoLO_video_plus_options = QtGui.QHBoxLayout()
        self.hoLO_video_plus_options.setObjectName(_fromUtf8("hoLO_video_plus_options"))
        # graphical output label
        # self.lbl_video_output_label = QtGui.QLabel(tracker_main_widget)
        # self.lbl_video_output_label.setMinimumWidth((tracker_main_widget.geometry().width()-22)/2)
        # self.lbl_video_output_label.setObjectName(_fromUtf8("lbl_videl_output_label"))
        # self.lbl_video_output_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.hoLO_video_plus_options.addWidget(self.lbl_video_output_label)

        # options tab widget
        self.tab_widget_options = QtGui.QTabWidget(tracker_main_widget)
        self.tab_widget_options.setObjectName(_fromUtf8("tab_widget_options"))

        # file tab
        self.tab_file = TabFile()
        self.tab_widget_options.addTab(self.tab_file, _fromUtf8(""))

        # roi tab
        # self.tab_roi = QtGui.QWidget()
        self.tab_roi = TabRoi()
        self.tab_widget_options.addTab(self.tab_roi, _fromUtf8(""))

        # adv tab
        # self.tab_adv = QtGui.QWidget()
        self.tab_adv = TabAdv()
        self.tab_widget_options.addTab(self.tab_adv, _fromUtf8(""))

        # visuals tab
        self.tab_visual = QtGui.QWidget()
        self.tab_visual.setObjectName(_fromUtf8("tab_visual"))
        # vertical layout visuals tab
        self.vertLO_tab_visual = QtGui.QVBoxLayout(self.tab_visual)
        self.vertLO_tab_visual.setObjectName(_fromUtf8("vertLO_tab_visual"))
        # spacer
        spacerItem11 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_visual.addItem(spacerItem11)
        # line
        self.line_7 = QtGui.QFrame(self.tab_visual)
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.vertLO_tab_visual.addWidget(self.line_7)
        # label image morphing
        self.lbl_img_morphing = QtGui.QLabel(self.tab_visual)
        self.lbl_img_morphing.setObjectName(_fromUtf8("lbl_img_morphing"))
        self.vertLO_tab_visual.addWidget(self.lbl_img_morphing)
        # grid layout image morphing
        self.gridLO_img_morphing = QtGui.QGridLayout()
        self.gridLO_img_morphing.setObjectName(_fromUtf8("gridLO_img_morphing"))
        # label erosion factor
        self.lbl_erosion = QtGui.QLabel(self.tab_visual)
        self.lbl_erosion.setObjectName(_fromUtf8("lbl_erosion"))
        self.gridLO_img_morphing.addWidget(self.lbl_erosion, 1, 1, 1, 1)
        # label dilation factor
        self.lbl_dilation = QtGui.QLabel(self.tab_visual)
        self.lbl_dilation.setObjectName(_fromUtf8("lbl_dilation"))
        self.gridLO_img_morphing.addWidget(self.lbl_dilation, 4, 1, 1, 1)
        # spinbox set erosion factor
        self.spinBox_erosion = QtGui.QSpinBox(self.tab_visual)
        self.spinBox_erosion.setMinimum(0)
        self.spinBox_erosion.setObjectName(_fromUtf8("spinBox_erosion"))
        self.gridLO_img_morphing.addWidget(self.spinBox_erosion, 1, 2, 1, 1)
        # spinbox set dilation factor
        self.spinBox_dilation = QtGui.QSpinBox(self.tab_visual)
        self.spinBox_dilation.setMinimum(0)
        self.spinBox_dilation.setObjectName(_fromUtf8("spinBox_dilation"))
        self.gridLO_img_morphing.addWidget(self.spinBox_dilation, 4, 2, 1, 1)
        # add grid layout image morphing
        self.vertLO_tab_visual.addLayout(self.gridLO_img_morphing)
        # line
        self.line_8 = QtGui.QFrame(self.tab_visual)
        self.line_8.setFrameShape(QtGui.QFrame.HLine)
        self.line_8.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_8.setObjectName(_fromUtf8("line_8"))
        self.vertLO_tab_visual.addWidget(self.line_8)
        # spacer
        spacerItem12 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_visual.addItem(spacerItem12)
        # line
        self.line_13 = QtGui.QFrame(self.tab_visual)
        self.line_13.setFrameShape(QtGui.QFrame.HLine)
        self.line_13.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_13.setObjectName(_fromUtf8("line_13"))
        self.vertLO_tab_visual.addWidget(self.line_13)
        # label image processing steps
        self.lbl_img_proc_steps = QtGui.QLabel(self.tab_visual)
        self.lbl_img_proc_steps.setObjectName(_fromUtf8("lbl_img_proc_steps"))
        # vertical layout show processing steps enable
        self.vertLO_tab_visual.addWidget(self.lbl_img_proc_steps)
        # checkbox show background subtracted image
        self.cbx_show_bgsub_img = QtGui.QCheckBox(self.tab_visual)
        self.cbx_show_bgsub_img.setObjectName(_fromUtf8("cbx_show_bgsub_img"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_bgsub_img)
        # checkbox show morphed image
        self.cbx_show_morph_img = QtGui.QCheckBox(self.tab_visual)
        self.cbx_show_morph_img.setObjectName(_fromUtf8("cbx_show_morph_img"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_morph_img)
        # checkbox show contour image
        self.cbx_show_contour = QtGui.QCheckBox(self.tab_visual)
        self.cbx_show_contour.setObjectName(_fromUtf8("cbx_show_contour"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_contour)
        # checkbox show ellipse
        self.cbx_show_ellipse = QtGui.QCheckBox(self.tab_visual)
        self.cbx_show_ellipse.setObjectName(_fromUtf8("cbx_show_ellipse"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_ellipse)
        # line
        self.line_14 = QtGui.QFrame(self.tab_visual)
        self.line_14.setFrameShape(QtGui.QFrame.HLine)
        self.line_14.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_14.setObjectName(_fromUtf8("line_14"))
        self.vertLO_tab_visual.addWidget(self.line_14)
        # spacer
        spacerItem13 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_visual.addItem(spacerItem13)
        # line
        self.line_11 = QtGui.QFrame(self.tab_visual)
        self.line_11.setFrameShape(QtGui.QFrame.HLine)
        self.line_11.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_11.setObjectName(_fromUtf8("line_11"))
        self.vertLO_tab_visual.addWidget(self.line_11)
        # label data visualisation
        self.gridLO_data_visual = QtGui.QGridLayout()
        self.gridLO_data_visual.setObjectName(_fromUtf8("gridLO_data_visual"))
        # spinbox linend offset
        self.spinBox_lineend_offset = QtGui.QSpinBox(self.tab_visual)
        self.spinBox_lineend_offset.setMinimum(0)
        self.spinBox_lineend_offset.setMaximum(20)
        self.spinBox_lineend_offset.setObjectName(_fromUtf8("spinBox_lineend_offset"))
        self.gridLO_data_visual.addWidget(self.spinBox_lineend_offset, 1, 1, 1, 1)
        # spinbox
        self.spinBox_circle_size = QtGui.QSpinBox(self.tab_visual)
        self.spinBox_circle_size.setMinimum(1)
        self.spinBox_circle_size.setMaximum(10)
        self.spinBox_circle_size.setObjectName(_fromUtf8("spinBox_circle_size"))
        self.gridLO_data_visual.addWidget(self.spinBox_circle_size, 2, 1, 1, 1)
        # button set line color
        self.btn_set_line_color = QtGui.QPushButton(self.tab_visual)
        self.btn_set_line_color.setObjectName(_fromUtf8("btn_set_line_color"))
        self.gridLO_data_visual.addWidget(self.btn_set_line_color, 3, 1, 1, 1)
        # button set circle color
        self.btn_set_circle_color = QtGui.QPushButton(self.tab_visual)
        self.btn_set_circle_color.setObjectName(_fromUtf8("btn_set_circle_color"))
        self.gridLO_data_visual.addWidget(self.btn_set_circle_color, 4, 1, 1, 1)
        # label circle color
        self.lbl_circ_color = QtGui.QLabel(self.tab_visual)
        self.lbl_circ_color.setObjectName(_fromUtf8("lbl_circ_color"))
        self.gridLO_data_visual.addWidget(self.lbl_circ_color, 4, 0, 1, 1)
        # label circle size
        self.lbl_circle_size = QtGui.QLabel(self.tab_visual)
        self.lbl_circle_size.setObjectName(_fromUtf8("lbl_circle_size"))
        self.gridLO_data_visual.addWidget(self.lbl_circle_size, 2, 0, 1, 1)
        # label line offset
        self.lbl_line_offset = QtGui.QLabel(self.tab_visual)
        self.lbl_line_offset.setObjectName(_fromUtf8("lbl_line_offset"))
        self.gridLO_data_visual.addWidget(self.lbl_line_offset, 1, 0, 1, 1)
        # label line color
        self.lbl_ln_color = QtGui.QLabel(self.tab_visual)
        self.lbl_ln_color.setObjectName(_fromUtf8("lbl_ln_color"))
        self.gridLO_data_visual.addWidget(self.lbl_ln_color, 3, 0, 1, 1)
        # label  data visualization
        self.lbl_data_visualisation = QtGui.QLabel(self.tab_visual)
        self.lbl_data_visualisation.setObjectName(_fromUtf8("lbl_data_visualisation"))
        self.gridLO_data_visual.addWidget(self.lbl_data_visualisation, 0, 0, 1, 1)
        # add data visualization layout
        self.vertLO_tab_visual.addLayout(self.gridLO_data_visual)
        # line
        self.line_12 = QtGui.QFrame(self.tab_visual)
        self.line_12.setFrameShape(QtGui.QFrame.HLine)
        self.line_12.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_12.setObjectName(_fromUtf8("line_12"))
        self.vertLO_tab_visual.addWidget(self.line_12)
        # spacer
        spacerItem14 = QtGui.QSpacerItem(20, 119, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_visual.addItem(spacerItem14)
        self.tab_widget_options.addTab(self.tab_visual, _fromUtf8(""))
        # add visuals tab to video_plus_options tab
        self.hoLO_video_plus_options.addWidget(self.tab_widget_options)
        # add video_plus_options tab to main widget
        self.vertLO_main.addLayout(self.hoLO_video_plus_options)

        # horizontal layout bot buttons
        self.hoLO_bot_buttons = QtGui.QHBoxLayout()
        self.hoLO_bot_buttons.setObjectName(_fromUtf8("hoLO_bot_buttons"))
        # button start tracking
        self.btn_start_tracking = QtGui.QPushButton(tracker_main_widget)
        self.btn_start_tracking.setMinimumSize(QtCore.QSize(0, 50))
        self.btn_start_tracking.setObjectName(_fromUtf8("btn_start_tracking"))
        self.hoLO_bot_buttons.addWidget(self.btn_start_tracking)
        # button abort tracking
        self.btn_abort_tracking = QtGui.QPushButton(tracker_main_widget)
        self.btn_abort_tracking.setMinimumSize(QtCore.QSize(0, 50))
        self.btn_abort_tracking.setObjectName(_fromUtf8("btn_abort_tracking"))
        self.hoLO_bot_buttons.addWidget(self.btn_abort_tracking)
        # add button layout to main widget layout
        self.vertLO_main.addLayout(self.hoLO_bot_buttons)

        self.retranslateUi(tracker_main_widget)
        self.tab_widget_options.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(tracker_main_widget)

    def retranslateUi(self, tracker_main_widget):
        tracker_main_widget.setWindowTitle(_translate("tracker_main_widget", "Tool For Tracking Fish - [TF]² 1.0", None))

        self.tab_file.retranslate_tab_file()
        self.tab_roi.retranslate_tab_roi()
        self.tab_adv.retranslate_tab_adv()

        self.tab_widget_options.setTabText(self.tab_widget_options.indexOf(self.tab_file), _translate("tracker_main_widget", "File", None))
        self.tab_widget_options.setTabText(self.tab_widget_options.indexOf(self.tab_roi), _translate("tracker_main_widget", "ROI", None))
        self.tab_widget_options.setTabText(self.tab_widget_options.indexOf(self.tab_adv), _translate("tracker_main_widget", "Advanced", None))

        self.lbl_img_morphing.setText(_translate("tracker_main_widget", "Image Morphing", None))
        self.lbl_erosion.setText(_translate("tracker_main_widget", "Erosion Faktor", None))
        self.lbl_dilation.setText(_translate("tracker_main_widget", "Dilation Faktor", None))
        self.lbl_img_proc_steps.setText(_translate("tracker_main_widget", "Image Processing Steps", None))
        self.cbx_show_bgsub_img.setText(_translate("tracker_main_widget", "Show Background-subtracted Image", None))
        self.cbx_show_morph_img.setText(_translate("tracker_main_widget", "Show Morphed Image", None))
        self.cbx_show_contour.setText(_translate("tracker_main_widget", "Show Contours", None))
        self.cbx_show_ellipse.setText(_translate("tracker_main_widget", "Show fitted Ellipse", None))
        self.btn_set_circle_color.setText(_translate("tracker_main_widget", "Set Color", None))
        self.lbl_circ_color.setText(_translate("tracker_main_widget", "Circle Color", None))
        self.lbl_circle_size.setText(_translate("tracker_main_widget", "Circle Size", None))
        self.lbl_line_offset.setText(_translate("tracker_main_widget", "Lineend Offset", None))
        self.btn_set_line_color.setText(_translate("tracker_main_widget", "Set Color", None))
        self.lbl_ln_color.setText(_translate("tracker_main_widget", "Line Color", None))
        self.lbl_data_visualisation.setText(_translate("tracker_main_widget", "Data Visualisation", None))
        self.tab_widget_options.setTabText(self.tab_widget_options.indexOf(self.tab_visual), _translate("tracker_main_widget", "Visualization", None))

        self.btn_start_tracking.setText(_translate("tracker_main_widget", "Start Tracking", None))
        self.btn_abort_tracking.setText(_translate("tracker_main_widget", "Abort Tracking", None))

    def set_shortcuts(self):
        self.btn_start_tracking.setShortcut('Ctrl+s')
        self.btn_start_tracking.setToolTip("Strg + S")

        self.tab_file.btn_browse_file.setShortcut('Ctrl+f')
        self.tab_file.btn_browse_file.setToolTip("Strg + F")

    def center_ui(self, qApp):
        # screen = QDesktopWidget().screenGeometry()
        screen = qApp.desktop().screenGeometry()
        gui_size = self.geometry()
        x_pos = (screen.width() - gui_size.width()) / 2
        y_pos = (screen.height() - gui_size.height() - gui_size.height()) / 2
        self.move(x_pos, y_pos)

    def set_new_tracker(self):
        self.tracker = Tracker()
        return

    # TODO finish connecting!
    def connect_widgets(self):
        self.tab_file.btn_browse_file.clicked.connect(self.controller.browse_file)
        self.tab_file.btn_browse_output.clicked.connect(self.controller.browse_output_directory)
        self.btn_start_tracking.clicked.connect(self.controller.start_tracking)
        self.btn_abort_tracking.clicked.connect(self.controller.abort_tracking)

        self.connect(self.tab_file.cbx_enable_nix_output, QtCore.SIGNAL("stateChanged(int)"), self.controller.change_enable_nix_output)
        self.connect(self.tab_file.cbx_output_is_input, QtCore.SIGNAL("stateChanged(int)"), self.controller.change_output_is_input)

        self.connect(self.tab_roi.spinBox_roi_x1, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_roi_values)
        self.connect(self.tab_roi.spinBox_roi_x2, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_roi_values)
        self.connect(self.tab_roi.spinBox_roi_y1, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_roi_values)
        self.connect(self.tab_roi.spinBox_roi_y2, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_roi_values)

        self.connect(self.tab_adv.spinBox_starting_x1_factor, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_starting_area_factors)
        self.connect(self.tab_adv.spinBox_starting_x2_factor, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_starting_area_factors)
        self.connect(self.tab_adv.spinBox_starting_y1_factor, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_starting_area_factors)
        self.connect(self.tab_adv.spinBox_starting_y2_factor, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_starting_area_factors)

        self.connect(self.tab_adv.spinBox_frame_waittime, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_frame_waittime)

        self.connect(self.tab_adv.spinBox_start_orientation, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_start_orientation)

        self.connect(self.tab_adv.spinBox_fish_threshold, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_min_fish_threshold)
        self.connect(self.tab_adv.spinBox_fish_max_threshold, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_max_fish_threshold)
        self.connect(self.tab_adv.cbx_enable_max_size_thresh, QtCore.SIGNAL("stateChanged(int)"), self.controller.change_enable_max_size_threshold)

        self.connect(self.spinBox_erosion, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_erosion_factor)
        self.connect(self.spinBox_dilation, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_dilation_factor)

        self.connect(self.cbx_show_bgsub_img, QtCore.SIGNAL("stateChanged(int)"), self.controller.change_show_bg_sub_img)
        self.connect(self.cbx_show_morph_img, QtCore.SIGNAL("stateChanged(int)"), self.controller.change_show_morphed_img)
        self.connect(self.cbx_show_contour, QtCore.SIGNAL("stateChanged(int)"), self.controller.change_draw_contour)
        self.connect(self.cbx_show_ellipse, QtCore.SIGNAL("stateChanged(int)"), self.controller.change_draw_ellipse)

        self.connect(self.spinBox_lineend_offset, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_lineend_offset)
        self.connect(self.spinBox_circle_size, QtCore.SIGNAL("valueChanged(int)"), self.controller.change_circle_size)
