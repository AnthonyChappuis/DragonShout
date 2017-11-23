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

        self.lastRowIndex = 4

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
        self.buttonGrid = QWidget()
        self.buttonGrid.setLayout(self.sampleButtonsGridLayout)
        self.mainLayout.addWidget(self.buttonGrid)

        self.mainLayout.addStretch(1)

    def constructGrid(self):
        """Constructs the buttons' grid according to the self.sampleButtons property
            - Takes no parameter.
            - Returns a QGridLayout containing the sample buttons.
        """
        gridLayout = QGridLayout()
        row = 0
        while row <= self.lastRowIndex:
            column = 0
            while column < self.MAXBUTTONPERROW:
                defaultSampleButton = SoundEffect(SoundEffect.NEWEFFECTBUTTON,(row,column))
                defaultSampleButton.clicked.connect(lambda *args: self.clickOnSoundEffect(self.sender()))
                gridLayout.addWidget(defaultSampleButton,row,column)
                column += 1
            row += 1

        return gridLayout

    def addControlButtons(self):
        """Add the the control buttons to the interface.
            - Takes no parameter.
            - Returns nothing.
        """
        #Toggle edit mode button
        self.toggleEditModeButton = QPushButton(self.mainWindow.text.localisation('buttons','samplerEditButton','caption'))
        self.toggleEditModeButton.clicked.connect(lambda *args: self.toggleMode(Sampler.EDITMODE))

        #Toggle delete button
        self.toggleDeleteModeButton = QPushButton(self.mainWindow.text.localisation('buttons','samplerDeleteButton','caption'))
        self.toggleDeleteModeButton.clicked.connect(lambda *args: self.toggleMode(Sampler.DELETEMODE))

        #Add to layout
        controlLayout = QHBoxLayout()
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

    def addSampleButton(self, coordinates:tuple):
        """Show the Sample button dialog to transform a default button into a soundEffect button.
            - Takes no parameter.
            - Returns nothing.
        """
        #Check if the last row is full according to self.MAXBUTTONPERROW.
        #It begins a new row if necessary
        path,icon, ok = SampleButtonDialogBox(self.mainWindow).getItems()

        if ok :
            row = coordinates[0]
            column = coordinates[1]

            sampleButton = SoundEffect(SoundEffect.SOUNDEFFECTBUTTON,(row,column),path,icon)
            sampleButton.clicked.connect(lambda *args: self.clickOnSoundEffect(self.sender()))
            self.sampleButtonsGridLayout.itemAtPosition(row,column).widget().setParent(None)
            self.sampleButtonsGridLayout.addWidget(sampleButton,row,column)

    def removeSampleButton(self, soundEffect:SoundEffect):
        """Remove a sample button, require the Delete mode.
            - Takes one parameter:
                - sampleButton as SoundEffect object.
            - Returns nothing.
        """
        lastButtonColumn = len(self.sampleButtons[self.lastRowIndex])
        for rowIndex, buttonRow in enumerate(self.sampleButtons):
            for columnIndex, storedButton in enumerate(buttonRow):
                if soundEffect == storedButton:
                    self.sampleButtonsGridLayout.itemAtPosition(rowIndex,columnIndex).widget().setParent(None)
                    self.sampleButtons[rowIndex].remove(self.sampleButtons[rowIndex][columnIndex])

                    if (lastButtonColumn-1) == 0 and self.lastRowIndex > 0 :
                        self.sampleButtons.remove(self.sampleButtons[self.lastRowIndex])
                        self.lastRowIndex -= 1

        #QWidget().setLayout(self.buttonGrid.layout())
        #self.buttonGrid.setLayout(self.constructGrid())


    def editSampleButton(self, soundEffect:SoundEffect):
        """Edit a sample button.
            - Takes one parameter:
                - sampleButton as SoundEffect object.
            - Returns nothing.
        """
        for rowIndex, buttonRow in enumerate(self.sampleButtons):
            for columnIndex, storedButton in enumerate(buttonRow):
                if soundEffect == storedButton:
                    filepath,iconPath,ok = SampleButtonDialogBox(self.mainWindow,soundEffect.filepath,soundEffect.iconPath).getItems()
                    if ok :
                        self.sampleButtons[rowIndex][columnIndex].changeFile(filepath)
                        self.sampleButtons[rowIndex][columnIndex].changeIcon(iconPath)

    def clickOnSoundEffect(self, soundEffect:SoundEffect):
        """Called when a soundEffect button is clicked.
            - Takes one parameter:
                - soundEffect as soundEffect Object.
            - Returns nothing.
        """
        #Checks sampler's mode
        if self.samplerMode == Sampler.EDITMODE:
            self.editSampleButton(soundEffect)

        elif self.samplerMode == Sampler.DELETEMODE:
            self.removeSampleButton(soundEffect)

        elif soundEffect.buttonType == SoundEffect.SOUNDEFFECTBUTTON:
            media = QMediaContent(QUrl.fromLocalFile(soundEffect.filepath))
            self.samplePlayer.setMedia(media)
            self.samplePlayer.play()

        else: #Any other cases defaults to prompting the new sample button dialog.
            self.addSampleButton(soundEffect.coordinates)
