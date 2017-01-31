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
    QVBoxLayout, QSplitter, QFileDialog, QWidget, QListWidget, QLabel)

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
        action.setShortcut('Ctrl+q')
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
        horizontalSplitter = QSplitter()
        windowWidth = self.geometry().width()

        #Scene list
        sceneList = QListWidget()
        horizontalSplitter.addWidget(sceneList)

        #Theme selection and controls
        default = QWidget()
        horizontalSplitter.addWidget(default)

        verticalSplitter = QSplitter(Qt.Qt.Vertical)
        #Label of the currant playlist
        playlistLabel = QLabel('Playlist label')
        playlistLabel.setAlignment(Qt.Qt.AlignCenter)
        verticalSplitter.addWidget(playlistLabel)

        #Playlist of the selected theme
        verticalSplitter.addWidget(QListWidget())

        #Files on the computer
        fileBrowser = QFileDialog()
        musicPath = Qt.QDir.homePath()
        fileBrowser.setDirectory(musicPath)
        verticalSplitter.addWidget(fileBrowser)

        horizontalSplitter.addWidget(verticalSplitter)

        layout = QVBoxLayout()
        layout.addWidget(horizontalSplitter)
        centralWidget = QWidget(self)
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

    def changeLanguage(self,language:str='english'):
            self.text = Text(language)
            self.setGUI()
