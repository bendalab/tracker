#! /usr/bin/env python

import sys
from PyQt4 import QtGui
from ui.TrackerUI import TrackerUserInterface

if __name__ == "__main__":
    print "ignore Gtk-warning..."
    qApp = QtGui.QApplication(sys.argv)
    ui_tr = TrackerUserInterface()
    ui_tr.center_ui(qApp)
    ui_tr.show()
    sys.exit(qApp.exec_())