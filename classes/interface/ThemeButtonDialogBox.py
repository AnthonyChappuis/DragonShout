#---------------------------------
#Author: Chappuis Anthony
#
#Handle the dialogbox used when adding a new theme button to the application
#
#Application: DragonShout music sampler
#Last Edited: Mai 07th 2017
#---------------------------------

from classes.interface import MainWindow

from PyQt5.QtWidgets import QDialog

class ThemeButtonDialogBox(QDialog):

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
