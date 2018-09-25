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

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon

from classes.interface import MainWindow
from classes.interface.ExportDialogBox import ExportDialogBox

from classes.ressourcesFilepath import Stylesheets, Images

class ImportDialogBox(QDialog):

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow

        #window title and icon
        self.setWindowIcon(QIcon(Images.applicationIcon))
        self.setWindowTitle(self.mainWindow.text.localisation('dialogBoxes','import','title'))

        styleSheet = open(Stylesheets.globalStyle,'r', encoding='utf-8').read()
        self.setStyleSheet(styleSheet)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        #close button
        self.closeButton = QPushButton(self.mainWindow.text.localisation('buttons','close','caption'))
        self.closeButton.clicked.connect(lambda *args: self.close())

        #Main layout widgets
        self.mainLayout.addWidget(self.closeButton)
