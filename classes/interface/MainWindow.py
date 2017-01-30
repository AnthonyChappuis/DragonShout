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

        self.text = ''
        self.menuBar()
        self.changeLanguage()

        self.show()

    def setGUI(self):
        #Creating status bar
        self.statusBar().showMessage('Ready')

        #Creating menu bar
        self.menuBar().clear()
        menuBar = self.menuBar()

        #Creating file menu
        #Defining file menu actions
        action = QAction(QIcon('exit.png'), self.text.localisation('menuEntries','exit','caption'), self)
        action.setShortcut('Alt+F4')
        action.setStatusTip(self.text.localisation('menuEntries','exit','toolTip'))
        action.triggered.connect(qApp.quit)

        fileMenu = menuBar.addMenu(self.text.localisation('menus','files','caption'))
        fileMenu.addAction(action)

        #Creating Options menu and entries

        optionsMenu = menuBar.addMenu(self.text.localisation('menus','options','caption'))
        languageMenu = optionsMenu.addMenu(self.text.localisation('menuEntries','language','caption'))

        #Creating language actions
        action = QAction(QIcon('England.png'), 'English',self)
        action.triggered.connect(lambda *args: self.changeLanguage('english'))
        languageMenu.addAction(action)
        action = QAction(QIcon('France.png'), 'Français',self)
        action.triggered.connect(lambda *args: self.changeLanguage('french'))
        languageMenu.addAction(action)

    def changeLanguage(self,language:str='english'):
            self.text = Text(language)
            self.setGUI()
