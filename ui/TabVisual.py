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


class TabVisual(QtGui.QWidget):
    def __init__(self):
        super(TabVisual, self).__init__()

        self.setObjectName(_fromUtf8("tab_visual"))
        # vertical layout visuals tab
        self.vertLO_tab_visual = QtGui.QVBoxLayout(self)
        self.vertLO_tab_visual.setObjectName(_fromUtf8("vertLO_tab_visual"))
        # spacer
        spacerItem11 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_visual.addItem(spacerItem11)
        # line
        self.line_7 = MyQLine(self, "line_7")
        self.vertLO_tab_visual.addWidget(self.line_7)
        # label image morphing
        self.lbl_img_morphing = QtGui.QLabel(self)
        self.lbl_img_morphing.setObjectName(_fromUtf8("lbl_img_morphing"))
        self.vertLO_tab_visual.addWidget(self.lbl_img_morphing)
        # grid layout image morphing
        self.gridLO_img_morphing = QtGui.QGridLayout()
        self.gridLO_img_morphing.setObjectName(_fromUtf8("gridLO_img_morphing"))
        # label erosion factor
        self.lbl_erosion = QtGui.QLabel(self)
        self.lbl_erosion.setObjectName(_fromUtf8("lbl_erosion"))
        self.gridLO_img_morphing.addWidget(self.lbl_erosion, 1, 1, 1, 1)
        # label dilation factor
        self.lbl_dilation = QtGui.QLabel(self)
        self.lbl_dilation.setObjectName(_fromUtf8("lbl_dilation"))
        self.gridLO_img_morphing.addWidget(self.lbl_dilation, 4, 1, 1, 1)
        # spinbox set erosion factor
        self.spinBox_erosion = QtGui.QSpinBox(self)
        self.spinBox_erosion.setMinimum(0)
        self.spinBox_erosion.setObjectName(_fromUtf8("spinBox_erosion"))
        self.gridLO_img_morphing.addWidget(self.spinBox_erosion, 1, 2, 1, 1)
        # spinbox set dilation factor
        self.spinBox_dilation = QtGui.QSpinBox(self)
        self.spinBox_dilation.setMinimum(0)
        self.spinBox_dilation.setObjectName(_fromUtf8("spinBox_dilation"))
        self.gridLO_img_morphing.addWidget(self.spinBox_dilation, 4, 2, 1, 1)
        # add grid layout image morphing
        self.vertLO_tab_visual.addLayout(self.gridLO_img_morphing)

        # line
        self.line_8 = MyQLine(self, "line_8")
        self.vertLO_tab_visual.addWidget(self.line_8)
        # spacer
        spacerItem12 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_visual.addItem(spacerItem12)
        # line
        self.line_13 = MyQLine(self, "line_13")
        self.vertLO_tab_visual.addWidget(self.line_13)

        # label image processing steps
        self.lbl_img_proc_steps = QtGui.QLabel(self)
        self.lbl_img_proc_steps.setObjectName(_fromUtf8("lbl_img_proc_steps"))
        # vertical layout show processing steps enable
        self.vertLO_tab_visual.addWidget(self.lbl_img_proc_steps)
        # checkbox show background subtracted image
        self.cbx_show_bgsub_img = QtGui.QCheckBox(self)
        self.cbx_show_bgsub_img.setObjectName(_fromUtf8("cbx_show_bgsub_img"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_bgsub_img)
        # checkbox show morphed image
        self.cbx_show_morph_img = QtGui.QCheckBox(self)
        self.cbx_show_morph_img.setObjectName(_fromUtf8("cbx_show_morph_img"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_morph_img)
        # checkbox show contour image
        self.cbx_show_contour = QtGui.QCheckBox(self)
        self.cbx_show_contour.setObjectName(_fromUtf8("cbx_show_contour"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_contour)
        # checkbox show ellipse
        self.cbx_show_ellipse = QtGui.QCheckBox(self)
        self.cbx_show_ellipse.setObjectName(_fromUtf8("cbx_show_ellipse"))
        self.vertLO_tab_visual.addWidget(self.cbx_show_ellipse)

        # line
        self.line_14 = MyQLine(self, "line_14")
        self.vertLO_tab_visual.addWidget(self.line_14)
        # spacer
        spacerItem13 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_visual.addItem(spacerItem13)
        # line
        self.line_11 = MyQLine(self, "line_11")
        self.vertLO_tab_visual.addWidget(self.line_11)

        # grid layout data visualisation
        self.gridLO_data_visual = QtGui.QGridLayout()
        self.gridLO_data_visual.setObjectName(_fromUtf8("gridLO_data_visual"))
        # label  data visualization
        self.lbl_data_visualisation = QtGui.QLabel(self)
        self.lbl_data_visualisation.setObjectName(_fromUtf8("lbl_data_visualisation"))
        self.gridLO_data_visual.addWidget(self.lbl_data_visualisation, 0, 0, 1, 1)
        # label line offset
        self.lbl_line_offset = QtGui.QLabel(self)
        self.lbl_line_offset.setObjectName(_fromUtf8("lbl_line_offset"))
        self.gridLO_data_visual.addWidget(self.lbl_line_offset, 1, 0, 1, 1)
        # spinbox lineend offset
        self.spinBox_lineend_offset = QtGui.QSpinBox(self)
        self.spinBox_lineend_offset.setMinimum(0)
        self.spinBox_lineend_offset.setMaximum(20)
        self.spinBox_lineend_offset.setObjectName(_fromUtf8("spinBox_lineend_offset"))
        self.gridLO_data_visual.addWidget(self.spinBox_lineend_offset, 1, 1, 1, 1)
        # label circle size
        self.lbl_circle_size = QtGui.QLabel(self)
        self.lbl_circle_size.setObjectName(_fromUtf8("lbl_circle_size"))
        self.gridLO_data_visual.addWidget(self.lbl_circle_size, 2, 0, 1, 1)
        # spinbox circle size
        self.spinBox_circle_size = QtGui.QSpinBox(self)
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
        spacerItem14 = QtGui.QSpacerItem(20, 119, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_visual.addItem(spacerItem14)

    def connect_widgets(self, controller):
        self.connect(self.spinBox_erosion, QtCore.SIGNAL("valueChanged(int)"), controller.change_erosion_factor)
        self.connect(self.spinBox_dilation, QtCore.SIGNAL("valueChanged(int)"), controller.change_dilation_factor)

        self.connect(self.cbx_show_bgsub_img, QtCore.SIGNAL("stateChanged(int)"), controller.change_show_bg_sub_img)
        self.connect(self.cbx_show_morph_img, QtCore.SIGNAL("stateChanged(int)"), controller.change_show_morphed_img)
        self.connect(self.cbx_show_contour, QtCore.SIGNAL("stateChanged(int)"), controller.change_draw_contour)
        self.connect(self.cbx_show_ellipse, QtCore.SIGNAL("stateChanged(int)"), controller.change_draw_ellipse)

        self.connect(self.spinBox_lineend_offset, QtCore.SIGNAL("valueChanged(int)"), controller.change_lineend_offset)
        self.connect(self.spinBox_circle_size, QtCore.SIGNAL("valueChanged(int)"), controller.change_circle_size)
        return

    def retranslate_tab_visual(self):
        self.lbl_img_morphing.setText(_translate("tracker_main_widget", "Image Morphing", None))
        self.lbl_erosion.setText(_translate("tracker_main_widget", "Erosion Faktor", None))
        self.lbl_dilation.setText(_translate("tracker_main_widget", "Dilation Faktor", None))
        self.lbl_img_proc_steps.setText(_translate("tracker_main_widget", "Image Processing Steps", None))
        self.cbx_show_bgsub_img.setText(_translate("tracker_main_widget", "Show Background-subtracted Image", None))
        self.cbx_show_morph_img.setText(_translate("tracker_main_widget", "Show Morphed Image", None))
        self.cbx_show_contour.setText(_translate("tracker_main_widget", "Show Contours", None))
        self.cbx_show_ellipse.setText(_translate("tracker_main_widget", "Show fitted Ellipse", None))
        self.lbl_circle_size.setText(_translate("tracker_main_widget", "Circle Size", None))
        self.lbl_line_offset.setText(_translate("tracker_main_widget", "Lineend Offset", None))
        self.lbl_data_visualisation.setText(_translate("tracker_main_widget", "Data Visualisation", None))