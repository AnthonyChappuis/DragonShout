#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for main window of the application
#
#Application: DragonShout music sampler
#Last Edited: February 16th 2017
#---------------------------------

from constants import *
from classes.interface.Text import Text

import os
from classes.library.Library import Library
from classes.interface.Playlist import Playlist

from PyQt5 import Qt, QtGui, QtCore
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
    QHBoxLayout, QSplitter, QWidget, QListWidget, QLabel,
    QPushButton, QVBoxLayout, QGridLayout, QInputDialog)

class MainWindow(QMainWindow):

    def __init__(self,application:QApplication):
        super().__init__()
        screen = application.desktop().screenGeometry()

        self.setGeometry(50, 50, screen.width(), screen.height())
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon('dragonShout.png'))

        self.text = ''

        self.library = ''
        self.loadLibrary()

        self.themesLayout = QVBoxLayout()
        self.themesLayout.setAlignment(Qt.Qt.AlignHCenter)
        self.themesWidget = QWidget()
        self.themesWidget.setLayout(self.themesLayout)

        self.playlist = ''

        self.menuBar()
        self.changeLanguage()

        self.setGUI()

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
        self.setThemes()
        mainHorizontalSplitter.addWidget(self.themesWidget)

        #Playlist
        self.playlist = Playlist(self.text)
        mainHorizontalSplitter.addWidget(self.playlist)

        #adding the splitter containing the main elements to the window
        genericLayout = QHBoxLayout()
        genericLayout.addWidget(mainHorizontalSplitter)
        centralWidget = QWidget(self)
        centralWidget.setLayout(genericLayout)

        self.setCentralWidget(centralWidget)

    def changeLanguage(self,language:str='english'):
        """Change the language of the application. Called by a signal emited when clicking on another language"""
        self.text = Text(language)

    def loadLibrary(self,filepath:str=''):
        """Loads an existing library or creates a new one"""
        if os.path.isfile(filepath):
        	self.library = Library.load(filepath)
        else:
            self.library = Library("new_library","")

    def setThemes(self):
        """Gets the category objects in the library and arrange them as push buttons in the main window.
           Takes no parameters.
        """
        newThemeButton = QPushButton('+')
        newThemeButton.clicked.connect(lambda *args: self.addTheme())
        newThemeButton.setMaximumWidth(100)
        self.themesLayout.addWidget(newThemeButton)

        for theme in self.library.categories:
            self.addThemeButtonToThemeLayout(theme.name)


    def selectTheme(self,themeName:str):
        """Update the playlist with the music list of the selected theme
            Takes one parameter:
            - themeName as string
        """
        theme = self.library.get_category(themeName)
        if theme :
            self.playlist.setList(themeName,theme.tracks)

    def addTheme(self):
        """Add a new theme to the application and open dialog box to set the theme name.
            Takes no parameter.
        """
        themeName, ok = QInputDialog.getText(self,self.text.localisation('dialogBoxes','newTheme','caption'),self.text.localisation('dialogBoxes','newTheme','question'))

        if ok :
            self.library.add_category(themeName)
            self.addThemeButtonToThemeLayout(themeName)

    def addThemeButtonToThemeLayout(self,buttonText:str=''):
        """Adds a new theme button to the theme layout.
            Takes one parameter:
            - button text as string.
        """
        if buttonText == '' :
            buttonText = self.text.localisation('buttons','newTheme','caption')

        themeButton = QPushButton(buttonText)
        themeButton.setMaximumWidth(100)
        themeButton.clicked.connect(lambda *args: self.selectTheme(self.sender().text()))
        self.themesLayout.addWidget(themeButton)

    def renameTheme(self,themeName:str):
        """Modify the name of the theme.
            Takes one parameter:
            - themeName as string
        """
        theme = self.library.get_category(themeName)
