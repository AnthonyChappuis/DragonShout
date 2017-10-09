#---------------------------------
#Author: Chappuis Anthony
#
#This class manage the buttons of the sampler function.
#
#Application: DragonShout music sampler
#Last Edited: October 09th 2017
#---------------------------------

from classes.interface import MainWindow

from PyQt5 import Qt

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton

class Sampler(QWidget):

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow

        self.sampleButtons = []

        self.mainLayout = QGridLayout()
        self.mainLayout.setAlignment(Qt.Qt.AlignHCenter)
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(QPushButton())
