#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for main window of the application
#
#Application: DragonShout music sampler
#Last Edited: September 03 2018
#---------------------------------

import os
import traceback
import tarfile
from pathlib import Path

from classes.interface.Text import Text
from classes.interface.Playlist import Playlist
from classes.interface.Themes import Themes
from classes.interface.Sampler import Sampler
from classes.interface.SoundEffect import SoundEffect
from classes.ressourcesFilepath import Stylesheets, Images

from classes.library.Library import Library

from PyQt5 import Qt, QtGui
from PyQt5.QtCore import QFileInfo, QStandardPaths, QDir
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
    QHBoxLayout, QSplitter, QWidget, QListWidget, QLabel,
    QPushButton, QVBoxLayout, QGridLayout, QFileDialog, QMessageBox)

class MainWindow(QMainWindow):

    SUPPORTEDLIBRARYFILES = '*.json'
    APPLICATIONNAME = 'Dragon Shout'

    AppDataFolder = QStandardPaths.locate(QStandardPaths.AppDataLocation, '', QStandardPaths.LocateDirectory)+'DragonShout/'
    ArchiveThemesFolderName = 'themes'
    ArchiveSamplesFolderName = 'soundEffects'
    TempExtension = '.default'


    def __init__(self,application:QApplication):
        super().__init__()

        #App data directory
        if not QDir(MainWindow.AppDataFolder).exists():
            QDir().mkdir(MainWindow.AppDataFolder)

        #Global style sheet
        styleSheet = open(Stylesheets.globalStyle,'r', encoding='utf-8').read()
        self.setStyleSheet(styleSheet)

        #Window decoration
        self.setWindowTitle(MainWindow.APPLICATIONNAME)
        self.setWindowIcon(QIcon(Images.applicationIcon))

        #Variable and CONSTANTS
        self.text = Text(MainWindow.AppDataFolder)

        self.loadLibrary()

        self.sampler = Sampler(self)
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

        action = QAction(QIcon(Images.loadIcon), self.text.localisation('menuEntries','load','caption'), self)
        action.setShortcut('Ctrl+l')
        action.setStatusTip(self.text.localisation('menuEntries','load','toolTip'))
        action.triggered.connect(lambda *args: self.load())

        fileMenu.addAction(action)

        action = QAction(QIcon(Images.saveIcon), self.text.localisation('menuEntries','save','caption'), self)
        action.setShortcut('Ctrl+s')
        action.setStatusTip(self.text.localisation('menuEntries','save','toolTip'))
        action.triggered.connect(lambda *args: self.save())

        fileMenu.addAction(action)

        action = QAction(QIcon(Images.exportIcon), 'export', self)
        action.setShortcut('Ctrl+Alt+e')
        action.setStatusTip('Archive your library for easier transfert to another computer')
        action.triggered.connect(lambda * args: self.export())

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
        for languageKey, languageValues in self.text.SupportedLanguages.items():
            action = QAction(QIcon(languageValues['icon']), languageValues['caption'],self)
            action.triggered.connect(lambda *args: self.changeLanguage(self.sender().text()))
            languageMenu.addAction(action)

        #Splitter containing all other elements of MainWindow
        #----------------------------------------------------
        mainHorizontalSplitter = QSplitter()
        windowWidth = self.geometry().width()

        #Theme selection and controls
        mainHorizontalSplitter.addWidget(self.themes)

        #Playlist
        mainHorizontalSplitter.addWidget(self.playlist)

        #Sampler
        mainHorizontalSplitter.addWidget(self.sampler)

        #adding the splitter containing the main elements to the window
        genericLayout = QHBoxLayout()
        genericLayout.addWidget(mainHorizontalSplitter)
        centralWidget = QWidget(self)
        centralWidget.setLayout(genericLayout)

        self.setCentralWidget(centralWidget)

    def changeLanguage(self,language:str=Text.SupportedLanguages['English']['caption']):
        """Change the language of the application. Called by a signal emited when clicking on another language"""
        messageBox = QMessageBox(QMessageBox.Information,self.text.localisation('messageBoxes','saveLanguage','title'),self.text.localisation('messageBoxes','saveLanguage','caption'))
        messageBox.setWindowIcon(QIcon(Images.applicationIcon))
        messageBox.exec()
        self.text.saveLanguage(language)

    def loadLibrary(self,filepath:str=''):
        """Loads an existing library or creates a new one"""
        if os.path.isfile(filepath) and Library.load(self,filepath):
        	self.library = Library.load(self,filepath)
        elif os.path.isfile(filepath) and not Library.load(filepath):
            QMessageBox(QMessageBox.Warning,self.text.localisation('messageBoxes','loadLibrary','title'),self.text.localisation('messageBoxes','loadLibrary','caption')).exec()
        else:
            self.library = Library(self,"new_library","")

    def loadSampler(self,filepath:str=''):
        """Loads an existing sampleSet or creates a new one"""
        if os.path.isfile(filepath) and self.sampler.load(filepath,'test'):
        	self.sampler.load(filepath)
        elif os.path.isfile(filepath) and not Sampler.load(filepath):
            QMessageBox(QMessageBox.Warning,self.text.localisation('messageBoxes','loadLibrary','title'),self.text.localisation('messageBoxes','loadLibrary','caption')).exec()
        else:
            self.sampler = Sampler(self)

    def renameTheme(self,themeName:str):
        """Modify the name of the theme.
            Takes one parameter:
            - themeName as string
        """
        theme = self.library.get_category(themeName)

    def save(self):
        """Saves the current library.
            Takes no parameter.
            Returns nothing.
        """
        saveDialog = QFileDialog()
        saveDialog.setAcceptMode(QFileDialog.AcceptSave)
        userFolderPath = QStandardPaths.locate(QStandardPaths.HomeLocation, '', QStandardPaths.LocateDirectory)

        filepath , ok = saveDialog.getSaveFileName(self,self.text.localisation('dialogBoxes','saveLibrary','title'),os.path.expanduser(userFolderPath))

        if not filepath.endswith('.json') :
            filepath += '.json'

        if ok :
            libraryName = QFileInfo(filepath).fileName()
            self.library.name = libraryName
            self.library.save(filepath)

    def load(self):
        """Loads a new library.
            Takes no parameter.
            Returns nothing.
        """
        homeFolderPath = QStandardPaths.locate(QStandardPaths.HomeLocation, '', QStandardPaths.LocateDirectory)
        filepath, ok = QFileDialog().getOpenFileName(self,'test',os.path.expanduser(homeFolderPath),MainWindow.SUPPORTEDLIBRARYFILES)
        if ok :
            self.loadLibrary(filepath)
            self.loadSampler(filepath)
            self.themes.setThemes()
            self.playlist.reset()

    def export(self):
        """Used to export library and 'atttached' sound files as an archive that can be transfered to another computer and/or operating system. Use gzip compression module.
            Takes no parameter.
            Returns nothing.
        """

        try:
            archiveFilePath = Path(QStandardPaths.locate(QStandardPaths.DocumentsLocation, '', QStandardPaths.LocateDirectory)+'archive.dsm')
            #Create archive
            print('Export starts')
            archive = tarfile.open(archiveFilePath.resolve(),'x:gz')
            print('Archive created')

            #Archive the themes and their playlists
            #themes folder from category name
            for theme in self.library.categories:
                print('In theme: '+theme.name)
                subFolderName = theme.name

                #filling theme folder with given tracks
                for track in theme.tracks:
                    archive.add(track.location,MainWindow.ArchiveThemesFolderName+'/'+subFolderName+'/'+track.name)
                    print('File: '+track.location)

            #Archive the sound effects from the sampler
            for row in self.sampler.sampleButtons:
                for sampleButton in row :
                    buttonCoordinatesName = str(sampleButton.coordinates[0])+str(sampleButton.coordinates[1])
                    typeFolder = str(sampleButton.buttonType)

                    #user defined sound effects
                    if sampleButton.buttonType == SoundEffect.SOUNDEFFECTBUTTON :
                        sampleFilepath = Path(sampleButton.filepath)
                        endName = buttonCoordinatesName+sampleFilepath.name
                        archive.add(sampleFilepath.resolve(),MainWindow.ArchiveSamplesFolderName+'/'+typeFolder+'/'+endName)
                    #default buttons without effects
                    elif sampleButton.buttonType == SoundEffect.NEWEFFECTBUTTON :
                        endName = buttonCoordinatesName+MainWindow.TempExtension
                        defaultButtonTempPath = Path(MainWindow.AppDataFolder+endName)
                        defaultButtonTempPath.touch() #temp file to add to the archive
                        archive.add(defaultButtonTempPath.resolve(),MainWindow.ArchiveSamplesFolderName+'/'+typeFolder+'/'+endName)
                        defaultButtonTempPath.unlink() #remove the temp file
                    #Any other cases stops the export and triggers clean-up actions
                    else:
                        raise Exception
            aaaa.test()

            archive.close()
            print('Export successful')
        except FileExistsError:
            print('File exists!!')
        except Exception as e:
            print('An error occured, cleaning')
            #Clean archive
            archive.close()
            Path.unlink(archiveFilePath)

            #Clean temp files
            workFolder = Path(MainWindow.AppDataFolder)
            for child in workFolder.iterdir():
                print(child.name)
                if child.name.endswith(MainWindow.TempExtension):
                    child.unlink()

            print(traceback.format_exc())
