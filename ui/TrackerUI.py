# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tracker_ui.ui'
#
# Created: Mon Dec  1 12:45:22 2014
#      by: PyQt4 ui code generator 4.10.4

from PyQt5 import QtWidgets, QtCore
from core.Tracker import Tracker
from controller.Controller import Controller

from .TabFile import TabFile
from .TabRoi import TabRoi
from .TabAdv import TabAdv
from .TabVisual import TabVisual
from .TabMeta import TabMeta


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class TrackerUserInterface(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.batch_tracking_enabled = False

        #main widget
        self.setObjectName(_fromUtf8("self"))

        # main vertical layout
        self.vertLO_main = QtWidgets.QVBoxLayout(self)
        self.vertLO_main.setObjectName(_fromUtf8("vertLO_main"))
        # horizontal layout video + options
        self.hoLO_video_plus_options = QtWidgets.QHBoxLayout()
        self.hoLO_video_plus_options.setObjectName(_fromUtf8("hoLO_video_plus_options"))
        # graphical output label
        # self.lbl_video_output_label = QtWidgets.QLabel(self)
        # self.lbl_video_output_label.setMinimumWidth((self.geometry().width()-22)/2)
        # self.lbl_video_output_label.setObjectName(_fromUtf8("lbl_videl_output_label"))
        # self.lbl_video_output_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.hoLO_video_plus_options.addWidget(self.lbl_video_output_label)

        # options tab widget
        self.tab_widget_options = QtWidgets.QTabWidget(self)
        self.tab_widget_options.setObjectName(_fromUtf8("tab_widget_options"))

        # file tab
        self.tab_file = TabFile()
        self.tab_widget_options.addTab(self.tab_file, _fromUtf8(""))

        # roi tab
        self.tab_roi = TabRoi()
        self.tab_widget_options.addTab(self.tab_roi, _fromUtf8(""))

        # adv tab
        self.tab_adv = TabAdv()
        self.tab_widget_options.addTab(self.tab_adv, _fromUtf8(""))

        # visuals tab
        self.tab_visual = TabVisual()
        self.tab_widget_options.addTab(self.tab_visual, _fromUtf8(""))

        # meta tab
        self.tab_meta = TabMeta()
        self.tab_widget_options.addTab(self.tab_meta, _fromUtf8(""))

        # add options widget to horizontal layout
        self.hoLO_video_plus_options.addWidget(self.tab_widget_options)

        # add video_plus_options tab to main widget
        self.vertLO_main.addLayout(self.hoLO_video_plus_options)

        # horizontal layout bot buttons
        self.hoLO_bot_buttons = QtWidgets.QHBoxLayout()
        self.hoLO_bot_buttons.setObjectName(_fromUtf8("hoLO_bot_buttons"))
        # button start tracking
        self.btn_start_tracking = QtWidgets.QPushButton(self)
        self.btn_start_tracking.setMinimumSize(QtCore.QSize(0, 50))
        self.btn_start_tracking.setObjectName(_fromUtf8("btn_start_tracking"))
        self.btn_start_tracking.setDisabled(False)
        self.hoLO_bot_buttons.addWidget(self.btn_start_tracking)
        # vertical layout file label and progress label
        self.vert_lo_file_progress = QtWidgets.QVBoxLayout()
        # file bel
        self.lbl_file = QtWidgets.QLabel()
        self.lbl_file.setObjectName(_fromUtf8("lbl_file"))
        self.lbl_file.setText(_fromUtf8("no file started"))
        self.vert_lo_file_progress.addWidget(self.lbl_file)
        # progress label
        self.lbl_progress = QtWidgets.QLabel()
        self.lbl_progress.setObjectName(_fromUtf8("lbl_progress"))
        self.lbl_progress.setText(_fromUtf8("Progress:"))
        self.vert_lo_file_progress.addWidget(self.lbl_progress)
        self.hoLO_bot_buttons.addLayout(self.vert_lo_file_progress)
        # button abort tracking
        self.btn_abort_tracking = QtWidgets.QPushButton(self)
        self.btn_abort_tracking.setMinimumSize(QtCore.QSize(0, 50))
        self.btn_abort_tracking.setObjectName(_fromUtf8("btn_abort_tracking"))
        self.btn_abort_tracking.setDisabled(True)
        self.hoLO_bot_buttons.addWidget(self.btn_abort_tracking)
        # add button layout to main widget layout
        self.vertLO_main.addLayout(self.hoLO_bot_buttons)

        self.retranslate_ui(self)
        self.tab_widget_options.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.controller = Controller(self)
        self.connect_controller_to_tabs()
        self.tracker = Tracker(controller=self.controller)

        # self.tab_roi.populate(self.tracker.roim)

        self.controller.preset_options()
        self.connect_widgets()
        self.set_shortcuts()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def connect_controller_to_tabs(self):
        self.tab_roi.connect_to_controller(self.controller)
        self.tab_meta.connect_to_controller(self.controller)
        # TODO connect to other tabs

    def retranslate_ui(self, tracker_main_widget):
        tracker_main_widget.setWindowTitle(_translate("tracker_main_widget",
                                                      "Tool For Tracking Fish - [TF]² Ver. 1.5 beta",
                                                      None))

        self.tab_file.retranslate_tab_file()
        self.tab_roi.retranslate_tab_roi()
        self.tab_adv.retranslate_tab_adv()
        self.tab_visual.retranslate_tab_visual()
        self.tab_meta.retranslate_tab_meta()

        self.tab_widget_options.setTabText(self.tab_widget_options.indexOf(self.tab_file),
                                           _translate("tracker_main_widget", "File", None))
        self.tab_widget_options.setTabText(self.tab_widget_options.indexOf(self.tab_roi),
                                           _translate("tracker_main_widget", "ROI", None))
        self.tab_widget_options.setTabText(self.tab_widget_options.indexOf(self.tab_adv),
                                           _translate("tracker_main_widget", "Advanced", None))
        self.tab_widget_options.setTabText(self.tab_widget_options.indexOf(self.tab_visual),
                                           _translate("tracker_main_widget", "Visualization", None))
        self.tab_widget_options.setTabText(self.tab_widget_options.indexOf(self.tab_meta),
                                           _translate("tracker_main_widget", "Meta Data", None))

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

    def set_new_tracker(self, controller):
        self.tab_roi.clear()
        self.tab_meta.clear_tabs()
        if self.batch_tracking_enabled:
            self.tracker = Tracker(controller=controller, batch_mode_on=True)
        else:
            self.tracker = Tracker(controller=controller)
        return

    def connect_widgets(self):
        self.tab_file.connect_widgets(self.controller)
        self.tab_roi.connect_widgets(self.controller)
        self.tab_adv.connect_widgets(self.controller)
        self.tab_visual.connect_widgets(self.controller)
        self.tab_meta.connect_widgets(self.controller)

        self.btn_start_tracking.clicked.connect(self.controller.start_tracking)
        self.btn_abort_tracking.clicked.connect(self.controller.abort_tracking)
