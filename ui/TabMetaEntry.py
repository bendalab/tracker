from PyQt4 import QtGui, QtCore
import odml

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


# maybe enough to inherit from QTreeView
#class TabMetaEntry(QtGui.QScrollArea):
class TabMetaEntry(QtGui.QWidget):
    def __init__(self, path, name, controller):
        super(TabMetaEntry, self).__init__()
        self.controller = controller

        self.name = name
        self.delete_me = False

        self.vert_LO = QtGui.QVBoxLayout(self)
        self.btn_delete_self = QtGui.QPushButton()
        self.btn_delete_self.setObjectName("btn_delete_self")
        self.btn_delete_self.setText(_translate(self.name, "Delete This", None))
        self.btn_delete_self.clicked.connect(self.delete_self_clicked)
        self.vert_LO.addWidget(self.btn_delete_self)

        self.tree_widget = QtGui.QTreeWidget()
        self.vert_LO.addWidget(self.tree_widget)

        self.parents = []
        self.tree_widget.setColumnCount(2)

        self.extract_odml_data(path)
        self.tree_widget.addTopLevelItems(self.parents)
        self.tree_widget.expandAll()
        for c in range(self.tree_widget.columnCount()):
            self.tree_widget.resizeColumnToContents(c)

    def extract_odml_data(self, path):
        odml_data = odml.tools.xmlparser.load(path)
        for s in odml_data.sections:
            tree_item = QtGui.QTreeWidgetItem()
            tree_item.setText(0, s.name)
            self.add_subsections_to_entry(tree_item, s)
            self.parents.append(tree_item)

    def add_subsections_to_entry(self, tree_item, section):
        if section.sections is not None and len(section.sections) > 0:
            for s in section.sections:
                # add subsections recursiveley
                sub_item = QtGui.QTreeWidgetItem()
                sub_item.setText(0, s.name)
                self.add_subsections_to_entry(sub_item, s)
                tree_item.addChild(sub_item)

            # add values of section
        if section.properties is not None and len(section.properties) > 0:
            for p in section.properties:
                prop_item = QtGui.QTreeWidgetItem()
                prop_item.setText(0, p.name)
                prop_item.setData(1, 0, QtCore.QVariant(QtCore.QString(str(p.value))))
                tree_item.addChild(prop_item)

    def delete_self_clicked(self):
        self.delete_me = True
        self.controller.btn_remove_self_clicked()