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

        #Sample buttons grid layout
        self.sampleButtonsGridLayout = self.constructGrid()
        buttonGrid = QWidget()
        buttonGrid.setLayout(self.sampleButtonsGridLayout)
        self.mainLayout.addWidget(buttonGrid)

        self.mainLayout.addStretch(1)

    def constructGrid(self):
        """Constructs the buttons' grid according to the self.sampleButtons property
            - Takes no parameter.
            - Returns a QGridLayout containing the sample buttons.
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

        return gridLayout

    def addNewSampleButton(self):
        """Add the 'Add a new sample button' button to the interface.
            - Takes no parameter.
            - Returns nothing.
        """
        self.newSampleButton = QPushButton('New sample')
        self.newSampleButton.clicked.connect(lambda *args: self.addSampleButton())
        self.mainLayout.addWidget(self.newSampleButton)


    def addSampleButton(self):
        """Append a new QPushButton to self.sampleButtons.
            - Takes no parameter.
            - Returns nothing.
        """
        #Check if the last row is full according to self.MAXBUTTONPERROW.
        #It begins a new row if necessary
        buttonColumn = len(self.sampleButtons[self.lastRowIndex])
        if buttonColumn >= self.MAXBUTTONPERROW:
            self.sampleButtons.append([])
            self.lastRowIndex += 1
            buttonColumn = 0

        sampleButton = QPushButton(str(self.lastRowIndex))
        buttonRow = self.lastRowIndex

        self.sampleButtons[self.lastRowIndex].append(sampleButton)

        self.sampleButtonsGridLayout.addWidget(sampleButton,buttonRow,buttonColumn)
