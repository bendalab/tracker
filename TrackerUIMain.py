#! /usr/bin/env python

import sys
from PyQt5 import QtWidgets
from ui.TrackerUI import TrackerUserInterface

if __name__ == "__main__":
    qApp = QtWidgets.QApplication(sys.argv)
    ui_tr = TrackerUserInterface()
    ui_tr.resize(800, 600)
    ui_tr.center()
    ui_tr.show()
    sys.exit(qApp.exec_())
