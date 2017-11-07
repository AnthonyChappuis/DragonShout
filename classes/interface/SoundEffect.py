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

    def __init__(self, soundEffectFilePath:str='', soundEffectIconPath:str=''):
        super().__init__()

        self.filepath = soundEffectFilePath
        self.text = QFileInfo(soundEffectFilePath).fileName()

        #Verify if soundEffectIconPath is an str item and defaults it if not.
        if soundEffectIconPath == '' or not isinstance(soundEffectIconPath, str) :
            soundEffectIconPath = ThemeButtonDialogBox.DefaultThemeIconPath
        self.soundEffectIconPath = soundEffectIconPath
        styleSheets = open(SoundEffect.BUTTONSTYLESHEETPATH,'r',encoding='utf-8').read()
        self.setStyleSheet(styleSheets)
        self.setIcon(QIcon(self.soundEffectIconPath))
