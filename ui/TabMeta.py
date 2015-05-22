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


class TabMeta(QtGui.QWidget):
    def __init__(self):
        super(TabMeta, self).__init__()

        self.name = "tab_meta"

        self.setWhatsThis(_fromUtf8(""))
        self.setObjectName(_fromUtf8("tab_meta"))

        # vertLO meta tab
        self.vert_LO_tab_meta = QtGui.QVBoxLayout(self)
        self.vert_LO_tab_meta.setObjectName(_fromUtf8("vert_LO_tab_meta"))

        # spacer
        spacer_item = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vert_LO_tab_meta.addItem(spacer_item)

        # line
        self.line = MyQLine(self, "line")
        self.vert_LO_tab_meta.addWidget(self.line)

        # label experimenter
        self.lbl_experimenter = QtGui.QLabel(self)
        self.lbl_experimenter.setObjectName(_fromUtf8("lbl_experimenter"))
        self.vert_LO_tab_meta.addWidget(self.lbl_experimenter)

        # line edit experimenter
        self.ln_edit_experimenter = QtGui.QLineEdit(self)
        self.ln_edit_experimenter.setObjectName(_fromUtf8("lnEdit_experimenter"))
        self.vert_LO_tab_meta.addWidget(self.ln_edit_experimenter)

        # line
        self.line_2 = MyQLine(self, "line_2")
        self.vert_LO_tab_meta.addWidget(self.line_2)

        # label fish_id
        self.lbl_fish_id = QtGui.QLabel(self)
        self.lbl_fish_id.setObjectName(_fromUtf8("lbl_fish_id"))
        self.vert_LO_tab_meta.addWidget(self.lbl_fish_id)

        # line edit fish_id
        self.ln_edit_fish_id = QtGui.QLineEdit(self)
        self.ln_edit_fish_id.setObjectName(_fromUtf8("lnEdit_fish_id"))
        self.vert_LO_tab_meta.addWidget(self.ln_edit_fish_id)

        # line
        self.line_2 = MyQLine(self, "line_2")
        self.vert_LO_tab_meta.addWidget(self.line_2)

        # TODO are those needed? maybe import video meta file?
        # # spacer
        # spacer_item_2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        # self.vert_LO_tab_meta.addItem(spacer_item_2)
        #
        # # line
        # self.line_2 = MyQLine(self, "line_2")
        # self.vert_LO_tab_meta.addWidget(self.line_2)
        #
        # # label camera model
        # self.lbl_camera_model = QtGui.QLabel(self)
        # self.lbl_camera_model.setObjectName(_fromUtf8("lbl_camera_model"))
        # self.vert_LO_tab_meta.addWidget(self.lbl_camera_model)
        #
        # # line edit camera model
        # self.ln_edit_camera_model = QtGui.QLineEdit(self)
        # self.ln_edit_camera_model.setObjectName(_fromUtf8("lnEdit_camera_model"))
        # self.vert_LO_tab_meta.addWidget(self.ln_edit_camera_model)
        #
        # # line
        # self.line_2 = MyQLine(self, "line_2")
        # self.vert_LO_tab_meta.addWidget(self.line_2)
        #
        # # label camera vendor
        # self.lbl_camera_vendor = QtGui.QLabel(self)
        # self.lbl_camera_vendor.setObjectName(_fromUtf8("lbl_camera_vendor"))
        # self.vert_LO_tab_meta.addWidget(self.lbl_camera_vendor)
        #
        # # line edit camera vendor
        # self.ln_edit_camera_vendor = QtGui.QLineEdit(self)
        # self.ln_edit_camera_vendor.setObjectName(_fromUtf8("lnEdit_camera_vendor"))
        # self.vert_LO_tab_meta.addWidget(self.ln_edit_camera_vendor)

        # spacer
        self.vert_LO_tab_meta.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))

    # TODO
    def connect_widgets(self, controller):
        #
        return

    def retranslate_tab_meta(self):
        self.lbl_experimenter.setText(_translate(self.name, "Experimenter", None))
        self.lbl_fish_id.setText(_translate(self.name, "Fish ID", None))
        # self.lbl_camera_model.setText(_translate(self.name, "Camera Model", None))
        # self.lbl_camera_vendor.setText(_translate(self.name, "Camera Vendor", None))