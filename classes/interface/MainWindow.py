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

from PyQt5 import Qt, QtGui
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
    QGridLayout, QPushButton, QWidget, QListWidget, QLabel)

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
        fileMenu = menuBar.addMenu(self.text.localisation('menus','files','caption'))

        action = QAction(QIcon('save.png'), self.text.localisation('menuEntries','save','caption'), self)
        action.setShortcut('Ctrl+s')
        action.setStatusTip(self.text.localisation('menuEntries','save','toolTip'))
#       action.triggered.connect(qApp.quit)

        fileMenu.addAction(action)

        action = QAction(QIcon('exit.png'), self.text.localisation('menuEntries','exit','caption'), self)
        action.setShortcut('Alt+F4')
        action.setStatusTip(self.text.localisation('menuEntries','exit','toolTip'))
        action.triggered.connect(qApp.quit)

        fileMenu.addAction(action)


        #Creating Options menu and entries

        optionsMenu = menuBar.addMenu(self.text.localisation('menus','options','caption'))
        languageMenu = optionsMenu.addMenu(self.text.localisation('menuEntries','language','caption'))

        #Creating language actions
        action = QAction(QIcon('ressources/interface/england.png'), 'English',self)
        action.triggered.connect(lambda *args: self.changeLanguage('english'))
        languageMenu.addAction(action)
        action = QAction(QIcon('ressources/interface/France.png'), 'Français',self)
        action.triggered.connect(lambda *args: self.changeLanguage('french'))
        languageMenu.addAction(action)

        #Grid layout containing all other elements of MainWindow
        grid = QGridLayout()
        windowWidth = self.geometry().width()

        #Scene list
        sceneList = QListWidget()
        grid.addWidget(sceneList,0,0,0,1)

        default = QWidget()
        default.setMinimumWidth(windowWidth/2)
        grid.addWidget(default,0,1,0,1)

        #Label of the currant playlist
        playlistLabel = QLabel('Playlist label')
        playlistLabel.setAlignment(Qt.Qt.AlignCenter)
        grid.addWidget(playlistLabel,0,2)

        grid.addWidget(QListWidget(),1,2)
        grid.addWidget(QListWidget(),2,2)

        centralWidget = QWidget(self)
        centralWidget.setLayout(grid)

        self.setCentralWidget(centralWidget)

    def changeLanguage(self,language:str='english'):
            self.text = Text(language)
            self.setGUI()
