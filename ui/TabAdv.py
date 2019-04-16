from PyQt5 import QtWidgets, QtCore
from .MyQLine import MyQLine

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


class TabAdv(QtWidgets.QWidget):
    def __init__(self):
        super(TabAdv, self).__init__()

        self.setObjectName(_fromUtf8("tab_adv"))
        # vertical layout adv tab
        self.vertLO_tab_adv = QtWidgets.QVBoxLayout(self)
        self.vertLO_tab_adv.setObjectName(_fromUtf8("vertLO_tab_adv"))

        # spacer
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                             QtWidgets.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem11)

        # line
        self.line_7 = MyQLine(self, "line_7")
        self.vertLO_tab_adv.addWidget(self.line_7)

        # label image morphing
        self.lbl_img_morphing = QtWidgets.QLabel(self)
        self.lbl_img_morphing.setObjectName(_fromUtf8("lbl_img_morphing"))
        self.vertLO_tab_adv.addWidget(self.lbl_img_morphing)
        # grid layout image morphing
        self.gridLO_img_morphing = QtWidgets.QGridLayout()
        self.gridLO_img_morphing.setObjectName(_fromUtf8("gridLO_img_morphing"))
        # label erosion factor
        self.lbl_erosion = QtWidgets.QLabel(self)
        self.lbl_erosion.setObjectName(_fromUtf8("lbl_erosion"))
        self.gridLO_img_morphing.addWidget(self.lbl_erosion, 1, 1, 1, 1)
        # label dilation factor
        self.lbl_dilation = QtWidgets.QLabel(self)
        self.lbl_dilation.setObjectName(_fromUtf8("lbl_dilation"))
        self.gridLO_img_morphing.addWidget(self.lbl_dilation, 4, 1, 1, 1)
        # spinbox set erosion factor
        self.spinBox_erosion = QtWidgets.QSpinBox(self)
        self.spinBox_erosion.setMinimum(0)
        self.spinBox_erosion.setObjectName(_fromUtf8("spinBox_erosion"))
        self.gridLO_img_morphing.addWidget(self.spinBox_erosion, 1, 2, 1, 1)
        # spinbox set dilation factor
        self.spinBox_dilation = QtWidgets.QSpinBox(self)
        self.spinBox_dilation.setMinimum(0)
        self.spinBox_dilation.setObjectName(_fromUtf8("spinBox_dilation"))
        self.gridLO_img_morphing.addWidget(self.spinBox_dilation, 4, 2, 1, 1)
        # add grid layout image morphing
        self.vertLO_tab_adv.addLayout(self.gridLO_img_morphing)

        # line
        self.line_8 = MyQLine(self, "line_8")
        self.vertLO_tab_adv.addWidget(self.line_8)
        # spacer
        self.vertLO_tab_adv.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                          QtWidgets.QSizePolicy.Expanding))

        # erosion and dilation matrices
        # label image morphing
        self.lbl_morph_matrices = QtWidgets.QLabel(self)
        self.lbl_morph_matrices.setObjectName(_fromUtf8("lbl_morph_matrices"))
        self.vertLO_tab_adv.addWidget(self.lbl_morph_matrices)
        # grid layout image morphing
        self.gridLO_morph_matrices = QtWidgets.QGridLayout()
        self.gridLO_morph_matrices.setObjectName(_fromUtf8("gridLO_morph_matrices"))
        # label erosion factor
        self.lbl_erosion_matrix = QtWidgets.QLabel(self)
        self.lbl_erosion_matrix.setObjectName(_fromUtf8("lbl_erosion_matrix"))
        self.gridLO_morph_matrices.addWidget(self.lbl_erosion_matrix, 1, 1, 1, 1)
        # label dilation factor
        self.lbl_dilation_matrix = QtWidgets.QLabel(self)
        self.lbl_dilation_matrix.setObjectName(_fromUtf8("lbl_dilation"))
        self.gridLO_morph_matrices.addWidget(self.lbl_dilation_matrix, 4, 1, 1, 1)
        # spinbox set erosion factor
        self.spinBox_erosion_matrix = QtWidgets.QSpinBox(self)
        self.spinBox_erosion_matrix.setMinimum(1)
        self.spinBox_erosion_matrix.setObjectName(_fromUtf8("spinBox_erosion"))
        self.gridLO_morph_matrices.addWidget(self.spinBox_erosion_matrix, 1, 2, 1, 1)
        # spinbox set dilation factor
        self.spinBox_dilation_matrix = QtWidgets.QSpinBox(self)
        self.spinBox_dilation_matrix.setMinimum(1)
        self.spinBox_dilation_matrix.setObjectName(_fromUtf8("spinBox_dilation"))
        self.gridLO_morph_matrices.addWidget(self.spinBox_dilation_matrix, 4, 2, 1, 1)
        # add grid layout image morphing
        self.vertLO_tab_adv.addLayout(self.gridLO_morph_matrices)

        # spacer
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem4)
        # line
        self.line_10 = MyQLine(self, "line_10")
        self.vertLO_tab_adv.addWidget(self.line_10)
        # spacer
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem5)
        # horizontal layout frame waittime
        self.hoLO_frame_waittime = QtWidgets.QHBoxLayout()
        self.hoLO_frame_waittime.setObjectName(_fromUtf8("hoLO_frame_waittime"))
        # label frame waittime
        self.lbl_frame_waittime = QtWidgets.QLabel(self)
        self.lbl_frame_waittime.setObjectName(_fromUtf8("lbl_frame_waittime"))
        self.hoLO_frame_waittime.addWidget(self.lbl_frame_waittime)
        # spin box frame waittime
        self.spinBox_frame_waittime = QtWidgets.QSpinBox(self)
        self.spinBox_frame_waittime.setMinimum(1)
        self.spinBox_frame_waittime.setMaximum(1000)
        self.spinBox_frame_waittime.setObjectName(_fromUtf8("spinBox_frame_waittime"))
        self.hoLO_frame_waittime.addWidget(self.spinBox_frame_waittime)
        self.vertLO_tab_adv.addLayout(self.hoLO_frame_waittime)
        # spacer
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem8)
        # line
        self.line_9 = MyQLine(self, "line_9")
        self.vertLO_tab_adv.addWidget(self.line_9)
        # spacer
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem9)
        # grid layout fishsize threshold
        self.gridLO_fishsize_th = QtWidgets.QGridLayout()
        self.gridLO_fishsize_th.setObjectName(_fromUtf8("gridLO_fishsize_th"))
        # label fishsize threshold
        self.lbl_fishsize_threshold = QtWidgets.QLabel(self)
        self.lbl_fishsize_threshold.setObjectName(_fromUtf8("lbl_fishsize_threshold"))
        self.gridLO_fishsize_th.addWidget(self.lbl_fishsize_threshold, 0, 0, 1, 1)
        # spinbox fishsize threshold
        self.spinBox_fish_threshold = QtWidgets.QSpinBox(self)
        self.spinBox_fish_threshold.setMaximum(9999)
        self.spinBox_fish_threshold.setObjectName(_fromUtf8("spinBox_fish_threshold"))
        self.gridLO_fishsize_th.addWidget(self.spinBox_fish_threshold, 0, 1, 1, 1)
        # label maximum fishsize threshold
        self.lbl_max_fishsize_threshold = QtWidgets.QLabel(self)
        self.lbl_max_fishsize_threshold.setObjectName(_fromUtf8("lbl_max_fishsize_threshold"))
        self.gridLO_fishsize_th.addWidget(self.lbl_max_fishsize_threshold, 1, 0, 1, 1)
        # spinbox maximum fishsize threshold
        self.spinBox_fish_max_threshold = QtWidgets.QSpinBox(self)
        self.spinBox_fish_max_threshold.setMaximum(9999)
        self.spinBox_fish_max_threshold.setObjectName(_fromUtf8("spinBox_fish_max_threshold"))
        self.gridLO_fishsize_th.addWidget(self.spinBox_fish_max_threshold, 1, 1, 1, 1)
        # add fishsize layout to tab layout
        self.vertLO_tab_adv.addLayout(self.gridLO_fishsize_th)
        # checkbox enable maximum size threshold
        self.cbx_enable_max_size_thresh = QtWidgets.QCheckBox(self)
        self.cbx_enable_max_size_thresh.setObjectName(_fromUtf8("cbx_enable_max_size_thresh"))
        self.vertLO_tab_adv.addWidget(self.cbx_enable_max_size_thresh)
        # spacer
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                             QtWidgets.QSizePolicy.Expanding)
        self.vertLO_tab_adv.addItem(spacerItem10)

    def connect_widgets(self, controller):
        self.spinBox_erosion.valueChanged.connect(controller.change_erosion_factor)
        self.spinBox_dilation.valueChanged.connect(controller.change_dilation_factor)

        self.spinBox_erosion_matrix.valueChanged.connect(controller.change_erosion_matrix)
        self.spinBox_dilation_matrix.valueChanged.connect(controller.change_dilation_matrix)
        self.spinBox_frame_waittime.valueChanged.connect(controller.change_frame_waittime)
        self.spinBox_fish_threshold.valueChanged.connect(controller.change_min_fish_threshold)
        self.spinBox_fish_max_threshold.valueChanged.connect(controller.change_max_fish_threshold)
        self.cbx_enable_max_size_thresh.stateChanged.connect(controller.change_enable_max_size_threshold)
        return

    def retranslate_tab_adv(self):
        self.lbl_img_morphing.setText(_translate("tracker_main_widget", "Image Morphing", None))
        self.lbl_erosion.setText(_translate("tracker_main_widget", "Erosion Faktor", None))
        self.lbl_dilation.setText(_translate("tracker_main_widget", "Dilation Faktor", None))
        self.lbl_morph_matrices.setText(_translate("tracker_main_widget", "Image Morphing Matrices", None))
        self.lbl_erosion_matrix.setText(_translate("tracker_main_widget", "Erosion Matrix", None))
        self.lbl_dilation_matrix.setText(_translate("tracker_main_widget", "Dilation Matrix", None))
        self.lbl_frame_waittime.setText(_translate("tracker_main_widget", "Frame Waittime (ms)", None))
        self.lbl_fishsize_threshold.setText(_translate("tracker_main_widget", "Fish Detection min Size Threshold", None))
        self.lbl_max_fishsize_threshold.setText(_translate("tracker_main_widget", "Fish Detection max Size Threshold", None))
        self.cbx_enable_max_size_thresh.setText(_translate("tracker_main_widget", "Enable max Size Threshold", None))
