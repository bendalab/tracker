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


class TabMeta(QtGui.QTabWidget):
    def __init__(self):
        super(TabMeta, self).__init__()

        self.name = "tab_meta"

        self.browse_tab = QtGui.QWidget()
        self.vert_LO_browse_tab = QtGui.QVBoxLayout(self.browse_tab)
        self.btn_meta_browse = QtGui.QPushButton()
        self.btn_meta_browse.setObjectName("btn_meta_browse")
        self.vert_LO_browse_tab.addWidget(self.btn_meta_browse)

        self.addTab(self.browse_tab, "browse templates")

        self.setWhatsThis(_fromUtf8(""))
        self.setObjectName(_fromUtf8("tab_meta"))

        # vertLO meta tab
        self.vert_LO_tab_meta = QtGui.QVBoxLayout(self)
        self.vert_LO_tab_meta.setObjectName(_fromUtf8("vert_LO_tab_meta"))

        # spacer
        self.vert_LO_tab_meta.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))

    # TODO
    def connect_widgets(self, controller):
        #
        return

    def retranslate_tab_meta(self):
        # self.lbl_experimenter.setText(_translate(self.name, "Experimenter", None))
        # self.lbl_fish_id.setText(_translate(self.name, "Fish ID", None))
        # self.lbl_camera_model.setText(_translate(self.name, "Camera Model", None))
        # self.lbl_camera_vendor.setText(_translate(self.name, "Camera Vendor", None))
        pass