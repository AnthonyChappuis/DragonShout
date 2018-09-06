#---------------------------------
#Author: Chappuis Anthony
#
#This class manage the buttons of the sampler function.
#
#Application: DragonShout music sampler
#Last Edited: August 20th 2018
#---------------------------------

import json

from classes.interface import MainWindow
from classes.ressourcesFilepath import Stylesheets
from classes.interface.SoundEffect import SoundEffect
from classes.interface.SampleButtonDialogBox import SampleButtonDialogBox

from PyQt5 import Qt
from PyQt5.QtCore import QUrl

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QSlider

class Sampler(QWidget):

    #Sampler modes
    PLAYMODE = '0'
    EDITMODE = '1'
    DELETEMODE = '2'

    #Sample volumes
    MINVOLUME = 0
    MAXVOLUME = 100

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow

        self.lastRowIndex = 9

        self.samplerMode = Sampler.PLAYMODE

        self.MAXBUTTONPERROW = 6

        #Grid layout
        self.sampleButtonsGridLayout = self.constructGrid()

        #Main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.Qt.AlignHCenter)
        self.setLayout(self.mainLayout)

        self.populateMainLayout()
        self.changeVolume(int(Sampler.MAXVOLUME/2))


    def populateMainLayout(self):
        """Used to place the various widget of this module on the main layout.
            - Takes no parameter.
            - Returns nothing.
        """
        #Control buttons
        self.addControlButtons()

        #Sample buttons grid layout
        self.buttonGrid = QWidget()
        self.buttonGrid.setLayout(self.sampleButtonsGridLayout)
        self.mainLayout.addWidget(self.buttonGrid)

        self.mainLayout.addStretch(1)

    def constructGrid(self, sampleSet:list=None):
        """Constructs the buttons' grid according to the self.sampleButtons property
            - Takes no parameter.
            - Returns a QGridLayout containing the sample buttons.
        """
        gridLayout = QGridLayout()
        self.sampleButtons = [[]]


        #If a sample set is provided = create buttons according to the sample set
        if sampleSet != None :
            #Creating all objects from the sample set
            soundEffects = []
            for sampleJSON in sampleSet:
                soundEffect = SoundEffect.unserialize(self.mainWindow,sampleJSON)
                soundEffect.clicked.connect(lambda *args: self.clickOnSoundEffect(self.sender()))
                soundEffects.append(soundEffect)

            row = 0
            while row <= self.lastRowIndex:
                column = 0
                while column < self.MAXBUTTONPERROW:
                    #Place each object on the grids
                    for soundEffect in soundEffects:
                        buttonRow = soundEffect.coordinates[0]
                        buttonColumn = soundEffect.coordinates[1]
                        if buttonRow == row and buttonColumn == column:
                            gridLayout.addWidget(soundEffect,row,column)
                            self.sampleButtons[row].append(soundEffect)
                    column += 1
                self.sampleButtons.append([])
                row += 1

        #if no sample set is provided = creates only default buttons
        else:
            row = 0
            while row <= self.lastRowIndex:
                column = 0
                while column < self.MAXBUTTONPERROW:
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

        #Volume control
        self.volumeSlider = QSlider(Qt.Qt.Vertical)
        self.volumeSlider.setMinimum(Sampler.MINVOLUME)
        self.volumeSlider.setMaximum(Sampler.MAXVOLUME)
        self.volumeSlider.setTickPosition(QSlider.TicksBelow)
        self.volumeSlider.valueChanged.connect(lambda *args: self.changeVolume(self.sender().value()))
        self.volumeSlider.setValue(int(Sampler.MAXVOLUME/2))
        controlLayout.addWidget(self.volumeSlider)

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
                styleSheet = open(Stylesheets.activeToggleButtons,'r', encoding='utf-8').read()
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
                styleSheet = open(Stylesheets.activeToggleButtons,'r', encoding='utf-8').read()
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
        path,icon, styleSheetPath, ok = SampleButtonDialogBox(self.mainWindow).getItems()

        if ok :
            row = coordinates[0]
            column = coordinates[1]

            sampleButton = SoundEffect(self.mainWindow,SoundEffect.SOUNDEFFECTBUTTON,(row,column),path,icon,styleSheetPath)
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

        sampleButton = SoundEffect(self.mainWindow, SoundEffect.NEWEFFECTBUTTON,(row,column))
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
        filepath,iconPath, styleSheetPath,ok = SampleButtonDialogBox(self.mainWindow,soundEffect.filepath,soundEffect.iconPath,soundEffect.styleSheetPath).getItems()
        if ok :
            soundEffect.changeFile(filepath)
            soundEffect.changeIcon(iconPath)
            soundEffect.changeStyleSheet(styleSheetPath)

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

    def changeVolume(self, newVolume:int):
        """Used to change all the soundEffects volume.
            - Takes one parameter:
                - newVolume as integer.
            - Returns nothing.
        """
        for row in self.sampleButtons:
            for soundEffect in row:
                if soundEffect.buttonType == SoundEffect.SOUNDEFFECTBUTTON:
                    soundEffect.mediaPlayer.setVolume(newVolume)

    def countEffects(self):
        """Count number of effects.
            Takes no parameter.
            Returns:
            - effectNumber as integer.
        """
        effectNumber = 0
        for row in self.sampleButtons :
            for button in row :
                effectNumber += 1
        return effectNumber

    def load(self, filepath: str='',loadType:str="run"):
        """Used to load a sample set from the hard drive (JSON).
            - Takes one parameter:
                - filepath as string
            - Returns:
                - False as boolean or sampleSet as list.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as json_file:
                completeJSON = json.load(json_file)

            sampleSet = completeJSON["SampleSet"]

            if loadType == "run":
                newButtonGrid = QWidget()
                newButtonsGridLayout = self.constructGrid(sampleSet)
                newButtonGrid.setLayout(newButtonsGridLayout)
                oldButtonGrid = self.mainLayout.replaceWidget(self.buttonGrid,newButtonGrid)

                oldButtonGrid.widget().setParent(None)
                self.buttonGrid = newButtonGrid
                self.sampleButtonsGridLayout = newButtonsGridLayout

            elif loadType == "test":
                return True
        except :
            return False

    def serialize(self):
        """Used to serialize instance data to JSON format.
            - Takes no parameter.
            - Returns instance data as dictionnary.
        """

        sampleButtons_list = []
        for row in self.sampleButtons:
            for sampleButton in row:
                sampleButtons_list.append(sampleButton.serialize())

        return sampleButtons_list
