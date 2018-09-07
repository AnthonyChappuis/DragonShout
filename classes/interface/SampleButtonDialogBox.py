#---------------------------------
#Author: Chappuis Anthony
#
#Show a pop-up window to select sound and icon file for
# a sample button
#
#Application: DragonShout music sampler
#Last Edited: August 31th 2018
#---------------------------------

import os

from classes.interface import MainWindow
from classes.ressourcesFilepath import Stylesheets, Images
from classes.fileSupport import FileSupport

from PyQt5.QtWidgets import QDialog, QPushButton, QGridLayout, QLineEdit, QLabel, QFileDialog, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QFileInfo, QStandardPaths
from PyQt5.Qt import Qt

class SampleButtonDialogBox(QDialog):


    def __init__(self, mainWindow:MainWindow, samplePath:str='...', sampleIconPath:str='notset', colorSchemeStyleSheetPath:str='Default'):
        super().__init__()

        self.mainWindow = mainWindow
        self.okOrNot = False
        self.styleSheetPath = Stylesheets.effectButtons

        if colorSchemeStyleSheetPath == 'Default' :
            colorSchemeStyleSheetPath == Stylesheets.effectButtons

        styleSheet = open(Stylesheets.globalStyle,'r', encoding='utf-8').read()
        self.setStyleSheet(styleSheet)

        #parameters defaulting
        if sampleIconPath == 'notset' or not isinstance(sampleIconPath, str):
            sampleIconPath = Images.defaultButtonIcon

        #window title and icon
        self.setWindowIcon(QIcon(Images.applicationIcon))
        self.setWindowTitle(self.mainWindow.text.localisation('dialogBoxes','newSample','caption'))

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
        self.sampleIconButton.clicked.connect(lambda *args: self.getNewIcon())

        #Color scheme
        self.colorSchemeLabel = QLabel(self.mainWindow.text.localisation('labels','colorScheme','caption'))
        gridlayout = QGridLayout()
        self.colorSchemeWidget = QWidget()
        self.colorSchemeWidget.setLayout(gridlayout)
        self.colorSchemes = []
        colorNumber = 0

        for vert in range(2):
            for hor in range(3):
                if colorNumber == 1 :
                    styleSheetPath = Stylesheets.redEffectButtons
                elif colorNumber == 2 :
                    styleSheetPath = Stylesheets.yellowEffectButtons
                elif colorNumber == 3 :
                    styleSheetPath = Stylesheets.greyEffectButtons
                elif colorNumber == 4 :
                    styleSheetPath = Stylesheets.purpleEffectButtons
                elif colorNumber == 5 :
                    styleSheetPath = Stylesheets.blueEffectButtons
                else :
                    styleSheetPath = Stylesheets.effectButtons

                exampleButton = QPushButton()
                exampleButton.setStyleSheet(open(styleSheetPath,'r', encoding='utf-8').read())
                exampleButton.clicked.connect(lambda *args: self.toggleColorScheme(self.sender()))

                gridlayout.addWidget(exampleButton,vert,hor)
                self.colorSchemes.append((exampleButton,styleSheetPath))
                colorNumber += 1

                if styleSheetPath == colorSchemeStyleSheetPath :
                    exampleButton.click()

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
        self.layout.addWidget(self.colorSchemeLabel,2,0)
        self.layout.addWidget(self.colorSchemeWidget,2,1)
        self.layout.addWidget(self.OkButton,3,0)
        self.layout.addWidget(self.CancelButton,3,1)
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
        return self.samplePath, self.iconPath, self.styleSheetPath, self.okOrNot

    def getNewIcon(self):
        """Opens a filesystem dialog to choose a new icon file for the sample.
            Takes no parameter.
            Returns nothing.
        """
        picturesFolderPath = QStandardPaths.locate(QStandardPaths.PicturesLocation, '', QStandardPaths.LocateDirectory)

        filepath, ok = QFileDialog.getOpenFileName(self,self.mainWindow.text.localisation('dialogBoxes','newIcon','question'),os.path.expanduser(picturesFolderPath), FileSupport.pictures)

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
            filepath = QStandardPaths.locate(QStandardPaths.MusicLocation, '', QStandardPaths.LocateDirectory)

        filepath, ok = QFileDialog.getOpenFileName(self,self.mainWindow.text.localisation('dialogBoxes','newSample','question'),os.path.expanduser(filepath),FileSupport.audio)

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

    def toggleColorScheme(self, senderButton:QPushButton):
        """Used to select the color scheme when user is clicking on one of the color scheme buttonsself.
            - Takes one parameter:
                - senderButton as QPushButton.
            - Returns nothing.
        """
        filepath = Images.colorSchemeSelectorIcon
        for exampleButton in self.colorSchemes :
            exampleButton[0].setIcon(QIcon())
            #Store the styleSheetPath of the chosen button
            if exampleButton[0] == senderButton :
                self.styleSheetPath = exampleButton[1]

        senderButton.setIcon(QIcon(filepath))
