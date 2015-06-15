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


class TabFileBatch(QtGui.QWidget):
    def __init__(self):
        super(TabFileBatch, self).__init__()

        self.setWhatsThis(_fromUtf8(""))
        self.setObjectName(_fromUtf8("tab_file"))

        self.vert_lo_tab_file_batch = QtGui.QVBoxLayout(self)
        self.vert_lo_tab_file_batch.setObjectName("vert_lo_main")

        self.btn_to_single = QtGui.QPushButton()
        self.btn_to_single.setObjectName("btn_to_single")
        self.vert_lo_tab_file_batch.addWidget(self.btn_to_single)

    def retranslate_tab_file_batch(self):
        self.btn_to_single.setText("Switch to single tracking")

    def connect_widgets(self, controller):
        self.btn_to_single.clicked.connect(controller.btn_to_single_clicked)