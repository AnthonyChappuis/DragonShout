#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for storing all textes of the application
#It also manage which language is used when showing textes.
#
#Application: DragonShout music sampler
#Last Edited: April 11th 2017
#---------------------------------

import os

class Text:
    LanguageFilePath = 'lang.txt'
    SupportedLanguages = {'French' : 'fr', 'English' : 'en'}

    def isSupportedLanguage(self, language:str):
        """Check if the given language is supported by the application
            Takes one parameter:
            - language as string.
            Returns:
            - supported as boolean.
        """
        supported = False

        for supportedLanguage in Text.SupportedLanguages :
            if language == supportedLanguage :
                supported = True

        return supported


    def loadLanguage(self):
        """Used to define the language of the application by retrieving the info stored in
            lang.txt which is located in the application root directory.
            Takes no parameter.
            Returns nothing.
        """
        #Check if the language file exist and create it uf necessary
        if os.path.isfile(Text.LanguageFilePath) :
            languageFile = open(Text.LanguageFilePath,'r')
            language = languageFile.read()
        else:
            language = Text.SupportedLanguages['English']
            self.saveLanguage(language)


        #Defaults to english is the language is not recognized as a supported language
        if self.isSupportedLanguage(language) :
            self.language = language
        else:
            self.language = Text.SupportedLanguages['English']

    def saveLanguage(self, language:str):
        """Save the chosen language in lang.txt at the Text.LanguageFilePath location.
            Takes one parameter:
            - language as str (Use Text.SupportedLanguages['...'] to ensure compatibility).
        """
        if not(os.path.isfile(Text.LanguageFilePath)) :
            open(Text.LanguageFilePath,'x', encoding='utf-8')

        languageFile = open(Text.LanguageFilePath, 'w', encoding='utf-8')
        languageFile.write(language)


    def localisation(self,elementType:str,elementName:str,textType:str = 'caption'):
        return self._localisation[elementType][elementName][textType]

    def __init__(self,language:str):

        self.loadLanguage()

        #English
        if self.language == Text.SupportedLanguages['English']:

            buttons = {
                'scene': {'caption':'Scene','toolTip':"Changes the scene and gives access to a new group of themes"},
                'newTheme': {'caption':'New theme','toolTip':"Change the musical theme"}
            }

            menus = {
                'files': {'caption':"Files",'toolTip': 'This is a <b>QWidget</b> widget'},
                'options': {'caption':'Options','toolTip': 'Software options'}
            }

            menuEntries = {
                'exit': { 'caption':'Exit', 'toolTip': "Exit the application"},
                'language': { 'caption':'Language', 'toolTip': "Select the language of the application"},
                'save' : { 'caption':'Save', 'toolTip': "Save your work"},
                'load' : {'caption':'Load', 'toolTip': "Load an existing library"}
            }

            messageBoxes = {
                'deleteTheme': {'caption':'Do you really want to delete this theme ?', 'title':'Delete '}
            }

            dialogBoxes = {
                'newTheme': {'caption':'New theme','toolTip':'Name the new theme','question':'Enter the theme name :'},
                'addMusic': {'caption':'Choose a track to add to this theme','toolTip':'Navigate the drive for a track to add to the theme'},
                'saveLibrary': {'title':'Save your work'}
            }

            labels = {
                'scenes' : { 'caption': 'Scenes','toolTip':'List of musical scenes'},
                'playlistLabel' : {'caption': 'Select a theme to play','toolTip':'Shows the playlist of the selected theme'},
                'chooseThemeFirst': {'caption': 'Choose or create a theme first'}
            }

        #French
        if language == Text.SupportedLanguages['French']:
            buttons = {
                'scene': {'caption':'Scène','toolTip':"Change de scène et accède à un nouveau groupe de thèmes"},
                'newTheme': {'caption':'Nouveau thème','toolTip':"Change le thème musical"}
            }

            menus =  {
                'files': {'caption':"Fichiers",'toolTip': 'Ceci est un widget <b>QWidget</b>'},
                'options': {'caption':'Options','toolTip': 'Options du programme'}
            }

            menuEntries = {
                'exit': { 'caption':'Quitter', 'toolTip':"Quitter l'application."},
                'language': { 'caption':'Langue', 'toolTip': "Sélectionner la langue de l'application"},
                'save' : { 'caption':'Sauvegarder', 'toolTip': "Sauvegarder votre travail"},
                'load' : {'caption':'Charger', 'toolTip': "Charger une librairie existante"}
            }

            messageBoxes = {
                'deleteTheme': {'caption':'Voulez vous vraiment supprimer le thème ?', 'title':'Supprimer '}
            }

            dialogBoxes = {
                'newTheme': {'caption':'Nouveau thème','toolTip':'Nommer le nouveau thème','question':'Entrer le nom du thème :'},
                'addMusic': {'caption':'Choisir un morceau à ajouter au thème','toolTip':"Parcours le disque à la recherche d'un morceau à ajouter au thème"},
                'saveLibrary': {'title':'Sauver votre travail'}
            }

            labels = {
                'scenes' : { 'caption': 'Scènes','toolTip':'Liste des scènes musicales'},
                'playlistLabel' : {'caption': 'Sélectionne un thème à jouer ','toolTip':'Montre la liste de lecture du thème sélectionné'},
                'chooseThemeFirst': {'caption': "Il faut d'abord choisir ou créer un thème"}
            }


        self._localisation = {'buttons': buttons, 'menus': menus, 'menuEntries': menuEntries, 'messageBoxes': messageBoxes,
                                'labels': labels,'dialogBoxes': dialogBoxes}
