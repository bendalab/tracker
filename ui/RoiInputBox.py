from PyQt5 import QtWidgets, QtCore
import random

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


class RoiInputBox(QtWidgets.QWidget):
    def __init__(self, roi, controller):
        super(RoiInputBox, self).__init__()

        self.controller = controller

        self.setMinimumHeight(100)

        self.name = roi.name  #"roi_{0:s}".format(roi.name)
        self.roi_name = roi.name
        self.color = (random.randint(25, 200), random.randint(25, 200), random.randint(25, 200))

        self.setObjectName(_fromUtf8(self.name))

        self.vertLO_input_box = QtWidgets.QVBoxLayout(self)
        self.vertLO_input_box.setObjectName(_fromUtf8("vertLO_input_box"))

        self.lbl_name = QtWidgets.QLabel(self)
        self.lbl_name.setObjectName(_fromUtf8("lbl_name"))
        self.lbl_name.setAutoFillBackground(True)
        color_string = "rgb({0:s},{1:s},{2:s})".format(str(self.color[0]), str(self.color[1]),
                                                       str(self.color[2]))
        self.lbl_name.setStyleSheet("QLabel {{color: {0:s}; }}".format(color_string))
        self.vertLO_input_box.addWidget(self.lbl_name)

        self.gridLO_set_roi = QtWidgets.QGridLayout()
        self.gridLO_set_roi.setObjectName(_fromUtf8("gridLO_set_roi"))
        # spin box x start
        self.spinBox_roi_x1 = QtWidgets.QSpinBox(self)
        self.spinBox_roi_x1.setMaximum(9999)
        self.spinBox_roi_x1.setObjectName(_fromUtf8("spinBox_x_start"))
        self.gridLO_set_roi.addWidget(self.spinBox_roi_x1, 0, 1, 1, 1)
        # spin box x end
        self.spinBox_roi_x2 = QtWidgets.QSpinBox(self)
        self.spinBox_roi_x2.setMaximum(9999)
        self.spinBox_roi_x2.setObjectName(_fromUtf8("spinBox_x_end"))
        self.gridLO_set_roi.addWidget(self.spinBox_roi_x2, 0, 3, 1, 1)
        # spin box y start
        self.spinBox_roi_y1 = QtWidgets.QSpinBox(self)
        self.spinBox_roi_y1.setMaximum(9999)
        self.spinBox_roi_y1.setObjectName(_fromUtf8("spinBox_y_start"))
        self.gridLO_set_roi.addWidget(self.spinBox_roi_y1, 1, 1, 1, 1)
        # spin box y end
        self.spinBox_roi_y2 = QtWidgets.QSpinBox(self)
        self.spinBox_roi_y2.setMaximum(9999)
        self.spinBox_roi_y2.setObjectName(_fromUtf8("spinBox_y_end"))
        self.gridLO_set_roi.addWidget(self.spinBox_roi_y2, 1, 3, 1, 1)
        # label x start
        self.lbl_roi_x_start = QtWidgets.QLabel(self)
        self.lbl_roi_x_start.setObjectName(_fromUtf8("lbl_roi_x_start"))
        self.gridLO_set_roi.addWidget(self.lbl_roi_x_start, 0, 0, 1, 1)
        # label x end
        self.lbl_roi_x_end = QtWidgets.QLabel(self)
        self.lbl_roi_x_end.setObjectName(_fromUtf8("lbl_roi_x_end"))
        self.gridLO_set_roi.addWidget(self.lbl_roi_x_end, 0, 2, 1, 1)
        # label y start
        self.lbl_roi_y_start = QtWidgets.QLabel(self)
        self.lbl_roi_y_start.setObjectName(_fromUtf8("lbl_roi_y_start"))
        self.gridLO_set_roi.addWidget(self.lbl_roi_y_start, 1, 0, 1, 1)
        # label y end
        self.lbl_roi_y_end = QtWidgets.QLabel(self)
        self.lbl_roi_y_end.setObjectName(_fromUtf8("lbl_roi_y_end"))
        self.gridLO_set_roi.addWidget(self.lbl_roi_y_end, 1, 2, 1, 1)
        # add grid_layout_set_roi to vertical layout of tab
        self.vertLO_input_box.addLayout(self.gridLO_set_roi)

    def get_values(self):
        x1 = self.spinBox_roi_x1.value()
        y1 = self.spinBox_roi_y1.value()
        x2 = self.spinBox_roi_x2.value()
        y2 = self.spinBox_roi_y2.value()
        return x1, y1, x2, y2

    def connect_widgets(self, controller):
        self.spinBox_roi_x1.valueChanged.connect(self.send_value_change_x1)
        self.spinBox_roi_x2.valueChanged.connect(self.send_value_change_x2)
        self.spinBox_roi_y1.valueChanged.connect(self.send_value_change_y1)
        self.spinBox_roi_y2.valueChanged.connect(self.send_value_change_y2)
        return

    def send_value_change_x1(self):
        self.controller.change_roi_value(self, "x1")

    def send_value_change_x2(self):
        self.controller.change_roi_value(self, "x2")

    def send_value_change_y1(self):
        self.controller.change_roi_value(self, "y1")

    def send_value_change_y2(self):
        self.controller.change_roi_value(self, "y2")

    def retranslate_roi_input_box(self):
        self.lbl_name.setText(_translate("tracker_main_widget", self.name, None))
        self.lbl_roi_y_end.setText(_translate("tracker_main_widget", "Y End", None))
        self.lbl_roi_x_end.setText(_translate("tracker_main_widget", "X End", None))
        self.lbl_roi_x_start.setText(_translate("tracker_main_widget", "X Start", None))
        self.lbl_roi_y_start.setText(_translate("tracker_main_widget", "Y Start", None))
