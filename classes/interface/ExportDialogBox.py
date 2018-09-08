#---------------------------------
#Author: Chappuis Anthony
#
#Pop-up window that manage export feature
#
#Application: DragonShout music sampler
#Last Edited: September 06th 2018
#---------------------------------
import os
import tarfile
import traceback
from pathlib import Path

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QTextEdit,
                            QProgressBar, QFileDialog)
from PyQt5.QtGui import QIcon, QGuiApplication
from PyQt5.QtCore import QStandardPaths, QCoreApplication

from classes.interface import MainWindow
from classes.interface.SoundEffect import SoundEffect
from classes.library.Track import Track

from classes.ressourcesFilepath import Stylesheets, Images

class ExportDialogBox(QDialog):

    ArchiveThemesFolderName = 'themes'
    ArchiveSamplesFolderName = 'soundEffects'
    TempExtension = '.default'
    ArchiveFileExtension = '.dsa'

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.archiveFilePath = Path(QStandardPaths.locate(QStandardPaths.HomeLocation, '', QStandardPaths.LocateDirectory))

        #Window dimensions
        vRatio = 1/2
        hRatio = 1/3
        screen = QGuiApplication.primaryScreen()
        screenGeometry = screen.geometry()
        self.setMinimumWidth(screenGeometry.width()*hRatio)
        self.setMinimumHeight(screenGeometry.height()*vRatio)

        #window title and icon
        self.setWindowIcon(QIcon(Images.applicationIcon))
        self.setWindowTitle(self.mainWindow.text.localisation('dialogBoxes','export','title'))

        styleSheet = open(Stylesheets.globalStyle,'r', encoding='utf-8').read()
        self.setStyleSheet(styleSheet)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        #File dialog
        layout = QHBoxLayout()
        fileDialogWidget = QWidget()
        fileDialogWidget.setLayout(layout)

        fileLabel = QLabel(self.mainWindow.text.localisation('labels','archiveFilePathLabel','caption'))
        layout.addWidget(fileLabel)

        self.archiveFileSelectButton = QPushButton('...')
        self.archiveFileSelectButton.clicked.connect(lambda *args: self.getNewFilePath())
        layout.addWidget(self.archiveFileSelectButton)

        #Progress Bar
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)

        #text edit
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        #export button
        self.exportButton = QPushButton('Export')
        self.exportButton.setEnabled(False)
        self.exportButton.clicked.connect(lambda *args: self.export())

        #close button
        self.closeButton = QPushButton('Close')
        self.closeButton.clicked.connect(lambda *args: self.close())

        #Main layout widgets
        self.mainLayout.addWidget(fileDialogWidget)
        self.mainLayout.addWidget(self.progressBar)
        self.mainLayout.addWidget(self.textEdit)
        self.mainLayout.addWidget(self.exportButton)
        self.mainLayout.addWidget(self.closeButton)

    def addLogEntry(self, entry:str):
        """Adds a line to the text edit with given text.
            Takes one parameter:
            - entry as string.
            Returns nothing.
        """
        self.textEdit.append(entry)

    def getNewFilePath(self):
        """Opens a filesystem dialog to choose a folder and filename for the archive.
            Takes no parameter.
            Returns nothing.
        """
        archiveFileDialog = QFileDialog()
        archiveFileDialog.setAcceptMode(QFileDialog.AcceptSave)

        rawFilepath, ok = archiveFileDialog.getSaveFileName(self,self.mainWindow.text.localisation('dialogBoxes','export','question'),os.path.expanduser(self.archiveFilePath),ExportDialogBox.ArchiveFileExtension)

        if ok :
            filepath = Path(rawFilepath)

            if filepath.suffix != ExportDialogBox.ArchiveFileExtension :
                filepath = filepath.with_suffix(ExportDialogBox.ArchiveFileExtension)

            self.archiveFilePath = filepath
            self.archiveFileSelectButton.setText(filepath.name)
            self.exportButton.setEnabled(True)

    def resetProgressBar(self):
        """Reset progress bar by gathering file number and setting it's min/max values and progress steps.
            Takes no parameter.
            Returns nothing.
        """
        trackNumber = 0
        effectNumber = 0

        for category in self.mainWindow.library.categories :
            trackNumber += len(category.tracks)

        effectNumber = self.mainWindow.sampler.countEffects()

        self.progressBar.reset()
        self.progressBar.setRange(0,trackNumber+effectNumber)
        self.progressBar.setValue(0)

    def bumpProgressBar(self):
        """Bump the value of the progress bar.
            Takes no parameter.
            Returns nothing.
        """
        self.progressBar.setValue(self.progressBar.value()+1)

    def toggleControls(self):
        """Enable or disable UI buttons during export.
            Takes no parameter.
            Returns nothing.
        """
        if self.closeButton.isEnabled() :
            self.closeButton.setEnabled(False)
        else:
            self.closeButton.setEnabled(True)

        if self.exportButton.isEnabled() :
            self.exportButton.setEnabled(False)
        else:
            self.exportButton.setEnabled(True)

        if self.archiveFileSelectButton.isEnabled() :
            self.archiveFileSelectButton.setEnabled(False)
        else:
            self.archiveFileSelectButton.setEnabled(True)

    def export(self):
        """Used to export library and 'atttached' sound files as an archive that can be transfered to another computer and/or operating system. Use gzip compression module.
            Takes no parameter.
            Returns nothing.
        """
        border1 = '****************************'
        border2 = '----------------------------'
        warningBorder = '!!!!!!!!!!!!!!!!!!!!!!'
        blankLine = ''

        self.textEdit.clear()
        self.resetProgressBar()
        self.toggleControls()

        try:
            archiveFilePath = self.archiveFilePath

            #Create archive
            archive = tarfile.open(archiveFilePath.resolve(),'x:gz')
            self.addLogEntry(self.mainWindow.text.localisation('logs','archiveCreation','caption')+archiveFilePath.name)
            self.addLogEntry(blankLine)

            self.addLogEntry(border1)
            self.addLogEntry(self.mainWindow.text.localisation('logs','exportStart','caption'))
            self.addLogEntry(border1)
            self.addLogEntry(blankLine)

            QCoreApplication.processEvents()

            #Archive the themes and their playlists
            #themes folder from category name

            self.addLogEntry(border2)
            self.addLogEntry(self.mainWindow.text.localisation('logs','playlist','caption'))
            self.addLogEntry(border2)
            self.addLogEntry(blankLine)

            for theme in self.mainWindow.library.categories:
                self.addLogEntry(self.mainWindow.text.localisation('logs','inTheme','caption')+theme.name)
                self.addLogEntry(border2)
                self.addLogEntry(blankLine)
                subFolderName = theme.name

                #filling theme folder with given tracks
                for track in theme.tracks:
                    archive.add(track.location,ExportDialogBox.ArchiveThemesFolderName+'/'+subFolderName+'/'+track.name)
                    self.addLogEntry(self.mainWindow.text.localisation('logs','file','caption')+track.location)
                    self.bumpProgressBar()
                    QCoreApplication.processEvents()

                self.addLogEntry(blankLine)

            self.addLogEntry(border2)
            self.addLogEntry(self.mainWindow.text.localisation('logs','sampler','caption'))
            self.addLogEntry(border2)
            self.addLogEntry(blankLine)

            #Archive the sound effects from the sampler
            for row in self.mainWindow.sampler.sampleButtons:
                for sampleButton in row :
                    buttonCoordinatesID = str(sampleButton.coordinates[0])+str(sampleButton.coordinates[1])
                    typeFolder = str(sampleButton.buttonType)

                    #user defined sound effects
                    if sampleButton.buttonType == SoundEffect.SOUNDEFFECTBUTTON :

                        if sampleButton.styleSheetPath == Stylesheets.effectButtons:
                            colorID = 'U'
                        elif sampleButton.styleSheetPath == Stylesheets.redEffectButtons:
                            colorID = 'R'
                        elif sampleButton.styleSheetPath == Stylesheets.yellowEffectButtons:
                            colorID = 'Y'
                        elif sampleButton.styleSheetPath == Stylesheets.greyEffectButtons:
                            colorID = 'G'
                        elif sampleButton.styleSheetPath == Stylesheets.purpleEffectButtons:
                            colorID = 'P'
                        elif sampleButton.styleSheetPath == Stylesheets.blueEffectButtons:
                            colorID = 'B'
                        else:
                            colorID = 'U'

                        sampleFilepath = Path(sampleButton.filepath)
                        endName = buttonCoordinatesID+colorID+sampleFilepath.name
                        self.addLogEntry(self.mainWindow.text.localisation('logs','file','caption')+str(sampleFilepath.resolve()))
                        archive.add(sampleFilepath.resolve(),ExportDialogBox.ArchiveSamplesFolderName+'/'+typeFolder+'/'+endName)
                    #default buttons without effects
                    elif sampleButton.buttonType == SoundEffect.NEWEFFECTBUTTON :
                        endName = buttonCoordinatesID+ExportDialogBox.TempExtension
                        defaultButtonTempPath = Path(MainWindow.MainWindow.AppDataFolder+endName)
                        defaultButtonTempPath.touch() #temp file to add to the archive
                        archive.add(defaultButtonTempPath.resolve(),ExportDialogBox.ArchiveSamplesFolderName+'/'+typeFolder+'/'+endName)
                        defaultButtonTempPath.unlink() #remove the temp file
                    #Any other cases stops the export and triggers clean-up actions
                    else:
                        raise Exception

                    self.bumpProgressBar()

            self.addLogEntry(blankLine)

            archive.close()

            self.addLogEntry(border1)
            self.addLogEntry(self.mainWindow.text.localisation('logs','exportSuccess','caption'))
            self.addLogEntry(border1)
            QCoreApplication.processEvents()

        except FileExistsError:
            self.addLogEntry(warningBorder)
            self.addLogEntry(self.mainWindow.text.localisation('logs','fileExists','caption'))
            self.addLogEntry(warningBorder)
            QCoreApplication.processEvents()

        except Exception as e:
            self.addLogEntry(warningBorder)
            self.addLogEntry(self.mainWindow.text.localisation('logs','error','caption'))
            self.addLogEntry(warningBorder)
            self.addLogEntry(blankLine)
            QCoreApplication.processEvents()

            #Clean archive
            if 'archive' in locals():
                archive.close()
                Path.unlink(archiveFilePath)

            #Clean temp files
            workFolder = Path(MainWindow.MainWindow.AppDataFolder)
            for child in workFolder.iterdir():
                print(child.name)
                if child.name.endswith(ExportDialogBox.TempExtension):
                    child.unlink()

            self.addLogEntry(traceback.format_exc())

        self.toggleControls()
