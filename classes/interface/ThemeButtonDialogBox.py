#---------------------------------
#Author: Chappuis Anthony
#
#Handle the dialogbox used when adding a new theme button to the application
#
#Application: DragonShout music sampler
#Last Edited: July 26th 2018b
#---------------------------------

import os

from classes.interface import MainWindow
from classes.ressourcesFilepath import Stylesheets, Images

from PyQt5.QtWidgets import QDialog, QPushButton, QGridLayout, QLineEdit, QLabel, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QStandardPaths
from PyQt5.Qt import Qt

class ThemeButtonDialogBox(QDialog):

    def __init__(self, mainWindow:MainWindow, themeName:str='notset', themeIconPath:str='notset'):
        super().__init__()

        self.mainWindow = mainWindow
        self.okOrNot = False

        styleSheet = open(Stylesheets.globalStyle,'r', encoding='utf-8').read()
        self.setStyleSheet(styleSheet)

        #parameters defaulting
        if themeName == 'notset' or not isinstance(themeName, str):
            themeName = self.mainWindow.text.localisation('dialogBoxes','newTheme','caption')

        if themeIconPath == 'notset' or not isinstance(themeIconPath, str):
            themeIconPath = Images.defaultButtonIcon

        #window title and icon
        self.setWindowIcon(QIcon(MainWindow.MainWindow.APPLICATIONICONPATH))
        self.setWindowTitle(self.mainWindow.text.localisation('dialogBoxes','newTheme','caption'))

        #Theme name
        self.themeNameLabel = QLabel(self.mainWindow.text.localisation('dialogBoxes','newTheme','question'))
        self.themeName = QLineEdit(themeName)

        #icon
        self.themeIconButtonLabel = QLabel(self.mainWindow.text.localisation('dialogBoxes','newIcon','question'))
        self.iconPath = themeIconPath

        self.themeIconButton = QPushButton()
        self.themeIconButton.setIcon(QIcon(self.iconPath))
        self.themeIconButton.setIconSize(QSize(100,100))
        self.themeIconButton.setFlat(True)
        self.themeIconButton.clicked.connect(lambda *args: self.getNewIcon())

        #control buttons
        self.OkButton = QPushButton(self.mainWindow.text.localisation('buttons','ok','caption'))
        self.OkButton.clicked.connect(lambda *args: self.closeDialog(True))

        self.CancelButton = QPushButton(self.mainWindow.text.localisation('buttons','cancel','caption'))
        self.CancelButton.clicked.connect(lambda *args: self.closeDialog(False))

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.themeNameLabel,0,0)
        self.layout.addWidget(self.themeName,0,1)
        self.layout.addWidget(self.themeIconButtonLabel,1,0)
        self.layout.addWidget(self.themeIconButton,1,1)
        self.layout.addWidget(self.OkButton,2,0)
        self.layout.addWidget(self.CancelButton,2,1)
        self.setLayout(self.layout)

    def getItems(self):
        """Opens the theme button dialog box locking the window and await for user inputs.
            Takes no parameter.
            Returns:
            - themeName as string.
            - iconPath as string.
            - okOrNot as boolean.
        """
        self.exec()
        return self.themeName.text(), self.iconPath, self.okOrNot

    def getNewIcon(self):
        """Opens a filesystem dialog to choose a new icon file for the theme.
            Takes no parameter.
            Returns nothing.
        """

        picturesFolderPath = QStandardPaths.locate(QStandardPaths.PicturesLocation, '', QStandardPaths.LocateDirectory)

        filepath, ok = QFileDialog.getOpenFileName(self,self.mainWindow.text.localisation('dialogBoxes','newIcon','question'),os.path.expanduser(picturesFolderPath),"*.jpg *.jpeg *.ico *.png")

        if ok :
            self.themeIconButton.setIcon(QIcon(filepath))
            self.iconPath = filepath

    def closeDialog(self, okOrNot:bool):
        """Close the dialog.
            Takes one parameter:
            - okOrNot as boolean.
            Returns nothing.
        """
        self.okOrNot = okOrNot
        self.close()
