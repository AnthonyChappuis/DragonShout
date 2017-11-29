#---------------------------------
#Author: Chappuis Anthony
#
#This class manage the buttons of the sampler function.
#
#Application: DragonShout music sampler
#Last Edited: November 29th 2017
#---------------------------------

import json

from classes.interface import MainWindow
from classes.interface.SoundEffect import SoundEffect
from classes.interface.SampleButtonDialogBox import SampleButtonDialogBox

from PyQt5 import Qt
from PyQt5.QtCore import QUrl

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout

class Sampler(QWidget):

    #Sampler modes
    PLAYMODE = '0'
    EDITMODE = '1'
    DELETEMODE = '2'

    #Sampler styleSheets
    ACTIVEBUTTONSSTYLESHEETPATH = 'ressources/interface/stylesheets/activeSamplerToggleButtons.css'

    #Class method
    def load(cls, filepath: str=''):
        """Used to load a sample set from the hard drive (JSON).
            - Takes one parameter:
                - filepath as string
            - Returns:
                - False as boolean or sampleSet as list.
        """
    #try:
        with open(filepath, "r", encoding="utf-8") as json_file:
            completeJSON = json.load(json_file)

        sampleSet = completeJSON["SampleSet"]
        return sampleSet
    #except :
        #return False
    load = classmethod(load)

    def __init__(self, mainWindow:MainWindow, sampleSet:list=None):
        super().__init__()

        self.mainWindow = mainWindow

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
        self.sampleButtonsGridLayout = self.constructGrid(sampleSet)
        self.buttonGrid = QWidget()
        self.buttonGrid.setLayout(self.sampleButtonsGridLayout)
        self.mainLayout.addWidget(self.buttonGrid)

        self.mainLayout.addStretch(1)

    def constructGrid(self, sampleSet:list):
        """Constructs the buttons' grid according to the self.sampleButtons property
            - Takes no parameter.
            - Returns a QGridLayout containing the sample buttons.
        """
        gridLayout = QGridLayout()
        self.sampleButtons = [[]]
        row = 0
        while row <= self.lastRowIndex:
            column = 0
            while column < self.MAXBUTTONPERROW:
                if sampleSet != None :
                    for sampleJSON in sampleSet:
                        soundEffect = SoundEffect.unserialize(sampleJSON)
                        if soundEffect.coordinates == (row,column):
                            sampleButton = soundEffect
                else:
                    sampleButton = SoundEffect(self.mainWindow,SoundEffect.NEWEFFECTBUTTON,(row,column))
                    sampleButton.clicked.connect(lambda *args: self.clickOnSoundEffect(self.sender()))
                    self.sampleButtons[row].append(sampleButton)
                    gridLayout.addWidget(sampleButton,row,column)
                column += 1
            self.sampleButtons.append([])
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

            sampleButton = SoundEffect(self.mainWindow,SoundEffect.SOUNDEFFECTBUTTON,(row,column),path,icon)
            sampleButton.clicked.connect(lambda *args: self.clickOnSoundEffect(self.sender()))
            self.sampleButtonsGridLayout.itemAtPosition(row,column).widget().setParent(None)
            self.sampleButtonsGridLayout.addWidget(sampleButton,row,column)
            self.sampleButtons[row][column] = sampleButton

    def removeSampleButton(self, soundEffect:SoundEffect):
        """Remove a sample button, require the Delete mode.
            - Takes one parameter:
                - sampleButton as SoundEffect object.
            - Returns nothing.
        """
        row = soundEffect.coordinates[0]
        column = soundEffect.coordinates[1]

        sampleButton = SoundEffect(SoundEffect.NEWEFFECTBUTTON,(row,column))
        sampleButton.clicked.connect(lambda *args: self.clickOnSoundEffect(self.sender()))
        self.sampleButtonsGridLayout.itemAtPosition(row,column).widget().setParent(None)
        self.sampleButtonsGridLayout.addWidget(sampleButton,row,column)
        self.sampleButtons[row][column] = sampleButton

    def editSampleButton(self, soundEffect:SoundEffect):
        """Edit a sample button.
            - Takes one parameter:
                - sampleButton as SoundEffect object.
            - Returns nothing.
        """
        filepath,iconPath,ok = SampleButtonDialogBox(self.mainWindow,soundEffect.filepath,soundEffect.iconPath).getItems()

        if ok :
            soundEffect.changeFile(filepath)
            soundEffect.changeIcon(iconPath)

    def clickOnSoundEffect(self, soundEffect:SoundEffect):
        """Called when a soundEffect button is clicked.
            - Takes one parameter:
                - soundEffect as soundEffect Object.
            - Returns nothing.
        """
        #Checks sampler's mode
        if soundEffect.buttonType == SoundEffect.SOUNDEFFECTBUTTON:
            if self.samplerMode == Sampler.EDITMODE:
                self.editSampleButton(soundEffect)

            elif self.samplerMode == Sampler.DELETEMODE:
                self.removeSampleButton(soundEffect)

            else :
                soundEffect.playOrStop()

        else: #Any other cases defaults to prompting the new sample button dialog.
            self.addSampleButton(soundEffect.coordinates)

    def serialize(self):
        """Used to serialize instance data to JSON format.
            - Takes no parameter.
            - Returns instance data as dictionnary.
        """

        sampleButtons_list = []
        for row in self.sampleButtons:
            for sampleButton in row:
                sampleButtons_list.append(sampleButton.serialize())

        return {"__class__":        "SoundEffect",
                "sampleButtons":    sampleButtons_list}
