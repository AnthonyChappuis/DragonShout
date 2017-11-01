#---------------------------------
#Author: Chappuis Anthony
#
#This class manage the buttons of the sampler function.
#
#Application: DragonShout music sampler
#Last Edited: November 01st 2017
#---------------------------------

from classes.interface import MainWindow
from classes.interface.SoundEffect import SoundEffect
from classes.interface.SampleButtonDialogBox import SampleButtonDialogBox

from PyQt5 import Qt
from PyQt5.QtCore import QUrl

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout

class Sampler(QWidget):

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.samplePlayer = QMediaPlayer()

        self.sampleButtons = [[]]
        self.lastRowIndex = 0

        self.editMode = False

        self.MAXBUTTONPERROW = 4

        #Main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.Qt.AlignHCenter)
        self.setLayout(self.mainLayout)

        #Control buttons
        self.addControlButtons()

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

    def addControlButtons(self):
        """Add the the control buttons to the interface.
            - Takes no parameter.
            - Returns nothing.
        """
        #New sample button
        self.newSampleButton = QPushButton(self.mainWindow.text.localisation('buttons','addSample','caption'))
        self.newSampleButton.clicked.connect(lambda *args: self.addSampleButton())

        #Toggle edit mode button
        self.toggleEditModeButton = QPushButton('Edit')
        self.toggleEditModeButton.clicked.connect(lambda *args: self.toggleEditMode())

        #Add to layout
        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.newSampleButton)
        controlLayout.addWidget(self.toggleEditModeButton)
        controlWidget = QWidget()
        controlWidget.setLayout(controlLayout)
        self.mainLayout.addWidget(controlWidget)

    def toggleEditMode(self):
        """Activate or deactivate edit mode for the sampler.
            - Takes no parameter.
            - Returns nothing.
        """
        if self.editMode == True:
            self.editMode = False
            self.toggleEditModeButton.setStyleSheet('')
        else :
            self.editMode = True
            styleSheet = open('ressources/interface/toggleEditModeButton.css','r', encoding='utf-8').read()
            self.toggleEditModeButton.setStyleSheet(styleSheet)

    def addSampleButton(self):
        """Append a new QPushButton to self.sampleButtons.
            - Takes no parameter.
            - Returns nothing.
        """
        #Check if the last row is full according to self.MAXBUTTONPERROW.
        #It begins a new row if necessary
        path,icon, ok = SampleButtonDialogBox(self.mainWindow).getItems()

        if ok :
            buttonColumn = len(self.sampleButtons[self.lastRowIndex])
            if buttonColumn >= self.MAXBUTTONPERROW:
                self.sampleButtons.append([])
                self.lastRowIndex += 1
                buttonColumn = 0

            sampleButton = SoundEffect(path,icon)
            sampleButton.clicked.connect(lambda *args: self.playSoundEffect(self.sender()))
            buttonRow = self.lastRowIndex

            self.sampleButtons[self.lastRowIndex].append(sampleButton)

            self.sampleButtonsGridLayout.addWidget(sampleButton,buttonRow,buttonColumn)

    def playSoundEffect(self, soundEffect:SoundEffect):
        """Called when a soundEffect button is clicked.
            - Takes one parameter:
                - soundEffect as soundEffect Object.
            - Returns nothing.
        """
        print(str(soundEffect))
        media = QMediaContent(QUrl.fromLocalFile(soundEffect.filepath))
        self.samplePlayer.setMedia(media)
        self.samplePlayer.play()
