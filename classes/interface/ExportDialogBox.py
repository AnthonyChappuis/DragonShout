#---------------------------------
#Author: Chappuis Anthony
#
#Pop-up window that manage export feature
#
#Application: DragonShout music sampler
#Last Edited: September 06th 2018
#---------------------------------

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QTextEdit,
                            QProgressBar)
from PyQt5.QtGui import QIcon

from classes.interface import MainWindow

from classes.ressourcesFilepath import Stylesheets, Images

class ExportDialogBox(QDialog):
    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.okOrNot = False
        self.number = 0

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

        fileButton = QPushButton('...')
        layout.addWidget(fileButton)

        #Progress Bar
        self.progressBar = QProgressBar()

        #text edit
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        #Main layout widgets
        self.mainLayout.addWidget(fileDialogWidget)
        self.mainLayout.addWidget(self.progressBar)
        self.mainLayout.addWidget(self.textEdit)

    def getItems(self):
        """Opens the Export dialog box locking the window and await for user inputs.
            Takes no parameter.
            Returns:
            - okOrNot as boolean.
        """
        self.exec()
        return self.okOrNot

    def addLogEntry(self, entry:str):
        """Adds a line to the text edit with given text.
            Takes one parameter:
            - entry as string.
            Returns nothing.
        """
        self.textEdit.append(entry)
