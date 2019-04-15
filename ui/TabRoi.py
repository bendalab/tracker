from PyQt5 import QtWidgets, QtCore
from MyQLine import MyQLine
from RoiInputBox import RoiInputBox

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


class TabRoi(QtWidgets.QWidget):
    def __init__(self):
        super(TabRoi, self).__init__()

        self.controller = None

        self.setObjectName(_fromUtf8("tab_roi"))

        self.roi_input_boxes = []

        # horizontal layout preview  + layout config
        self.hoLO_tab_roi = QtWidgets.QHBoxLayout(self)

        # left side widget
        self.roi_preview_widget = QtWidgets.QWidget()
        self.vertLO_roi_preview = QtWidgets.QVBoxLayout(self.roi_preview_widget)
        # spaccer
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.vertLO_roi_preview.addItem(spacerItem2)
        # line
        self.line_3 = MyQLine(self, "line_3")
        self.vertLO_roi_preview.addWidget(self.line_3)
        # label region of interest
        self.lbl_roi = QtWidgets.QLabel(self)
        self.lbl_roi.setObjectName(_fromUtf8("lbl_roi"))
        self.vertLO_roi_preview.addWidget(self.lbl_roi)
        # add roi preview output
        self.lbl_roi_preview_label = QtWidgets.QLabel(self)
        self.lbl_roi_preview_label.setObjectName(_fromUtf8("lbl_roi_preview_label"))
        self.lbl_roi_preview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vertLO_roi_preview.addWidget(self.lbl_roi_preview_label)
        self.line_4 = MyQLine(self, "line_4")
        self.vertLO_roi_preview.addWidget(self.line_4)
        # spacer
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.vertLO_roi_preview.addItem(spacerItem3)

        # right side widget
        self.roi_config_scroll_area = QtWidgets.QScrollArea()
        self.roi_config_widget = QtWidgets.QWidget()
        self.roi_config_widget.setMinimumHeight(600)
        self.roi_config_widget.setMinimumWidth(280)
        # vertical layout roi config
        self.vertLO_roi_config = QtWidgets.QVBoxLayout(self.roi_config_widget)
        self.vertLO_roi_config.setObjectName(_fromUtf8("vertLO_tab_roi"))
        # label for new roi name
        self.lbl_new_roi_name = QtWidgets.QLabel(self)
        self.lbl_new_roi_name.setObjectName(_fromUtf8("lbl_new_roi_name"))
        self.vertLO_roi_config.addWidget(self.lbl_new_roi_name)
        # line edit for new roi name
        self.lnEdit_new_roi_name = QtWidgets.QLineEdit(self)
        self.lnEdit_new_roi_name.setObjectName(_fromUtf8("new_roi_name"))
        self.vertLO_roi_config.addWidget(self.lnEdit_new_roi_name)
        # button for roi creation
        self.btn_create_roi = QtWidgets.QPushButton()
        self.btn_create_roi.setObjectName(_fromUtf8("btn_create_roi"))
        self.vertLO_roi_config.addWidget(self.btn_create_roi)
        # button for roi deletion
        self.btn_delete_roi = QtWidgets.QPushButton()
        self.btn_delete_roi.setObjectName(_fromUtf8("btn_delete_roi"))
        self.vertLO_roi_config.addWidget(self.btn_delete_roi)

        self.roi_config_scroll_area.setWidget(self.roi_config_widget)

        # add roi preview and config widget
        self.hoLO_tab_roi.addWidget(self.roi_preview_widget)
        self.hoLO_tab_roi.addWidget(self.roi_config_scroll_area)

    def connect_to_controller(self, controller):
        self.controller = controller

    def get_roi_input_box(self, name):
        for r in self.roi_input_boxes:
            if r.name == name:
                return r

    def add_roi_input_box(self, roi, controller):
        new_box = RoiInputBox(roi, controller)
        self.roi_input_boxes.append(new_box)
        self.vertLO_roi_config.addWidget(new_box)
        new_box.retranslate_roi_input_box()
        controller.preset_roi_input_box(new_box)
        new_box.connect_widgets(self.controller)
        controller.display_roi_preview()

    def remove_roi_input_box(self, roi_name, controller):
        roi_box_name = "roi_{0:s}".format(roi_name)
        for i in range(len(self.roi_input_boxes)):
            if self.roi_input_boxes[i].name == roi_box_name:
                self.vertLO_roi_config.removeWidget(self.roi_input_boxes[i])
                self.roi_input_boxes[i].deleteLater()
                self.roi_input_boxes.pop(i)
                controller.display_roi_preview()
                break

    def adjust_all_sizes(self):
        self.roi_config_widget.adjustSize()
        return

    def connect_widgets(self, controller):
        # FIXME Signal are no longer supported
        for box in self.roi_input_boxes:
            box.connect_widgets(controller)
        self.btn_create_roi.clicked.connect(self.controller.add_new_roi_clicked)
        self.btn_delete_roi.clicked.connect(self.controller.delete_roi_clicked)

    def clear(self):
        for input_box in self.roi_input_boxes:
            self.vertLO_roi_config.removeWidget(input_box)
            input_box.deleteLater()
        self.roi_input_boxes = []
        self.adjust_all_sizes()

    def retranslate_tab_roi(self):
        self.lbl_roi.setToolTip(_translate("tracker_main_widget", "<html><head/><body><p>Define the Area in which the Fish shall be detected. Point (0,0) is the upper left corner.</p></body></html>", None))
        self.lbl_roi.setText(_translate("tracker_main_widget", "Region of interest", None))
        self.btn_create_roi.setText(_translate("btn_create_roi", "Create ROI", None))
        self.btn_delete_roi.setText(_translate("btn_delete_roi", "Delete ROI", None))
        self.lbl_new_roi_name.setText(_translate("lbl_new_roi_name", "name of ROI:", None))
        for box in self.roi_input_boxes:
            box.retranslate_roi_input_box()
