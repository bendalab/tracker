from PyQt4 import QtGui, QtCore
from MyQLine import MyQLine
from RoiInputBox import RoiInputBox

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


class TabRoi(QtGui.QWidget):
    def __init__(self):
        super(TabRoi, self).__init__()

        self.setObjectName(_fromUtf8("tab_roi"))

        self.roi_input_boxes = []

        # vertical layout roi tab
        self.vertLO_tab_roi = QtGui.QVBoxLayout(self)
        self.vertLO_tab_roi.setObjectName(_fromUtf8("vertLO_tab_roi"))
        # spaccer
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_roi.addItem(spacerItem2)
        # line
        self.line_3 = MyQLine(self, "line_3")
        self.vertLO_tab_roi.addWidget(self.line_3)
        # label region of interest
        self.lbl_roi = QtGui.QLabel(self)
        self.lbl_roi.setObjectName(_fromUtf8("lbl_roi"))
        self.vertLO_tab_roi.addWidget(self.lbl_roi)
        # roi preview output
        self.lbl_roi_preview_label = QtGui.QLabel(self)
        self.lbl_roi_preview_label.setObjectName(_fromUtf8("lbl_roi_preview_label"))
        self.lbl_roi_preview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vertLO_tab_roi.addWidget(self.lbl_roi_preview_label)

        # # grid layout set roi
        # self.gridLO_set_roi = QtGui.QGridLayout()
        # self.gridLO_set_roi.setObjectName(_fromUtf8("gridLO_set_roi"))
        # # spin box x start
        # self.spinBox_roi_x1 = QtGui.QSpinBox(self)
        # self.spinBox_roi_x1.setMaximum(9999)
        # self.spinBox_roi_x1.setObjectName(_fromUtf8("spinBox_x_start"))
        # self.gridLO_set_roi.addWidget(self.spinBox_roi_x1, 0, 1, 1, 1)
        # # spin box x end
        # self.spinBox_roi_x2 = QtGui.QSpinBox(self)
        # self.spinBox_roi_x2.setMaximum(9999)
        # self.spinBox_roi_x2.setObjectName(_fromUtf8("spinBox_x_end"))
        # self.gridLO_set_roi.addWidget(self.spinBox_roi_x2, 0, 3, 1, 1)
        # # spin box y start
        # self.spinBox_roi_y1 = QtGui.QSpinBox(self)
        # self.spinBox_roi_y1.setMaximum(9999)
        # self.spinBox_roi_y1.setObjectName(_fromUtf8("spinBox_y_start"))
        # self.gridLO_set_roi.addWidget(self.spinBox_roi_y1, 1, 1, 1, 1)
        # # spin box y end
        # self.spinBox_roi_y2 = QtGui.QSpinBox(self)
        # self.spinBox_roi_y2.setMaximum(9999)
        # self.spinBox_roi_y2.setObjectName(_fromUtf8("spinBox_y_end"))
        # self.gridLO_set_roi.addWidget(self.spinBox_roi_y2, 1, 3, 1, 1)
        # # label x start
        # self.lbl_roi_x_start = QtGui.QLabel(self)
        # self.lbl_roi_x_start.setObjectName(_fromUtf8("lbl_roi_x_start"))
        # self.gridLO_set_roi.addWidget(self.lbl_roi_x_start, 0, 0, 1, 1)
        # # label x end
        # self.lbl_roi_x_end = QtGui.QLabel(self)
        # self.lbl_roi_x_end.setObjectName(_fromUtf8("lbl_roi_x_end"))
        # self.gridLO_set_roi.addWidget(self.lbl_roi_x_end, 0, 2, 1, 1)
        # # label y start
        # self.lbl_roi_y_start = QtGui.QLabel(self)
        # self.lbl_roi_y_start.setObjectName(_fromUtf8("lbl_roi_y_start"))
        # self.gridLO_set_roi.addWidget(self.lbl_roi_y_start, 1, 0, 1, 1)
        # # label y end
        # self.lbl_roi_y_end = QtGui.QLabel(self)
        # self.lbl_roi_y_end.setObjectName(_fromUtf8("lbl_roi_y_end"))
        # self.gridLO_set_roi.addWidget(self.lbl_roi_y_end, 1, 2, 1, 1)
        # # add grid_layout_set_roi to vertical layout of tab
        # self.vertLO_tab_roi.addLayout(self.gridLO_set_roi)
        # line
        self.line_4 = MyQLine(self, "line_4")
        self.vertLO_tab_roi.addWidget(self.line_4)
        # spacer
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_roi.addItem(spacerItem3)

    def populate(self, roim):
        for entry in roim.roi_list:
            self.add_roi_input_box(entry)

    def add_roi_input_box(self, roi):
        new_box = RoiInputBox(roi)
        self.roi_input_boxes.append(new_box)
        self.vertLO_tab_roi.addWidget(new_box)
        new_box.retranslate_roi_input_box()

    # TODO
    def connect_widgets(self, controller):
        for box in self.roi_input_boxes:
            box.connect_widgets(controller)
        return

    def retranslate_tab_roi(self):
        self.lbl_roi.setToolTip(_translate("tracker_main_widget", "<html><head/><body><p>Define the Area in which the Fish shall be detected. Point (0,0) is the upper left corner.</p></body></html>", None))
        self.lbl_roi.setText(_translate("tracker_main_widget", "Region of interest", None))
        # self.lbl_roi_y_end.setText(_translate("tracker_main_widget", "Y End", None))
        # self.lbl_roi_x_end.setText(_translate("tracker_main_widget", "X End", None))
        # self.lbl_roi_x_start.setText(_translate("tracker_main_widget", "X Start", None))
        # self.lbl_roi_y_start.setText(_translate("tracker_main_widget", "Y Start", None))
        for box in self.roi_input_boxes:
            box.retranslate_roi_input_box()