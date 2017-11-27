#---------------------------------
#Author: Chappuis Anthony
#
#Show a pop-up window to select sound and icon file for
# a sample button
#
#Application: DragonShout music sampler
#Last Edited: October 25th 2017
#---------------------------------

import os

from classes.interface import MainWindow

from PyQt5.QtWidgets import QDialog, QPushButton, QGridLayout, QLineEdit, QLabel, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QFileInfo
from PyQt5.Qt import Qt

class SampleButtonDialogBox(QDialog):

    DefaultSampleIconPath = 'ressources/interface/defaultButtonIcon.png'

    def __init__(self, mainWindow:MainWindow, samplePath:str='...', sampleIconPath:str='notset'):
        super().__init__()

        self.mainWindow = mainWindow
        self.okOrNot = False

        #parameters defaulting
        if sampleIconPath == 'notset' or not isinstance(sampleIconPath, str):
            sampleIconPath = SampleButtonDialogBox.DefaultSampleIconPath

        #window title and icon
        self.setWindowIcon(QIcon(MainWindow.MainWindow.ApplicationIconPath))
        self.setWindowTitle(self.mainWindow.text.localisation('dialogBoxes','newTheme','caption'))

        #sample filepath
        self.samplePath = samplePath
        self.sampleFileSelectLabel = QLabel(self.mainWindow.text.localisation('dialogBoxes','newSample','question'))

        self.sampleFileSelectButton = QPushButton(QFileInfo(samplePath).fileName())
        self.sampleFileSelectButton.clicked.connect(lambda *args: self.getNewFilePath())

        #icon
        self.sampleIconButtonLabel = QLabel(self.mainWindow.text.localisation('dialogBoxes','newIcon','question'))
        self.iconPath = sampleIconPath

        self.sampleIconButton = QPushButton()
        self.sampleIconButton.setIcon(QIcon(self.iconPath))
        self.sampleIconButton.setIconSize(QSize(100,100))
        self.sampleIconButton.setFlat(True)
        self.sampleIconButton.clicked.connect(lambda *args: self.getNewIcon())

        #control buttons
        self.OkButton = QPushButton(self.mainWindow.text.localisation('buttons','ok','caption'))
        self.OkButton.clicked.connect(lambda *args: self.closeDialog(True))

        self.CancelButton = QPushButton(self.mainWindow.text.localisation('buttons','cancel','caption'))
        self.CancelButton.clicked.connect(lambda *args: self.closeDialog(False))

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.sampleFileSelectLabel,0,0)
        self.layout.addWidget(self.sampleFileSelectButton,0,1)
        self.layout.addWidget(self.sampleIconButtonLabel,1,0)
        self.layout.addWidget(self.sampleIconButton,1,1)
        self.layout.addWidget(self.OkButton,2,0)
        self.layout.addWidget(self.CancelButton,2,1)
        self.setLayout(self.layout)

    def getItems(self):
        """Opens the theme button dialog box locking the window and await for user inputs.
            Takes no parameter.
            Returns:
            - samplePath as string.
            - iconPath as string.
            - okOrNot as boolean.
        """
        self.exec()
        return self.samplePath, self.iconPath, self.okOrNot

    def getNewIcon(self):
        """Opens a filesystem dialog to choose a new icon file for the sample.
            Takes no parameter.
            Returns nothing.
        """
        if os.path.isfile(self.iconPath):
            filepath = self.iconPath
        else:
            filepath = '~/Pictures'

        filepath, ok = QFileDialog.getOpenFileName(self,self.mainWindow.text.localisation('dialogBoxes','newIcon','question'),os.path.expanduser(filepath),"*.jpg *.jpeg *.ico *.png")

        if ok :
            self.sampleIconButton.setIcon(QIcon(filepath))
            self.iconPath = filepath

    def getNewFilePath(self):
        """Opens a filesystem dialog to choose a new effect file for the sample.
            Takes no parameter.
            Returns nothing.
        """
        if os.path.isfile(self.samplePath):
            filepath = self.samplePath
        else:
            filepath = '~/Music'

        filepath, ok = QFileDialog.getOpenFileName(self,self.mainWindow.text.localisation('dialogBoxes','newSample','question'),os.path.expanduser(filepath),"*.mp3 *.wav *.flac *.aac")

        if ok :
            self.samplePath = filepath
            self.sampleFileSelectButton.setText(QFileInfo(filepath).fileName())

    def closeDialog(self, okOrNot:bool):
        """Close the dialog.
            Takes one parameter:
            - okOrNot as boolean.
            Returns nothing.
        """
        self.okOrNot = okOrNot
        self.close()
