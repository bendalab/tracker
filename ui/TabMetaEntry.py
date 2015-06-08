from PyQt4 import QtGui, QtCore
import odml


# maybe enough to inherit from QTreeView
#class TabMetaEntry(QtGui.QScrollArea):
class TabMetaEntry(QtGui.QTreeWidget):
    def __init__(self, path, name):
        super(TabMetaEntry, self).__init__()

        self.name = name

        self.parents = []
        self.setColumnCount(2)

        self.extract_odml_data(path)
        self.addTopLevelItems(self.parents)
        self.expandAll()
        for c in range(self.columnCount()):
            self.resizeColumnToContents(c)

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