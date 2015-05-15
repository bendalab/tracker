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


class TabRoi(QtGui.QScrollArea):
    def __init__(self):
        super(TabRoi, self).__init__()

        # widget to be put into scrollArea (TabRoi)
        self.tabRoi_widget = QtGui.QWidget()

        self.setObjectName(_fromUtf8("tab_roi"))

        self.roi_input_boxes = []

        # horizontal layout preview  + layout config
        self.hoLO_tab_roi = QtGui.QHBoxLayout(self.tabRoi_widget)

        # left side widget
        self.roi_preview_widget = QtGui.QWidget()
        self.vertLO_roi_preview = QtGui.QVBoxLayout(self.roi_preview_widget)
        # spaccer
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_roi_preview.addItem(spacerItem2)
        # line
        self.line_3 = MyQLine(self, "line_3")
        self.vertLO_roi_preview.addWidget(self.line_3)
        # label region of interest
        self.lbl_roi = QtGui.QLabel(self.tabRoi_widget)
        self.lbl_roi.setObjectName(_fromUtf8("lbl_roi"))
        self.vertLO_roi_preview.addWidget(self.lbl_roi)
        # add roi preview output
        self.lbl_roi_preview_label = QtGui.QLabel(self.tabRoi_widget)
        self.lbl_roi_preview_label.setObjectName(_fromUtf8("lbl_roi_preview_label"))
        self.lbl_roi_preview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vertLO_roi_preview.addWidget(self.lbl_roi_preview_label)
        self.line_4 = MyQLine(self, "line_4")
        self.vertLO_roi_preview.addWidget(self.line_4)
        # spacer
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_roi_preview.addItem(spacerItem3)
        #self.vertLO_roi__preview.setContentsMargins(0, 0, 30, 0)

        # right side widget
        self.roi_config_widget = QtGui.QWidget()
        # vertical layout roi config
        self.vertLO_roi_config = QtGui.QVBoxLayout(self.roi_config_widget)
        self.vertLO_roi_config.setObjectName(_fromUtf8("vertLO_tab_roi"))
        self.vertLO_roi_config.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))

        # add roi preview and config widget
        self.hoLO_tab_roi.addWidget(self.roi_preview_widget)
        self.hoLO_tab_roi.addWidget(self.roi_config_widget)

        # put widget into scroll area
        self.setWidget(self.tabRoi_widget)

    # def populate(self, roim):
    #     for entry in roim.roi_list:
    #         self.add_roi_input_box(entry)

    def add_roi_input_box(self, roi, controller):
        new_box = RoiInputBox(roi)
        self.roi_input_boxes.append(new_box)
        self.vertLO_roi_config.addWidget(new_box)
        new_box.retranslate_roi_input_box()
        controller.preset_roi_input_box(new_box)
        new_box.connect_widgets(controller)
        self.vertLO_roi_config.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        self.roi_config_widget.adjustSize()
        self.roi_preview_widget.adjustSize()
        self.tabRoi_widget.adjustSize()

    def connect_widgets(self, controller):
        for box in self.roi_input_boxes:
            box.connect_widgets(controller)
        return

    def clear(self):
        for input_box in self.roi_input_boxes:
            self.vertLO_roi_config.removeWidget(input_box)
            input_box.deleteLater()
        self.roi_input_boxes = []

    def retranslate_tab_roi(self):
        self.lbl_roi.setToolTip(_translate("tracker_main_widget", "<html><head/><body><p>Define the Area in which the Fish shall be detected. Point (0,0) is the upper left corner.</p></body></html>", None))
        self.lbl_roi.setText(_translate("tracker_main_widget", "Region of interest", None))
        # self.lbl_roi_y_end.setText(_translate("tracker_main_widget", "Y End", None))
        # self.lbl_roi_x_end.setText(_translate("tracker_main_widget", "X End", None))
        # self.lbl_roi_x_start.setText(_translate("tracker_main_widget", "X Start", None))
        # self.lbl_roi_y_start.setText(_translate("tracker_main_widget", "Y Start", None))
        for box in self.roi_input_boxes:
            box.retranslate_roi_input_box()