#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for main window of the application
#
#Application: DragonShout music sampler
#Last Edited: April 16th 2017
#---------------------------------

from constants import *

import os

from classes.interface.Text import Text
from classes.interface.Playlist import Playlist
from classes.interface.Themes import Themes

from classes.library.Library import Library

from PyQt5 import Qt, QtGui
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
    QHBoxLayout, QSplitter, QWidget, QListWidget, QLabel,
    QPushButton, QVBoxLayout, QGridLayout, QFileDialog, QMessageBox)

class MainWindow(QMainWindow):
    SupportedLibraryFiles = '*.json'

    def __init__(self,application:QApplication):
        super().__init__()
        screen = application.desktop().screenGeometry()

        self.setGeometry(50, 50, screen.width(), screen.height())
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon('dragonShout.png'))

        self.text = Text()

        self.library = ''
        self.loadLibrary()

        self.themes = Themes(self)
        self.playlist = Playlist(self)

        self.menuBar()

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

        action = QAction(QIcon('load.png'), self.text.localisation('menuEntries','load','caption'), self)
        action.setShortcut('Ctrl+l')
        action.setStatusTip(self.text.localisation('menuEntries','load','toolTip'))
        action.triggered.connect(lambda *args: self.load())

        fileMenu.addAction(action)

        action = QAction(QIcon('save.png'), self.text.localisation('menuEntries','save','caption'), self)
        action.setShortcut('Ctrl+s')
        action.setStatusTip(self.text.localisation('menuEntries','save','toolTip'))
        action.triggered.connect(lambda *args: self.save())

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
        action.triggered.connect(lambda *args: self.changeLanguage(Text.SupportedLanguages['English']))
        languageMenu.addAction(action)
        action = QAction(QIcon('ressources/interface/France.png'), 'Français',self)
        action.triggered.connect(lambda *args: self.changeLanguage(Text.SupportedLanguages['French']))
        languageMenu.addAction(action)

        #Splitter containing all other elements of MainWindow
        #----------------------------------------------------
        mainHorizontalSplitter = QSplitter()
        windowWidth = self.geometry().width()

        #Theme selection and controls
        mainHorizontalSplitter.addWidget(self.themes)

        #Playlist
        mainHorizontalSplitter.addWidget(self.playlist)

        #adding the splitter containing the main elements to the window
        genericLayout = QHBoxLayout()
        genericLayout.addWidget(mainHorizontalSplitter)
        centralWidget = QWidget(self)
        centralWidget.setLayout(genericLayout)

        self.setCentralWidget(centralWidget)

    def changeLanguage(self,language:str=Text.SupportedLanguages['English']):
        """Change the language of the application. Called by a signal emited when clicking on another language"""
        self.text.saveLanguage(language)

    def loadLibrary(self,filepath:str=''):
        """Loads an existing library or creates a new one"""
        if os.path.isfile(filepath) and Library.load(filepath):
        	self.library = Library.load(filepath)
        elif os.path.isfile(filepath) and not Library.load(filepath):
            QMessageBox(QMessageBox.Warning,self.text.localisation('messageBoxes','loadLibrary','title'),self.text.localisation('messageBoxes','loadLibrary','caption')).exec()
        else:
            self.library = Library("new_library","")

    def renameTheme(self,themeName:str):
        """Modify the name of the theme.
            Takes one parameter:
            - themeName as string
        """
        theme = self.library.get_category(themeName)

    def save(self):
        """Save the current library.
            Takes no parameter.
        """
        saveDialog = QFileDialog()
        saveDialog.setAcceptMode(QFileDialog.AcceptSave)

        filepath , ok = saveDialog.getSaveFileName(self,self.text.localisation('dialogBoxes','saveLibrary','title'),os.path.expanduser('~'))

        if not filepath.endswith('.json') :
            filepath += '.json'

        if ok :
            libraryName = QFileInfo(filepath).fileName()
            self.library.name = libraryName
            self.library.save(filepath)

    def load(self):
        loadDialog = QFileDialog()

        filepath, ok = loadDialog.getOpenFileName(self,'test',os.path.expanduser('~'),MainWindow.SupportedLibraryFiles)

        if ok :
            self.loadLibrary(filepath)
            self.themes.setThemes()
            self.playlist.reset()
