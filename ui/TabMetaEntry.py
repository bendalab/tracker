from PyQt4 import QtGui, QtCore

class TabMetaEntry(QtGui.QScrollArea):
    def __init__(self, name, path):
        super(TabMetaEntry, self).__init__()

        model = QtCore.QModel
        tree_view = QtGui.QTreeView()