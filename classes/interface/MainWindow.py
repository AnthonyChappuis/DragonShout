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

import os
from classes.library.Library import Library

from PyQt5 import Qt, QtGui, QtCore
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
    QHBoxLayout, QSplitter, QFileDialog, QWidget, QListWidget, QLabel,
    QPushButton, QVBoxLayout, QGridLayout, QInputDialog)

class MainWindow(QMainWindow):

    def __init__(self,application:QApplication):
        super().__init__()
        screen = application.desktop().screenGeometry()

        self.setGeometry(50, 50, screen.width(), screen.height())
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon('dragonShout.png'))

        self.library = ''
        self.loadLibrary()

        self.themesWidget = QWidget()
        self.playlistLabel = ''
        self.playlist = ''

        self.text = ''
        self.menuBar()
        self.changeLanguage()

        self.show()

    def setGUI(self):
        """Generates the main window user interface"""
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
        action.triggered.connect(lambda *args: self.library.save())

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

        #Splitter containing all other elements of MainWindow
        #----------------------------------------------------
        mainHorizontalSplitter = QSplitter()
        windowWidth = self.geometry().width()

        #Scene list
        # sceneVerticalSplitter = QSplitter(Qt.Qt.Vertical)
        # sceneLabel = QLabel(self.text.localisation('labels','scenes','caption'))
        # sceneLabel.setAlignment(Qt.Qt.AlignCenter)
        # sceneVerticalSplitter.addWidget(sceneLabel)
        #
        # sceneVerticalLayout = QVBoxLayout()
        # count = 1
        # while count <= 20 :
        #     testButton = QPushButton(self.text.localisation('buttons','scene','caption')+' '+str(count))
        #     testButton.setStatusTip(self.text.localisation('buttons','scene','toolTip'))
        #     sceneVerticalLayout.addWidget(testButton)
        #     count+=1
        #
        # genericWidget = QWidget()
        # genericWidget.setLayout(sceneVerticalLayout)
        # sceneVerticalSplitter.addWidget(genericWidget)
        # mainHorizontalSplitter.addWidget(sceneVerticalSplitter)

        #Theme selection and controls
        self.showThemes()
        mainHorizontalSplitter.addWidget(self.themesWidget)

        #Label of the currant playlist
        playlistVerticalSplitter = QSplitter(Qt.Qt.Vertical)

        self.playlistLabel = QLabel('Playlist label')
        self.playlistLabel.setAlignment(Qt.Qt.AlignCenter)
        playlistVerticalSplitter.addWidget(self.playlistLabel)

        #Playlist of the selected theme
        self.playlist = QListWidget()
        playlistVerticalSplitter.addWidget(self.playlist)

        #Controls of the playlist
        controlsWidget = QWidget(self)
        genericLayout = QHBoxLayout()
        playButton = QPushButton()
        stopButton = QPushButton()
        playButton.setIcon(QIcon('ressources/interface/play.png'))
        playButton.setMaximumWidth(40)
        stopButton.setIcon(QIcon('ressources/interface/stop.png'))
        stopButton.setMaximumWidth(40)
        genericLayout.addWidget(playButton)
        genericLayout.addWidget(stopButton)
        controlsWidget.setLayout(genericLayout)
        playlistVerticalSplitter.addWidget(controlsWidget)

        #Files on the computer
        fileBrowser = QFileDialog()
        musicPath = Qt.QDir.homePath()
        fileBrowser.setDirectory(musicPath)
        playlistVerticalSplitter.addWidget(fileBrowser)

        mainHorizontalSplitter.addWidget(playlistVerticalSplitter)

        genericLayout = QHBoxLayout()
        genericLayout.addWidget(mainHorizontalSplitter)
        centralWidget = QWidget(self)
        centralWidget.setLayout(genericLayout)

        self.setCentralWidget(centralWidget)

    def changeLanguage(self,language:str='english'):
        """Change the language of the application. Called by a signal emited when clicking on another language"""
        self.text = Text(language)
        self.setGUI()

    def loadLibrary(self,filepath:str=''):
        """Loads an existing library or creates a new one"""
        if os.path.isfile(filepath):
        	self.library = Library.load(filepath)
        else:
            self.library = Library("new_library","")

    def showThemes(self):
        """Gets the category objects in the library and arrange them as push buttons in the main window.
           Takes no parameters.
        """
        themesLayout = QGridLayout()
        for theme in self.library.categories:
            themeButton = QPushButton(theme.name)
            themeButton.clicked.connect(lambda *args: self.selectTheme(self.sender().text()))
            themesLayout.addWidget(themeButton)

        newThemeButton = QPushButton('+')
        newThemeButton.clicked.connect(lambda *args: self.addTheme())
        newThemeButton.setMaximumWidth(100)
        themesLayout.addWidget(newThemeButton)

        themesWidget = QWidget()
        themesWidget.setLayout(themesLayout)

        self.themesWidget = themesWidget

    def selectTheme(self,themeName:str):
        """Update the playlist with the music list of the selected theme
            Takes one parameter:
            - themeName as string
        """
        self.playlistLabel.setText(themeName)
        self.playlist.clear()
        theme = self.library.get_category(themeName)

        for track in theme.tracks :
            self.playlist.addItem(track.name)

    def addTheme(self):
        """Add a new theme to the application and open dialog box to set the theme name.
            Takes no parameter.
        """

        themeName, ok = QInputDialog.getText(self,self.text.localisation('dialogBoxes','newTheme','caption'),self.text.localisation('dialogBoxes','newTheme','question'))

        if ok :
            self.library.add_category(themeName)
            self.setGUI()

    def renameTheme(self,themeName:str):
        """Modify the name of the theme.
            Takes one parameter:
            - themeName as string
        """
        theme = self.library.get_category(themeName)
