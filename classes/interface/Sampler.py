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

    #Sampler modes
    PLAYMODE = '0'
    EDITMODE = '1'
    DELETEMODE = '2'

    #Sampler styleSheets
    ACTIVEBUTTONSSTYLESHEETPATH = 'ressources/interface/stylesheets/activeSamplerToggleButtons.css'

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.samplePlayer = QMediaPlayer()

        self.sampleButtons = [[]]
        self.lastRowIndex = 0

        self.samplerMode = Sampler.PLAYMODE

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
        self.toggleEditModeButton = QPushButton(self.mainWindow.text.localisation('buttons','samplerEditButton','caption'))
        self.toggleEditModeButton.clicked.connect(lambda *args: self.toggleMode(Sampler.EDITMODE))

        #Toggle delete button
        self.toggleDeleteModeButton = QPushButton(self.mainWindow.text.localisation('buttons','samplerDeleteButton','caption'))
        self.toggleDeleteModeButton.clicked.connect(lambda *args: self.toggleMode(Sampler.DELETEMODE))

        #Add to layout
        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.newSampleButton)
        controlLayout.addWidget(self.toggleEditModeButton)
        controlLayout.addWidget(self.toggleDeleteModeButton)
        controlWidget = QWidget()
        controlWidget.setLayout(controlLayout)
        self.mainLayout.addWidget(controlWidget)

    def toggleMode(self, samplerMode:int):
        """Activate or deactivate different mode for the sampler.
            - Takes one parameter:
                - samplerMode as One of the Sampler constants: PLAYMODE, EDITMODE, DELETEMODE.
            - Returns nothing.
        """
        if samplerMode == Sampler.EDITMODE:
            #Checks if Edit mode is already active
            if self.samplerMode == Sampler.EDITMODE:
                #Deactivate Edit mode and returns to Play mode
                self.samplerMode = Sampler.PLAYMODE
                self.toggleEditModeButton.setStyleSheet(None)
                self.toggleDeleteModeButton.setStyleSheet(None)
            else:
                #Activate Edit mode
                self.samplerMode = samplerMode
                styleSheet = open(Sampler.ACTIVEBUTTONSSTYLESHEETPATH,'r', encoding='utf-8').read()
                self.toggleEditModeButton.setStyleSheet(styleSheet)
                self.toggleDeleteModeButton.setStyleSheet(None)

        elif samplerMode == Sampler.DELETEMODE:
            #Checks if Delete mode is already active
            if self.samplerMode == Sampler.DELETEMODE:
                #Deactivate Delete mode and returns to Play mode
                self.samplerMode = Sampler.PLAYMODE
                self.toggleEditModeButton.setStyleSheet(None)
                self.toggleDeleteModeButton.setStyleSheet(None)
            else:
                #Activate Delete mode
                self.samplerMode = samplerMode
                styleSheet = open(Sampler.ACTIVEBUTTONSSTYLESHEETPATH,'r', encoding='utf-8').read()
                self.toggleEditModeButton.setStyleSheet(None)
                self.toggleDeleteModeButton.setStyleSheet(styleSheet)

        else:
            self.samplerMode = Sampler.PLAYMODE
            self.toggleEditModeButton.setStyleSheet(None)
            self.toggleDeleteButton.setStyleSheet(None)

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
            sampleButton.clicked.connect(lambda *args: self.clickOnSoundEffect(self.sender()))
            buttonRow = self.lastRowIndex

            self.sampleButtons[self.lastRowIndex].append(sampleButton)

            self.sampleButtonsGridLayout.addWidget(sampleButton,buttonRow,buttonColumn)

    def removeSampleButton(self, sampleButton:SoundEffect):
        """Remove a sample button, require the edit mode.
            - Takes one parameter:
                - sampleButton as SoundEffect object.
            - Returns nothing.
        """
        #Checks if edit mode is active:
        if self.samplerMode:
            self.sampleButtonsGridLayout.removeWidget(sampleButton)

    def clickOnSoundEffect(self, soundEffect:SoundEffect):
        """Called when a soundEffect button is clicked.
            - Takes one parameter:
                - soundEffect as soundEffect Object.
            - Returns nothing.
        """
        #Checks sampler's mode
        if self.samplerMode == Sampler.EDITMODE:
            for rowIndex, buttonRow in enumerate(self.sampleButtons):
                for columnIndex, storedButton in enumerate(buttonRow):
                    if soundEffect == storedButton:
                        filepath,iconPath,ok = SampleButtonDialogBox(self.mainWindow,soundEffect.filepath,soundEffect.iconPath).getItems()
                        if ok :
                            self.sampleButtons[rowIndex][columnIndex].changeFile(filepath)
                            self.sampleButtons[rowIndex][columnIndex].changeIcon(iconPath)

        elif self.samplerMode == Sampler.DELETEMODE:
            print('delete')
        else: #Any other cases defaults to playmode
            media = QMediaContent(QUrl.fromLocalFile(soundEffect.filepath))
            self.samplePlayer.setMedia(media)
            self.samplePlayer.play()
