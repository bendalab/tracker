from PyQt4 import QtGui, QtCore
from MyQLine import MyQLine

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


class TabAdv(QtGui.QWidget):
    def __init__(self):
        super(TabAdv, self).__init__()

        self.setObjectName(_fromUtf8("tab_adv"))
        # vertical layout adv tab
        self.vertLO_tab_adv = QtGui.QVBoxLayout(self)
        self.vertLO_tab_adv.setObjectName(_fromUtf8("vertLO_tab_adv"))
        # spacer
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem4)
        # line
        self.line_10 = MyQLine(self, "line_10")
        self.vertLO_tab_adv.addWidget(self.line_10)
        # spacer
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem5)
        # horizontal layout frame waittime
        self.hoLO_frame_waittime = QtGui.QHBoxLayout()
        self.hoLO_frame_waittime.setObjectName(_fromUtf8("hoLO_frame_waittime"))
        # label frame waittime
        self.lbl_frame_waittime = QtGui.QLabel(self)
        self.lbl_frame_waittime.setObjectName(_fromUtf8("lbl_frame_waittime"))
        self.hoLO_frame_waittime.addWidget(self.lbl_frame_waittime)
        # spin box frame waittime
        self.spinBox_frame_waittime = QtGui.QSpinBox(self)
        self.spinBox_frame_waittime.setMinimum(1)
        self.spinBox_frame_waittime.setMaximum(1000)
        self.spinBox_frame_waittime.setObjectName(_fromUtf8("spinBox_frame_waittime"))
        self.hoLO_frame_waittime.addWidget(self.spinBox_frame_waittime)
        self.vertLO_tab_adv.addLayout(self.hoLO_frame_waittime)
        # spacer
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem6)
        # line
        self.line_5 = MyQLine(self, "line_5")
        self.vertLO_tab_adv.addWidget(self.line_5)
        # label start area
        self.lbl_start_area = QtGui.QLabel(self)
        self.lbl_start_area.setObjectName(_fromUtf8("lbl_start_area"))
        self.vertLO_tab_adv.addWidget(self.lbl_start_area)
        # graphics view starting area
         # roi preview output
        self.lbl_starting_area_preview_label = QtGui.QLabel(self)
        self.lbl_starting_area_preview_label.setObjectName(_fromUtf8("lbl_starting_area_preview_label"))
        self.lbl_starting_area_preview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vertLO_tab_adv.addWidget(self.lbl_starting_area_preview_label)
        # grid layout set starting area
        self.gridLO_start_area = QtGui.QGridLayout()
        self.gridLO_start_area.setObjectName(_fromUtf8("gridLO_start_area"))
        # spinbox starting_x start
        self.spinBox_starting_x1_factor = QtGui.QSpinBox(self)
        self.spinBox_starting_x1_factor.setMaximum(10000)
        self.spinBox_starting_x1_factor.setObjectName(_fromUtf8("spinBox_starting_x_start"))
        self.gridLO_start_area.addWidget(self.spinBox_starting_x1_factor, 0, 1, 1, 1)
        # spinbox starting_x end
        self.spinBox_starting_x2_factor = QtGui.QSpinBox(self)
        self.spinBox_starting_x2_factor.setMaximum(10000)
        self.spinBox_starting_x2_factor.setObjectName(_fromUtf8("spinBox_starting_x_end"))
        self.gridLO_start_area.addWidget(self.spinBox_starting_x2_factor, 0, 3, 1, 1)
        # spinbox starting_y start
        self.spinBox_starting_y1_factor = QtGui.QSpinBox(self)
        self.spinBox_starting_y1_factor.setMaximum(10000)
        self.spinBox_starting_y1_factor.setObjectName(_fromUtf8("spinBox_starting_y_start"))
        self.gridLO_start_area.addWidget(self.spinBox_starting_y1_factor, 1, 1, 1, 1)
        # spinbox starting_y end
        self.spinBox_starting_y2_factor = QtGui.QSpinBox(self)
        self.spinBox_starting_y2_factor.setMaximum(10000)
        self.spinBox_starting_y2_factor.setObjectName(_fromUtf8("spinBox_starting_y_end"))
        self.gridLO_start_area.addWidget(self.spinBox_starting_y2_factor, 1, 3, 1, 1)
        # label starting_x start
        self.lbl_start_x_start = QtGui.QLabel(self)
        self.lbl_start_x_start.setObjectName(_fromUtf8("lbl_start_x_start"))
        self.gridLO_start_area.addWidget(self.lbl_start_x_start, 0, 0, 1, 1)
        # label starting_x end
        self.lbl_start_x_end = QtGui.QLabel(self)
        self.lbl_start_x_end.setObjectName(_fromUtf8("lbl_start_x_end"))
        self.gridLO_start_area.addWidget(self.lbl_start_x_end, 0, 2, 1, 1)
        # label starting_y start
        self.lbl_start_y_start = QtGui.QLabel(self)
        self.lbl_start_y_start.setObjectName(_fromUtf8("lbl_start_y_start"))
        self.gridLO_start_area.addWidget(self.lbl_start_y_start, 1, 0, 1, 1)
        # label starting_y end
        self.lbl_start_y_end = QtGui.QLabel(self)
        self.lbl_start_y_end.setObjectName(_fromUtf8("lbl_start_y_end"))
        self.gridLO_start_area.addWidget(self.lbl_start_y_end, 1, 2, 1, 1)
        # add starting are selection grid layout to tab layout
        self.vertLO_tab_adv.addLayout(self.gridLO_start_area)
        # line
        self.line_6 = MyQLine(self, "line_6")
        self.vertLO_tab_adv.addWidget(self.line_6)
        # spacer
        spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem7)
        # horizontal layout set start orientation
        self.hoLO_start_ori = QtGui.QHBoxLayout()
        self.hoLO_start_ori.setObjectName(_fromUtf8("hoLO_start_ori"))
        # label start orientation
        self.lbl_start_orientation = QtGui.QLabel(self)
        self.lbl_start_orientation.setObjectName(_fromUtf8("lbl_start_orientation"))
        self.hoLO_start_ori.addWidget(self.lbl_start_orientation)
        # spinbox set start orientation
        self.spinBox_start_orientation = QtGui.QSpinBox(self)
        self.spinBox_start_orientation.setObjectName(_fromUtf8("spinBox_start_orientation"))
        self.spinBox_start_orientation.setMaximum(359)
        self.hoLO_start_ori.addWidget(self.spinBox_start_orientation)
        # add start orientation layout to tab layout
        self.vertLO_tab_adv.addLayout(self.hoLO_start_ori)
        # spacer
        spacerItem8 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem8)
        # line
        self.line_9 = MyQLine(self, "line_9")
        self.vertLO_tab_adv.addWidget(self.line_9)
        # spacer
        spacerItem9 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem9)
        # grid layout fishsize threshold
        self.gridLO_fishsize_th = QtGui.QGridLayout()
        self.gridLO_fishsize_th.setObjectName(_fromUtf8("gridLO_fishsize_th"))
        # label fishsize threshold
        self.lbl_fishsize_threshold = QtGui.QLabel(self)
        self.lbl_fishsize_threshold.setObjectName(_fromUtf8("lbl_fishsize_threshold"))
        self.gridLO_fishsize_th.addWidget(self.lbl_fishsize_threshold, 0, 0, 1, 1)
        # spinbox fishsize threshold
        self.spinBox_fish_threshold = QtGui.QSpinBox(self)
        self.spinBox_fish_threshold.setMaximum(9999)
        self.spinBox_fish_threshold.setObjectName(_fromUtf8("spinBox_fish_threshold"))
        self.gridLO_fishsize_th.addWidget(self.spinBox_fish_threshold, 0, 1, 1, 1)
        # label maximum fishsize threshold
        self.lbl_max_fishsize_threshold = QtGui.QLabel(self)
        self.lbl_max_fishsize_threshold.setObjectName(_fromUtf8("lbl_max_fishsize_threshold"))
        self.gridLO_fishsize_th.addWidget(self.lbl_max_fishsize_threshold, 1, 0, 1, 1)
        # spinbox maximum fishsize threshold
        self.spinBox_fish_max_threshold = QtGui.QSpinBox(self)
        self.spinBox_fish_max_threshold.setMaximum(9999)
        self.spinBox_fish_max_threshold.setObjectName(_fromUtf8("spinBox_fish_max_threshold"))
        self.gridLO_fishsize_th.addWidget(self.spinBox_fish_max_threshold, 1, 1, 1, 1)
        # add fishsize layout to tab layout
        self.vertLO_tab_adv.addLayout(self.gridLO_fishsize_th)
        # checkbox enable maximum size threshold
        self.cbx_enable_max_size_thresh = QtGui.QCheckBox(self)
        self.cbx_enable_max_size_thresh.setObjectName(_fromUtf8("cbx_enable_max_size_thresh"))
        self.vertLO_tab_adv.addWidget(self.cbx_enable_max_size_thresh)
        # spacer
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem10)

    def connect_widgets(self, controller):
        self.connect(self.spinBox_starting_x1_factor, QtCore.SIGNAL("valueChanged(int)"), controller.change_starting_area_factors)
        self.connect(self.spinBox_starting_x2_factor, QtCore.SIGNAL("valueChanged(int)"), controller.change_starting_area_factors)
        self.connect(self.spinBox_starting_y1_factor, QtCore.SIGNAL("valueChanged(int)"), controller.change_starting_area_factors)
        self.connect(self.spinBox_starting_y2_factor, QtCore.SIGNAL("valueChanged(int)"), controller.change_starting_area_factors)

        self.connect(self.spinBox_frame_waittime, QtCore.SIGNAL("valueChanged(int)"), controller.change_frame_waittime)

        self.connect(self.spinBox_start_orientation, QtCore.SIGNAL("valueChanged(int)"), controller.change_start_orientation)

        self.connect(self.spinBox_fish_threshold, QtCore.SIGNAL("valueChanged(int)"), controller.change_min_fish_threshold)
        self.connect(self.spinBox_fish_max_threshold, QtCore.SIGNAL("valueChanged(int)"), controller.change_max_fish_threshold)
        self.connect(self.cbx_enable_max_size_thresh, QtCore.SIGNAL("stateChanged(int)"), controller.change_enable_max_size_threshold)
        return

    def retranslate_tab_adv(self):
        self.lbl_frame_waittime.setText(_translate("tracker_main_widget", "Frame Waittime (ms)", None))
        self.lbl_start_area.setText(_translate("tracker_main_widget", "Starting Area (calculated in %)", None))
        self.lbl_start_x_end.setText(_translate("tracker_main_widget", "X End", None))
        self.lbl_start_y_start.setText(_translate("tracker_main_widget", "Y Start", None))
        self.lbl_start_y_end.setText(_translate("tracker_main_widget", "Y End", None))
        self.lbl_start_x_start.setText(_translate("tracker_main_widget", "X Start", None))
        self.lbl_start_orientation.setText(_translate("tracker_main_widget", "Starting Orientation", None))
        self.lbl_fishsize_threshold.setText(_translate("tracker_main_widget", "Fish Detection min Size Threshold", None))
        self.lbl_max_fishsize_threshold.setText(_translate("tracker_main_widget", "Fish Detection max Size Threshold", None))
        self.cbx_enable_max_size_thresh.setText(_translate("tracker_main_widget", "Enable max Size Threshold", None))