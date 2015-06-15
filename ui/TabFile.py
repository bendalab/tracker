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


class TabFile(QtGui.QWidget):
    def __init__(self):
        super(TabFile, self).__init__()

        self.name = "tab_file"

        self.setWhatsThis(_fromUtf8(""))
        self.setObjectName(_fromUtf8("tab_file"))
        # vertLO file tab
        self.vertLO_tab_file = QtGui.QVBoxLayout(self)
        self.vertLO_tab_file.setObjectName(_fromUtf8("vertLO_tab_file"))

        # change to batch button
        self.btn_to_batch = QtGui.QPushButton()
        self.btn_to_batch.setObjectName("btn_to_batch")
        self.vertLO_tab_file.addWidget(self.btn_to_batch)

        # spacer
        spacer_item = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_file.addItem(spacer_item)

        # line
        self.line = MyQLine(self, "line")
        self.vertLO_tab_file.addWidget(self.line)

        # label file path
        self.lbl_file_path = QtGui.QLabel(self)
        self.lbl_file_path.setObjectName(_fromUtf8("lbl_file_path"))
        self.vertLO_tab_file.addWidget(self.lbl_file_path)

        # line edit file path
        self.lnEdit_file_path = QtGui.QLineEdit(self)
        self.lnEdit_file_path.setObjectName(_fromUtf8("lnEdit_file_path"))
        self.vertLO_tab_file.addWidget(self.lnEdit_file_path)

        # button browse file
        self.btn_browse_file = QtGui.QPushButton(self)
        self.btn_browse_file.setObjectName(_fromUtf8("btn_browse_file"))
        self.vertLO_tab_file.addWidget(self.btn_browse_file)

        # line
        self.line_2 = MyQLine(self, "line_2")
        self.vertLO_tab_file.addWidget(self.line_2)

        # label output path
        self.lbl_output_path = QtGui.QLabel(self)
        self.lbl_output_path.setObjectName(_fromUtf8("lbl_output_path"))
        self.vertLO_tab_file.addWidget(self.lbl_output_path)

        # checkbox output is input
        self.cbx_output_is_input = QtGui.QCheckBox(self)
        self.cbx_output_is_input.setObjectName(_fromUtf8("cbx_output_is_input"))
        self.vertLO_tab_file.addWidget(self.cbx_output_is_input)

        # line edit output path
        self.lnEdit_output_path = QtGui.QLineEdit(self)
        self.lnEdit_output_path.setObjectName(_fromUtf8("lnEdit_output_path"))
        self.vertLO_tab_file.addWidget(self.lnEdit_output_path)

        # button browse output folder
        self.btn_browse_output = QtGui.QPushButton(self)
        self.btn_browse_output.setObjectName(_fromUtf8("btn_browse_file"))
        self.vertLO_tab_file.addWidget(self.btn_browse_output)

        # line
        self.line_2_1 = MyQLine(self, "line_2_1")
        self.vertLO_tab_file.addWidget(self.line_2_1)

        # spacer
        spacer_item_1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vertLO_tab_file.addItem(spacer_item_1)

        # # complete file tab
        # self.tab_widget_options.addTab(self, _fromUtf8(""))

    def connect_widgets(self, controller):
        self.btn_browse_file.clicked.connect(controller.browse_file)
        self.btn_browse_output.clicked.connect(controller.browse_output_directory)

        self.connect(self.cbx_output_is_input, QtCore.SIGNAL("stateChanged(int)"), controller.change_output_is_input)
        return

    def retranslate_tab_file(self):
        self.lbl_file_path.setText(_translate(self.name, "File Path", None))
        self.cbx_output_is_input.setText(_translate(self.name, "Save in Input Directory", None))
        self.btn_browse_file.setText(_translate(self.name, "Browse File", None))
        self.lbl_output_path.setText(_translate(self.name, "Output Path", None))
        self.btn_browse_output.setText(_translate(self.name, "Browse Output Folder", None))