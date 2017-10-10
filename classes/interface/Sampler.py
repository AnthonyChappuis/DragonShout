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

        self.sampleButtons = [[]]
        self.lastRowIndex = 0

        self.MAXBUTTONPERROW = 4

        self.mainLayout = QGridLayout()
        self.mainLayout.setAlignment(Qt.Qt.AlignHCenter)
        self.setLayout(self.mainLayout)

        self.addSampleButton()
        self.addSampleButton()
        self.addSampleButton()
        self.addSampleButton()
        self.addSampleButton()
        self.addSampleButton()
        self.addSampleButton()

        self.constructGrid()


    def constructGrid(self):
        """Constructs the buttons' grid according to the self.sampleButtons property
            - Takes no parameter.
            - Returns nothing
        """
        row = 0
        while row <= self.lastRowIndex:
            maxColumn = len(self.sampleButtons[row])
            column = 0
            while column < maxColumn:
                self.mainLayout.addWidget(self.sampleButtons[row][column],row,column)
                column += 1
            row += 1

    def addSampleButton(self):
        """Append a new QPushButton to self.sampleButtons.
            - Takes no parameter.
            - Returns nothing.
        """
        #Check if the last row is full according to self.MAXBUTTONPERROW.
        #It begins a new row if necessary
        if len(self.sampleButtons[self.lastRowIndex]) >= self.MAXBUTTONPERROW:
            self.sampleButtons.append([])
            self.lastRowIndex += 1

        self.sampleButtons[self.lastRowIndex].append(QPushButton())
