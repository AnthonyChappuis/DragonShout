#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from constants import *
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget


if __name__ == '__main__':

    app = QApplication(sys.argv)

    screen = app.desktop().screenGeometry()

    mainWindow = QWidget()
    mainWindow.resize(screen.width(),screen.height())
    mainWindow.move(0,0)
    mainWindow.setWindowTitle(APP_NAME)
    mainWindow.setWindowIcon(QIcon('dragonShout.png'))
    mainWindow.show()

    sys.exit(app.exec_())
