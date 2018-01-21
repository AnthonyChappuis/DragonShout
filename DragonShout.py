#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import platform
import ctypes
from classes.interface.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__.endswith('__main__'):

    if platform.system() == "Windows":
        #This insure that the application icon will appear on windows task bar.
        myappid = 'AnthonyChappuis.DragonShout'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        #-------------------

    application = QApplication(sys.argv)
    application.setApplicationName(MainWindow.APPLICATIONNAME)

    window = MainWindow(application)

    sys.exit(application.exec_())
