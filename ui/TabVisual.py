from PyQt5 import QtWidgets, QtCore
from MyQLine import MyQLine

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


class TabVisual(QtWidgets.QWidget):
    def __init__(self):
        super(TabVisual, self).__init__()

        self.setObjectName(_fromUtf8("tab_visual"))
        # vertical layout visuals tab
        self.vertLO_tab_visual = QtWidgets.QVBoxLayout(self)
        self.vertLO_tab_visual.setObjectName(_fromUtf8("vertLO_tab_visual"))
        # spacer
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                             QtWidgets.QSizePolicy.Expanding)
        self.vertLO_tab_visual.addItem(spacerItem12)
        # line
        self.line_13 = MyQLine(self, "line_13")
        self.vertLO_tab_visual.addWidget(self.line_13)

        # label image processing steps
        self.lbl_img_proc_steps = QtWidgets.QLabel(self)
        self.lbl_img_proc_steps.setObjectName(_fromUtf8("lbl_img_proc_steps"))
        # vertical layout show processing steps enable
        self.vertLO_tab_visual.addWidget(self.lbl_img_proc_steps)
        # checkbox show background subtracted image
        self.cbx_show_bgsub_img = QtWidgets.QCheckBox(self)
        self.cbx_show_bgsub_img.setObjectName(_fromUtf8("cbx_show_bgsub_img"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_bgsub_img)
        # checkbox show morphed image
        self.cbx_show_morph_img = QtWidgets.QCheckBox(self)
        self.cbx_show_morph_img.setObjectName(_fromUtf8("cbx_show_morph_img"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_morph_img)
        # checkbox show contour image
        self.cbx_show_contour = QtWidgets.QCheckBox(self)
        self.cbx_show_contour.setObjectName(_fromUtf8("cbx_show_contour"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_contour)
        # checkbox show ellipse
        self.cbx_show_ellipse = QtWidgets.QCheckBox(self)
        self.cbx_show_ellipse.setObjectName(_fromUtf8("cbx_show_ellipse"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_ellipse)
        # checkbox show ellipse
        self.cbx_show_orientation = QtWidgets.QCheckBox(self)
        self.cbx_show_orientation.setObjectName(_fromUtf8("cbx_show_orientation"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_orientation)

        # line
        self.line_14 = MyQLine(self, "line_14")
        self.vertLO_tab_visual.addWidget(self.line_14)
        # spacer
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                             QtWidgets.QSizePolicy.Expanding)
        self.vertLO_tab_visual.addItem(spacerItem13)

        # line
        self.line_11 = MyQLine(self, "line_11")
        self.vertLO_tab_visual.addWidget(self.line_11)

        # grid layout data visualisation
        self.gridLO_data_visual = QtWidgets.QGridLayout()
        self.gridLO_data_visual.setObjectName(_fromUtf8("gridLO_data_visual"))
        # label  data visualization
        self.lbl_data_visualisation = QtWidgets.QLabel(self)
        self.lbl_data_visualisation.setObjectName(_fromUtf8("lbl_data_visualisation"))
        self.gridLO_data_visual.addWidget(self.lbl_data_visualisation, 0, 0, 1, 1)
        # label line offset
        self.lbl_line_offset = QtWidgets.QLabel(self)
        self.lbl_line_offset.setObjectName(_fromUtf8("lbl_line_offset"))
        self.gridLO_data_visual.addWidget(self.lbl_line_offset, 1, 0, 1, 1)
        # spinbox lineend offset
        self.spinBox_lineend_offset = QtWidgets.QSpinBox(self)
        self.spinBox_lineend_offset.setMinimum(0)
        self.spinBox_lineend_offset.setMaximum(20)
        self.spinBox_lineend_offset.setEnabled(False)
        self.spinBox_lineend_offset.setObjectName(_fromUtf8("spinBox_lineend_offset"))
        self.gridLO_data_visual.addWidget(self.spinBox_lineend_offset, 1, 1, 1, 1)
        # label circle size
        self.lbl_circle_size = QtWidgets.QLabel(self)
        self.lbl_circle_size.setObjectName(_fromUtf8("lbl_circle_size"))
        self.gridLO_data_visual.addWidget(self.lbl_circle_size, 2, 0, 1, 1)
        # spinbox circle size
        self.spinBox_circle_size = QtWidgets.QSpinBox(self)
        self.spinBox_circle_size.setMinimum(1)
        self.spinBox_circle_size.setMaximum(10)
        self.spinBox_circle_size.setObjectName(_fromUtf8("spinBox_circle_size"))
        self.gridLO_data_visual.addWidget(self.spinBox_circle_size, 2, 1, 1, 1)
        # add data visualization layout
        self.vertLO_tab_visual.addLayout(self.gridLO_data_visual)
        # line
        self.line_12 = MyQLine(self, "line_12")
        self.vertLO_tab_visual.addWidget(self.line_12)
        # spacer
        spacerItem14 = QtWidgets.QSpacerItem(20, 119, QtWidgets.QSizePolicy.Minimum,
                                             QtWidgets.QSizePolicy.Expanding)
        self.vertLO_tab_visual.addItem(spacerItem14)

    def connect_widgets(self, controller):
        # FIXME Signal and slots
        self.cbx_show_bgsub_img.stateChanged.connect(controller.change_show_bg_sub_img)
        self.cbx_show_morph_img.stateChanged.connect(controller.change_show_morphed_img)
        self.cbx_show_contour.stateChanged.connect(controller.change_draw_contour)
        self.cbx_show_ellipse.stateChanged.connect(controller.change_draw_ellipse)
        self.cbx_show_orientation.stateChanged.connect(controller.change_show_orientation)

        self.spinBox_lineend_offset.valueChanged.connect(controller.change_lineend_offset)
        self.spinBox_circle_size.valueChanged.connect(controller.change_circle_size)
        return

    def retranslate_tab_visual(self):
        self.lbl_img_proc_steps.setText(_translate("tracker_main_widget", "Image Processing Steps", None))
        self.cbx_show_bgsub_img.setText(_translate("tracker_main_widget", "Show Background-subtracted Image", None))
        self.cbx_show_morph_img.setText(_translate("tracker_main_widget", "Show Morphed Image", None))
        self.cbx_show_contour.setText(_translate("tracker_main_widget", "Show Contours", None))
        self.cbx_show_ellipse.setText(_translate("tracker_main_widget", "Show fitted Ellipse", None))
        self.cbx_show_orientation.setText(_translate("tracker_main_widget", "Show Fish Orientation", None))
        self.lbl_circle_size.setText(_translate("tracker_main_widget", "Circle Size", None))
        self.lbl_line_offset.setText(_translate("tracker_main_widget", "Lineend Offset", None))
        self.lbl_data_visualisation.setText(_translate("tracker_main_widget", "Data Visualisation", None))
