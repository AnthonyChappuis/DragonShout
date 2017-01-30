#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for main window of the application
#
#Application: DragonShout music sampler
#Last Edited: September 13th 2016
#---------------------------------

from constants import *
from classes.interface.Text import Text

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp

class MainWindow(QMainWindow):

    def __init__(self,application:QApplication):
        super().__init__()
        screen = application.desktop().screenGeometry()

        self.setGeometry(50, 50, screen.width(), screen.height())
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon('dragonShout.png'))

        text = Text('english')

        #Creating status bar
        self.statusBar().showMessage('Ready')
        self.statusBar().setGeometry(0, self.height()-self.height()/20, self.width(), self.height()/20)

        #Creating menu bar
        menuBar = self. menuBar()

        #Creating file menu
        #Defining file menu actions
        action = QAction(QIcon('exit.png'), text.localisation('menuEntries','exit','caption'), self)
        action.setShortcut('Alt+F4')
        action.setStatusTip(text.localisation('menuEntries','exit','toolTip'))
        action.triggered.connect(qApp.quit)

        fileMenu = menuBar.addMenu(text.localisation('menus','files','caption'))
        fileMenu.addAction(action)

        #Creating Options menu
        #Defining Options menu actions
        action = QAction(QIcon('language.png'), text.localisation('menuEntries','language','caption'),self)
        action.setStatusTip(text.localisation('menuEntries','language','toolTip'))

        optionsMenu = menuBar.addMenu(text.localisation('menus','options','caption'))
        optionsMenu.addAction(action)

        self.show()
