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
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QStandardPaths, QCoreApplication

from classes.interface import MainWindow
from classes.interface.SoundEffect import SoundEffect

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

        fileLabel = QLabel('File select: ')
        layout.addWidget(fileLabel)

        self.archiveFileSelectButton = QPushButton('...')
        self.archiveFileSelectButton.clicked.connect(lambda *args: self.getNewFilePath())
        layout.addWidget(self.archiveFileSelectButton)

        #Progress Bar
        self.progressBar = QProgressBar()

        #text edit
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        #export button
        self.exportButton = QPushButton('Export')
        self.exportButton.setEnabled(False)
        self.exportButton.clicked.connect(lambda *args: self.export())

        #close button
        closeButton = QPushButton('Close')
        closeButton.clicked.connect(lambda *args: self.close())

        #Main layout widgets
        self.mainLayout.addWidget(fileDialogWidget)
        self.mainLayout.addWidget(self.progressBar)
        self.mainLayout.addWidget(self.textEdit)
        self.mainLayout.addWidget(self.exportButton)
        self.mainLayout.addWidget(closeButton)

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

    def export(self):
        """Used to export library and 'atttached' sound files as an archive that can be transfered to another computer and/or operating system. Use gzip compression module.
            Takes no parameter.
            Returns nothing.
        """
        border1 = '****************************'
        border2 = '----------------------------'
        blankLine = ''

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
                    QCoreApplication.processEvents()

                self.addLogEntry(blankLine)

            self.addLogEntry(border2)
            self.addLogEntry(self.mainWindow.text.localisation('logs','sampler','caption'))
            self.addLogEntry(border2)
            self.addLogEntry(blankLine)

            #Archive the sound effects from the sampler
            for row in self.mainWindow.sampler.sampleButtons:
                for sampleButton in row :
                    buttonCoordinatesName = str(sampleButton.coordinates[0])+str(sampleButton.coordinates[1])
                    typeFolder = str(sampleButton.buttonType)

                    #user defined sound effects
                    if sampleButton.buttonType == SoundEffect.SOUNDEFFECTBUTTON :
                        sampleFilepath = Path(sampleButton.filepath)
                        endName = buttonCoordinatesName+sampleFilepath.name
                        self.addLogEntry(self.mainWindow.text.localisation('logs','file','caption')+str(sampleFilepath.resolve()))
                        archive.add(sampleFilepath.resolve(),ExportDialogBox.ArchiveSamplesFolderName+'/'+typeFolder+'/'+endName)
                    #default buttons without effects
                    elif sampleButton.buttonType == SoundEffect.NEWEFFECTBUTTON :
                        endName = buttonCoordinatesName+ExportDialogBox.TempExtension
                        defaultButtonTempPath = Path(MainWindow.MainWindow.AppDataFolder+endName)
                        defaultButtonTempPath.touch() #temp file to add to the archive
                        archive.add(defaultButtonTempPath.resolve(),ExportDialogBox.ArchiveSamplesFolderName+'/'+typeFolder+'/'+endName)
                        defaultButtonTempPath.unlink() #remove the temp file
                    #Any other cases stops the export and triggers clean-up actions
                    else:
                        raise Exception

            self.addLogEntry(blankLine)

            archive.close()
            self.addLogEntry(border1)
            self.addLogEntry(self.mainWindow.text.localisation('logs','exportSuccess','caption'))
            self.addLogEntry(border1)
            QCoreApplication.processEvents()

        except FileExistsError:
            self.addLogEntry(border2)
            self.addLogEntry(self.mainWindow.text.localisation('logs','fileExists','caption'))
            self.addLogEntry(border2)
            QCoreApplication.processEvents()

        except Exception as e:
            self.addLogEntry(border2)
            self.addLogEntry(self.mainWindow.text.localisation('logs','error','caption'))
            self.addLogEntry(border2)
            self.addLogEntry(blankLine)
            QCoreApplication.processEvents()

            #Clean archive
            archive.close()
            Path.unlink(archiveFilePath)

            #Clean temp files
            workFolder = Path(MainWindow.MainWindow.AppDataFolder)
            for child in workFolder.iterdir():
                print(child.name)
                if child.name.endswith(ExportDialogBox.TempExtension):
                    child.unlink()

            self.addLogEntry(traceback.format_exc())
