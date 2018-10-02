#---------------------------------
#Author: Chappuis Anthony
#
#Contain the filepath to every ressources of the application.
#
#Application: DragonShout music sampler
#Last Edited: August 31th 2018
#---------------------------------

from pathlib import Path

class Stylesheets():
    #Diverse
    globalStyle = "ressources/interface/stylesheets/global.css"
    themeButtons = "ressources/interface/stylesheets/themeButtons.css"
    activeToggleButtons = "ressources/interface/stylesheets/activeToggleButtons.css"

    #Effect buttons
    effectButtons = "ressources/interface/stylesheets/soundEffects/soundEffectButtons.css"
    redEffectButtons = "ressources/interface/stylesheets/soundEffects/redSoundEffectButtons.css"
    yellowEffectButtons = "ressources/interface/stylesheets/soundEffects/yellowSoundEffectButtons.css"
    greyEffectButtons = "ressources/interface/stylesheets/soundEffects/greySoundEffectButtons.css"
    purpleEffectButtons = "ressources/interface/stylesheets/soundEffects/purpleSoundEffectButtons.css"
    blueEffectButtons = "ressources/interface/stylesheets/soundEffects/blueSoundEffectButtons.css"
    activeEffectButtons = "ressources/interface/stylesheets/soundEffects/activeSoundEffectButtons.css"
    defaultButtons = "ressources/interface/stylesheets/defaultButtons.css"


class Images():
    #General
    applicationIcon = "dragonShout.png"

    #Themes
    DefaultThemeIconPath = str(Path("ressources/interface/defaultButtonIcon.png").resolve())

    #Players
    repeatIcon = "ressources/interface/repeat.png"
    playIcon = "ressources/interface/play.png"
    stopIcon = "ressources/interface/stop.png"
    defaultButtonIcon = "ressources/interface/defaultButtonIcon.png"
    addSampleButtonIcon = "ressources/interface/addSampleButton.png"
    deleteButtonIcon = "ressources/interface/delete.png"
    colorSchemeSelectorIcon = "ressources/interface/colorSchemeSelector.png"

    #File menu
    saveIcon =      str(Path('ressources/interface/saveIcon.png').resolve())
    loadIcon =      str(Path('ressources/interface/loadIcon.png').resolve())
    exportIcon =    str(Path('ressources/interface/exportIcon.png').resolve())
    importIcon =    str(Path('ressources/interface/importIcon.png').resolve())
    exitIcon =      str(Path('ressources/interface/exitIcon.png').resolve())
