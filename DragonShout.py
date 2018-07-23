#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import platform
import ctypes

from classes.interface.MainWindow import MainWindow
from classes.ressourcesFilepath import Images

from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap

if __name__.endswith('__main__'):

    if platform.system() == "Windows":
        #This insure that the application icon will appear on windows task bar.
        myappid = 'Dragoncave.DragonShout'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        #-------------------

    application = QApplication(sys.argv)
    application.setApplicationName(MainWindow.APPLICATIONNAME)

    splashScreen = QSplashScreen(QPixmap(Images.applicationIcon))
    splashScreen.show()

    window = MainWindow(application)
    splashScreen.finish(window)


    sys.exit(application.exec_())
