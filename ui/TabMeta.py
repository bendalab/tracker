from PyQt4 import QtGui, QtCore
from MyQLine import MyQLine
from core.MetaEntry import MetaEntry
from TabMetaEntry import TabMetaEntry

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

        self.meta_entry_tabs = []

        self.name = "tab_meta"

        self.browse_tab = QtGui.QWidget()

        self.vert_LO_browse_tab = QtGui.QVBoxLayout(self.browse_tab)
        self.vert_LO_browse_tab.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        self.ln_edit_browse_template = QtGui.QLineEdit()
        self.vert_LO_browse_tab.addWidget(self.ln_edit_browse_template)
        self.ho_LO_buttons = QtGui.QHBoxLayout()
        self.vert_LO_browse_tab.addLayout(self.ho_LO_buttons)
        self.btn_template_browse = QtGui.QPushButton()
        self.btn_template_browse.setObjectName("btn_template_browse")
        self.ho_LO_buttons.addWidget(self.btn_template_browse)
        self.btn_template_add = QtGui.QPushButton()
        self.btn_template_add.setObjectName("btn_template_add")
        self.ho_LO_buttons.addWidget(self.btn_template_add)
        self.vert_LO_browse_tab.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        self.ln_edit_remove_template = QtGui.QLineEdit()
        self.vert_LO_browse_tab.addWidget(self.ln_edit_remove_template)
        self.btn_template_remove = QtGui.QPushButton()
        self.btn_template_remove.setObjectName("btn_template_remove")
        self.vert_LO_browse_tab.addWidget(self.btn_template_remove)
        self.vert_LO_browse_tab.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))

        self.addTab(self.browse_tab, "templates")

        self.setWhatsThis(_fromUtf8(""))
        self.setObjectName(_fromUtf8("tab_meta"))

        # vertLO meta tab
        self.vert_LO_tab_meta = QtGui.QVBoxLayout(self)
        self.vert_LO_tab_meta.setObjectName(_fromUtf8("vert_LO_tab_meta"))

        # spacer
        self.vert_LO_tab_meta.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))

    def add_tab_meta_entry(self, meta_entry):
        new_tab = TabMetaEntry(meta_entry.path, meta_entry.name)
        self.meta_entry_tabs.append(new_tab)
        self.addTab(new_tab, meta_entry.name)

    # TODO
    def connect_widgets(self, controller):
        self.btn_template_browse.clicked.connect(controller.btn_template_browse_clicked)
        self.btn_template_add.clicked.connect(controller.btn_template_add_clicked)
        self.btn_template_remove.clicked.connect(controller.btn_template_remove_clicked)
        return

    def retranslate_tab_meta(self):
        self.btn_template_browse.setText(_translate(self.name, "Browse Template", None))
        self.btn_template_remove.setText(_translate(self.name, "Remove Template", None))
        self.btn_template_add.setText(_translate(self.name, "Add", None))
        pass