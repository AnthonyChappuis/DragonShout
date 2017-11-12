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

    BUTTONSTYLESHEETPATH = 'ressources/interface/stylesheets/soundEffectButtons.css'

    def __init__(self, soundEffectFilePath:str='', iconPath:str=''):
        super().__init__()

        self.changeFile(soundEffectFilePath)
        self.changeStyleSheet()

        #Verify if iconPath is an str item and defaults it if not.
        if iconPath == '' or not isinstance(iconPath, str) :
            iconPath = ThemeButtonDialogBox.DefaultThemeIconPath
        self.changeIcon(iconPath)

    def changeIcon(self, iconPath:str):
        self.iconPath = iconPath
        self.setIcon(QIcon(iconPath))

    def changeFile(self, filepath:str):
        self.filepath = filepath
        self.setText(QFileInfo(filepath).fileName())

    def changeStyleSheet(self, styleSheetPath:str='Default'):
        if styleSheetPath == 'Default':
            styleSheet = open(SoundEffect.BUTTONSTYLESHEETPATH,'r',encoding='utf-8').read()
        else:
            styleSheet = open(styleSheetPath,'r',encoding='utf-8').read()

        self.setStyleSheet(styleSheet)
