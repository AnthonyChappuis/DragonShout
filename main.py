#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from classes.interface.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    application = QApplication(sys.argv)
    application.setApplicationName(MainWindow.ApplicationName)

    window = MainWindow(application)

    sys.exit(application.exec_())
