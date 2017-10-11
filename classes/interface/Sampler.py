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

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout

class Sampler(QWidget):

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow

        self.sampleButtons = [[]]
        self.lastRowIndex = 0

        self.MAXBUTTONPERROW = 4

        #Main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.Qt.AlignHCenter)
        self.setLayout(self.mainLayout)

        #New sample button
        self.addNewSampleButton()

        self.addSampleButton()
        self.addSampleButton()
        self.addSampleButton()
        self.addSampleButton()
        self.addSampleButton()
        self.addSampleButton()

        #Sample buttons grid layout
        self.constructGrid()

        self.mainLayout.addStretch(1)

    def constructGrid(self):
        """Constructs the buttons' grid according to the self.sampleButtons property
            - Takes no parameter.
            - Returns nothing
        """
        gridLayout = QGridLayout()
        row = 0
        while row <= self.lastRowIndex:
            maxColumn = len(self.sampleButtons[row])
            column = 0
            while column < maxColumn:
                gridLayout.addWidget(self.sampleButtons[row][column],row,column)
                column += 1
            row += 1

        buttonGrid = QWidget()
        buttonGrid.setLayout(gridLayout)
        self.mainLayout.addWidget(buttonGrid)

    def addNewSampleButton(self):
        """Add the 'Add a new sample button' button to the interface.
            - Takes no parameter.
            - Returns nothing.
        """
        self. mainLayout.addWidget(QPushButton('New sample'))
        #self.mainLayout.addWidget(QSpacer())


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

        self.sampleButtons[self.lastRowIndex].append(QPushButton(str(self.lastRowIndex)))
