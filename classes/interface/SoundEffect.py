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
from PyQt5.QtCore import QFileInfo

from classes.interface.ThemeButtonDialogBox import ThemeButtonDialogBox

class SoundEffect(QPushButton):

    EFFECTBUTTONSTYLESHEETPATH = 'ressources/interface/stylesheets/soundEffectButtons.css'
    DEFAULTBUTTONSTYLESHEETPATH = 'ressources/interface/stylesheets/defaultEffectButton.css'
    DEFAULTBUTTONICONPATH = 'ressources/interface/defaultButtonIcon.png'
    NEWEFFECTBUTTON = 0
    SOUNDEFFECTBUTTON = 1

    def __init__(self, buttonType:int, soundEffectFilePath:str='', iconPath:str='', coordinates:tuple=(0,0)):
        super().__init__()

        self.coordinates = coordinates

        if buttonType == SoundEffect.SOUNDEFFECTBUTTON:

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
        self.filepath = filepath
        self.setText(QFileInfo(filepath).fileName())

    def changeStyleSheet(self, styleSheetPath:str='Default'):
        if styleSheetPath == 'Default':
            styleSheet = open(SoundEffect.EFFECTBUTTONSTYLESHEETPATH,'r',encoding='utf-8').read()
        else:
            styleSheet = open(styleSheetPath,'r',encoding='utf-8').read()

        self.setStyleSheet(styleSheet)
