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
        self.name = "tab_file_batch"
        self.setObjectName(_fromUtf8(self.name))

        self.vert_lo_tab_file_batch = QtGui.QVBoxLayout(self)
        self.vert_lo_tab_file_batch.setObjectName("vert_lo_main")

        self.btn_to_single = QtGui.QPushButton()
        self.btn_to_single.setObjectName("btn_to_single")
        self.vert_lo_tab_file_batch.addWidget(self.btn_to_single)

         # spacer
        spacer_item = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vert_lo_tab_file_batch.addItem(spacer_item)

        # line
        self.line = MyQLine(self, "line")
        self.vert_lo_tab_file_batch.addWidget(self.line)

        # label file path
        self.lbl_file_path = QtGui.QLabel(self)
        self.lbl_file_path.setObjectName(_fromUtf8("lbl_file_path"))
        self.vert_lo_tab_file_batch.addWidget(self.lbl_file_path)

        # line edit file path
        self.lnEdit_file_path = QtGui.QLineEdit(self)
        self.lnEdit_file_path.setObjectName(_fromUtf8("lnEdit_file_path"))
        self.vert_lo_tab_file_batch.addWidget(self.lnEdit_file_path)

        # button browse folder
        self.btn_browse_directory = QtGui.QPushButton(self)
        self.btn_browse_directory.setObjectName(_fromUtf8("btn_browse_file"))
        self.vert_lo_tab_file_batch.addWidget(self.btn_browse_directory)

        # line
        self.line_2 = MyQLine(self, "line_2")
        self.vert_lo_tab_file_batch.addWidget(self.line_2)

        # label output path
        self.lbl_output_path = QtGui.QLabel(self)
        self.lbl_output_path.setObjectName(_fromUtf8("lbl_output_path"))
        self.vert_lo_tab_file_batch.addWidget(self.lbl_output_path)

        # checkbox output is input
        self.cbx_output_is_input = QtGui.QCheckBox(self)
        self.cbx_output_is_input.setObjectName(_fromUtf8("cbx_output_is_input"))
        self.vert_lo_tab_file_batch.addWidget(self.cbx_output_is_input)

        # line edit output path
        self.lnEdit_output_path = QtGui.QLineEdit(self)
        self.lnEdit_output_path.setObjectName(_fromUtf8("lnEdit_output_path"))
        self.vert_lo_tab_file_batch.addWidget(self.lnEdit_output_path)

        # button browse output folder
        self.btn_browse_output = QtGui.QPushButton(self)
        self.btn_browse_output.setObjectName(_fromUtf8("btn_browse_file"))
        self.vert_lo_tab_file_batch.addWidget(self.btn_browse_output)

        # line
        self.line_2_1 = MyQLine(self, "line_2_1")
        self.vert_lo_tab_file_batch.addWidget(self.line_2_1)

        # spacer
        spacer_item_1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vert_lo_tab_file_batch.addItem(spacer_item_1)

        # label output path
        self.lbl_file_suffix = QtGui.QLabel(self)
        self.lbl_file_suffix.setObjectName(_fromUtf8("lbl_file_suffix"))
        self.vert_lo_tab_file_batch.addWidget(self.lbl_file_suffix)

        # line edit file suffix
        self.lnEdit_file_suffix = QtGui.QLineEdit(self)
        self.lnEdit_file_suffix.setObjectName(_fromUtf8("lnEdit_file_suffix"))
        self.vert_lo_tab_file_batch.addWidget(self.lnEdit_file_suffix)

        # checkbox add metadata
        self.cbx_add_metadata = QtGui.QCheckBox()
        self.cbx_add_metadata.setObjectName("cbx_add_metadata")
        self.vert_lo_tab_file_batch.addWidget(self.cbx_add_metadata)

        # spacer
        spacer_item_1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vert_lo_tab_file_batch.addItem(spacer_item_1)

    def retranslate_tab_file_batch(self):
        self.btn_to_single.setText("Switch to single tracking")
        self.lbl_file_path.setText(_translate(self.name, "Directory Path", None))
        self.cbx_output_is_input.setText(_translate(self.name, "Save in Input Directory", None))
        self.btn_browse_directory.setText(_translate(self.name, "Browse Directory", None))
        self.lbl_output_path.setText(_translate(self.name, "Output Path", None))
        self.btn_browse_output.setText(_translate(self.name, "Browse Output Folder", None))
        self.lbl_file_suffix.setText(_translate(self.name, "Video File Suffix", None))
        self.cbx_add_metadata.setText(_translate(self.name, "Add Metadata in File Folder containing File Name", None))

    def connect_widgets(self, controller):
        self.btn_to_single.clicked.connect(controller.btn_to_single_clicked)
        self.btn_browse_directory.clicked.connect(controller.btn_browse_directory_clicked)
        self.btn_browse_output.clicked.connect(controller.browse_output_directory)

        self.connect(self.cbx_output_is_input, QtCore.SIGNAL("stateChanged(int)"), controller.change_output_is_input)
