#---------------------------------
#Author: Chappuis Anthony
#
#This class defines a sound effect object
# It heritates from QPushButton.
#
#Application: DragonShout music sampler
#Last Edited: October 25th 2017
#---------------------------------

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QFileInfo, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from classes.interface.ThemeButtonDialogBox import ThemeButtonDialogBox


class SoundEffect(QPushButton):

    EFFECTBUTTONSTYLESHEETPATH = 'ressources/interface/stylesheets/soundEffectButtons.css'
    DEFAULTBUTTONSTYLESHEETPATH = 'ressources/interface/stylesheets/defaultEffectButton.css'
    DEFAULTBUTTONICONPATH = 'ressources/interface/addSampleButton.png'
    NEWEFFECTBUTTON = 0
    SOUNDEFFECTBUTTON = 1

    def __init__(self, buttonType:int, coordinates:tuple, soundEffectFilePath:str='', iconPath:str=''):
        super().__init__()

        self.coordinates = coordinates
        self.buttonType = buttonType
        self.filepath = ''

        if buttonType == SoundEffect.SOUNDEFFECTBUTTON:

            self.mediaPlayer = QMediaPlayer()
            self.changeFile(soundEffectFilePath)
            self.changeStyleSheet()

            #Verify if iconPath is an str item and defaults it if not.
            if iconPath != '' and isinstance(iconPath, str) :
                self.changeIcon(iconPath)

        else:
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
        """Either start or stop the QMediaPlayer with the sound effect's file
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
