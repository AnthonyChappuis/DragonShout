#---------------------------------
#Author: Chappuis Anthony
#
#Pop-up window that manage import feature
#
#Application: DragonShout music sampler
#Last Edited: September 25th 2018
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
from classes.interface.ExportDialogBox import ExportDialogBox

from classes.ressourcesFilepath import Stylesheets, Images

class ImportDialogBox(QDialog):

    ArchiveType = 0
    DestinationType = 1

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.archiveFilePath = Path(QStandardPaths.locate(QStandardPaths.HomeLocation, '', QStandardPaths.LocateDirectory))
        self.destinationPath = self.archiveFilePath

        #Window dimensions
        vRatio = 1/2
        hRatio = 1/3
        screen = QGuiApplication.primaryScreen()
        screenGeometry = screen.geometry()
        self.setMinimumWidth(screenGeometry.width()*hRatio)
        self.setMinimumHeight(screenGeometry.height()*vRatio)

        #window title and icon
        self.setWindowIcon(QIcon(Images.applicationIcon))
        self.setWindowTitle(self.mainWindow.text.localisation('dialogBoxes','import','title'))

        styleSheet = open(Stylesheets.globalStyle,'r', encoding='utf-8').read()
        self.setStyleSheet(styleSheet)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        #Archive file dialog
        layout = QHBoxLayout()
        archiveFileDialogWidget = QWidget()
        archiveFileDialogWidget.setLayout(layout)

        fileLabel = QLabel(self.mainWindow.text.localisation('labels','archiveFilePathLabel','caption'))
        layout.addWidget(fileLabel)

        self.archiveFileSelectButton = QPushButton('...')
        self.archiveFileSelectButton.clicked.connect(lambda *args: self.getNewPath(ImportDialogBox.ArchiveType))
        layout.addWidget(self.archiveFileSelectButton)

        #Destination filedialog
        layout = QHBoxLayout()
        destinationDialogWidget = QWidget()
        destinationDialogWidget.setLayout(layout)

        fileLabel = QLabel('Destination')
        layout.addWidget(fileLabel)

        self.destinationSelectButton = QPushButton('...')
        self.destinationSelectButton.clicked.connect(lambda *args: self.getNewPath(ImportDialogBox.DestinationType))
        layout.addWidget(self.destinationSelectButton)

        #Progress Bar
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)

        #text edit
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        #Import button
        self.importButton = QPushButton(self.mainWindow.text.localisation('buttons','import','caption'))
        self.importButton.setEnabled(False)
        self.importButton.clicked.connect(lambda *args: self.importArchive())

        #Close button
        self.closeButton = QPushButton(self.mainWindow.text.localisation('buttons','close','caption'))
        self.closeButton.clicked.connect(lambda *args: self.close())

        #Main layout widgets
        self.mainLayout.addWidget(archiveFileDialogWidget)
        self.mainLayout.addWidget(destinationDialogWidget)
        self.mainLayout.addWidget(self.progressBar)
        self.mainLayout.addWidget(self.textEdit)
        self.mainLayout.addWidget(self.importButton)
        self.mainLayout.addWidget(self.closeButton)

    def getNewPath(self, fileType:int):
        """Opens a filesystem dialog to choose a filepath for the archive or destination.
            Takes one parameter:
            - fileType as either ImportDialogBox.ArchiveType or ImportDialogBox.DestinationType.
            Returns nothing.
        """
        archiveFileDialog = QFileDialog()

        if fileType == ImportDialogBox.ArchiveType:
            rawFilepath, ok = archiveFileDialog.getOpenFileName(self,self.mainWindow.text.localisation('dialogBoxes','export','question'),os.path.expanduser(self.archiveFilePath))

            if ok :
                filepath = Path(rawFilepath)
                self.archiveFilePath = filepath
                self.archiveFileSelectButton.setText(filepath.name)

        elif fileType == ImportDialogBox.DestinationType:
            rawFilepath = archiveFileDialog.getExistingDirectory(self,self.mainWindow.text.localisation('dialogBoxes','export','question'),os.path.expanduser(self.archiveFilePath))

            if rawFilepath :
                filepath = Path(rawFilepath)
                self.destinationPath = filepath
                self.destinationSelectButton.setText(filepath.name)

        self.checkReady()

    def checkReady(self):
        """Checks if both archive and destination are selected before enabling import button.
            Takes no parameter.
            Returns nothing.
        """
        archiveReady = False
        destinationReady = False

        if self.archiveFilePath.exists() and self.archiveFilePath.suffix == ExportDialogBox.ArchiveFileExtension:
            archiveReady = True

        if self.destinationPath.exists():
            destinationReady = True

        if archiveReady and destinationReady :
            self.importButton.setEnabled(True)
        else:
            self.importButton.setEnabled(False)

    def importArchive(self):
        print('Import')
