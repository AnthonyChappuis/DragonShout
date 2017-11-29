#---------------------------------
#Author: Chappuis Anthony
#
#This class defines a sound effect object
# It heritates from QPushButton.
#
#Application: DragonShout music sampler
#Last Edited: November 29th 2017
#---------------------------------

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QMessageBox
from PyQt5.QtCore import QFileInfo, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from classes.interface.SampleButtonDialogBox import SampleButtonDialogBox
from classes.interface import MainWindow


class SoundEffect(QPushButton):

    #Style sheets
    EFFECTBUTTONSTYLESHEETPATH = 'ressources/interface/stylesheets/soundEffectButtons.css'
    ACTIVEEFFECTBUTTONSSTYLESHEETPATH = 'ressources/interface/stylesheets/activeSoundEffectButtons.css'

    DEFAULTBUTTONSTYLESHEETPATH = 'ressources/interface/stylesheets/defaultEffectButton.css'

    #Icons
    DEFAULTBUTTONICONPATH = 'ressources/interface/addSampleButton.png'

    #Button Types
    NEWEFFECTBUTTON = 0
    SOUNDEFFECTBUTTON = 1

    #Class method
    def unserialize(cls,data: dict):
        """Used to unsrialize JSON data for SoundEffect instances
            - Takes one parameter:
                - data as dictionnary
                - mainWindow as MainWindow
            - Returns nothing
        """
        if "__class__" in data :
            if data["__class__"] == "SoundEffect":
                #creating SoundEffect instance
                soundEffect_object = SoundEffect(mainWindow,data["buttonType"],data["coordinates"],data["filepath"],data["iconPath"])
                return soundEffect_object
            return data
        unserialize = classmethod(unserialize)

    #constructor
    def __init__(self, mainWindow:MainWindow, buttonType:int, coordinates:tuple, soundEffectFilePath:str='', iconPath:str=''):
        super().__init__()

        self.mainWindow = mainWindow
        self.coordinates = coordinates
        self.buttonType = buttonType
        self.filepath = ''

        if buttonType == SoundEffect.SOUNDEFFECTBUTTON: #Creates a full sound effect Button

            self.mediaPlayer = QMediaPlayer()
            self.mediaPlayer.stateChanged.connect(lambda *args: self.playerStatusChanged())

            self.changeFile(soundEffectFilePath)
            self.changeStyleSheet()

            #Verify if iconPath is an str item and defaults it if not.
            if iconPath != '' and isinstance(iconPath, str) :
                self.changeIcon(iconPath)

        else: #Creates a default button to show effects availability on the interface
            self.changeIcon(SoundEffect.DEFAULTBUTTONICONPATH)
            self.changeStyleSheet(SoundEffect.DEFAULTBUTTONSTYLESHEETPATH)

    def changeIcon(self, iconPath:str):
        self.iconPath = iconPath
        self.setIcon(QIcon(iconPath))

    def changeFile(self, filepath:str):
        """Change sound Effect file and loads it into the player.
            - Takes one parameter:
                - filepath as str.
            - Returns nothing.
        """
        self.filepath = filepath
        media = QMediaContent(QUrl.fromLocalFile(self.filepath))
        self.mediaPlayer.setMedia(media)

    def changeStyleSheet(self, styleSheetPath:str='Default'):
        if styleSheetPath == 'Default':
            styleSheet = open(SoundEffect.EFFECTBUTTONSTYLESHEETPATH,'r',encoding='utf-8').read()
        else:
            styleSheet = open(styleSheetPath,'r',encoding='utf-8').read()

        self.setStyleSheet(styleSheet)

    def playOrStop(self):
        """Either start or stop the media player.
            - Takes no parameter.
            - Returns nothing.
        """
        if self.buttonType == SoundEffect.SOUNDEFFECTBUTTON:
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.stop()
            else:
                self.mediaPlayer.play()

        else:
            print('WARNING - this is a default button, no sound file is attached to it')

    def playerStatusChanged(self):
        """Handle player status changes.
            - Takes no parameter.
            - Returns nothing.
        """

        #Player encountered an error relative to the loaded media
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.InvalidMedia:
            QMessageBox(QMessageBox.Critical,self.mainWindow.text.localisation('messageBoxes','loadMedia','title'),self.mainWindow.text.localisation('messageBoxes','loadMedia','caption')).exec()

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.changeStyleSheet(SoundEffect.ACTIVEEFFECTBUTTONSSTYLESHEETPATH)

        elif self.mediaPlayer.state() == QMediaPlayer.StoppedState:
            self.changeStyleSheet(SoundEffect.EFFECTBUTTONSTYLESHEETPATH)

    def serialize(self):
        """Used to serialize instance data to JSON format.
            - Takes no parameter.
            - Returns instance data as dictionnary.
        """
        return {"__class__":    "SoundEffect",
                "coordinates":  self.coordinates,
                "buttonType":   self.buttonType,
                "filepath":     self.filepath,
                "iconPath":     self.iconPath}
