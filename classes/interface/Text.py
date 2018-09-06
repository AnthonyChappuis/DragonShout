#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for storing all textes of the application
#It also manage which language is used when showing textes.
#
#Application: DragonShout music sampler
#Last Edited: September 06th 2018
#---------------------------------

import os

class Text():
    LanguageFileName = 'lang.txt'
    SupportedLanguages = {  'French' : {'caption':'Français','icon':'ressources/interface/France.png'},
                            'English' : {'caption': 'English','icon':'ressources/interface/england.png'}
                        }

    def isSupportedLanguage(self, language:str):
        """Check if the given language is supported by the application
            Takes one parameter:
            - language as string.
            Returns:
            - supported as boolean.
        """
        supported = False

        for supportedLanguageKey, supportedLanguageValue in Text.SupportedLanguages.items() :
            if language == supportedLanguageValue['caption'] :
                supported = True
        return supported


    def loadLanguage(self):
        """Used to define the language of the application by retrieving the info stored in
            lang.txt which is located in the application root directory.
            Takes no parameter.
            Returns nothing.
        """
        #Check if the language file exist and create it if necessary
        if os.path.isfile(self.languageFilePath) :
            languageFile = open(self.languageFilePath,'r', encoding='utf-8')
            language = str.rstrip(languageFile.read())
        else:
            language = Text.SupportedLanguages['English']['caption']
            self.saveLanguage(language)


        #Defaults to english if the language is not recognized as a supported language
        if self.isSupportedLanguage(language) :
            self.language = language
        else:
            self.language = Text.SupportedLanguages['English']['caption']

    def saveLanguage(self, language:str):
        """Save the chosen language in lang.txt at the self.languageFilePath location.
            Takes one parameter:
            - language as str (Use Text.SupportedLanguages['...'] to ensure compatibility).
        """
        if not(os.path.isfile(self.languageFilePath)) :
            open(self.languageFilePath,'x', encoding='utf-8')

        languageFile = open(self.languageFilePath, 'w', encoding='utf-8')
        languageFile.write(language)
        languageFile.close()


    def localisation(self,elementType:str,elementName:str,textType:str = 'caption'):
        return self._localisation[elementType][elementName][textType]

    def __init__(self,appDataFolderPath:str):

        self.languageFilePath = appDataFolderPath+Text.LanguageFileName
        self.loadLanguage()

        #English
        if self.language == Text.SupportedLanguages['English']['caption']:

            buttons = {
                'scene': {'caption':'Scene','toolTip':"Changes the scene and gives access to a new group of themes"},
                'newTheme': {'caption':'New theme','toolTip':"Add a new theme"},
                'addMusic': {'caption':'Add a music','toolTip':'Add a music to the selected theme'},
                'removeMusic': {'caption':'Remove a music','toolTip': 'Remove selected music from the selected theme'},
                'ok' : {'caption':'OK'},
                'cancel' : {'caption':'Cancel'},
                'addSample': {'caption':'Add an effect','toolTip':"Add a new effect button to the sampler"},
                'samplerEditButton': {'caption':'Edit','toolTip':'Activate edit mode to change a sound effect. Click againg to deactivate.'},
                'samplerDeleteButton': {'caption':'Delete','toolTip':'Activate delete mode to suppress sound effects. Click again to deactivate.'}
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
                'deleteTheme': {'caption':'Do you really want to delete this theme ?', 'title':'Delete '},
                'loadLibrary': {'caption':'Please load a valid DragonShout library !', 'title':'Invalid file'},
                'saveLanguage': {'caption':'Restart the application to apply changes','title':'Language changed'},
                'loadMedia': {'caption':"Player encountered an error relative to the loaded music. Check that your file is supported by your operating system.",'title':'Missing codec or invalid file'},
                'existingTheme': {'caption':'A theme with that name is already existing','title':'Existing theme'}
            }

            dialogBoxes = {
                'newTheme': {'caption':'New theme','toolTip':'Name the new theme','question':'Enter the theme name :'},
                'newSample': {'caption':'New sound effect','toolTip':'Choose a new sound effect','question':'Choose a new sound effect :'},
                'addMusic': {'caption':'Choose a track to add to this theme','toolTip':'Navigate the drive for a track to add to the theme'},
                'saveLibrary': {'title':'Save your work'},
                'newIcon': {'question':'Change the icon :'},
                'export': {'title':'Export your work'}
            }

            labels = {
                'scenes' : { 'caption': 'Scenes','toolTip':'List of musical scenes'},
                'playlistLabel' : {'caption': 'Select a theme to play','toolTip':'Shows the playlist of the selected theme'},
                'chooseThemeFirst': {'caption': 'Choose or create a theme first'},
                'colorScheme' : {'caption': 'Color :'}
            }

        #French
        if self.language == Text.SupportedLanguages['French']['caption']:
            buttons = {
                'scene': {'caption':'Scène','toolTip':"Change de scène et accède à un nouveau groupe de thèmes"},
                'newTheme': {'caption':'Nouveau thème','toolTip':"Ajoute un nouveau thème"},
                'addMusic': {'caption':'Ajouter une musique','toolTip':'Ajouter une piste musicale au thème sélectioné'},
                'removeMusic': {'caption':'Supprimer la musique','toolTip': 'Supprimer la musique choisie du thème sélectionné'},
                'ok' : {'caption':'OK'},
                'cancel' : {'caption':'Annuler'},
                'addSample': {'caption':'Ajouter un effet','toolTip':"Ajouter un nouveau bouton d'effet au sampler"},
                'samplerEditButton': {'caption':'Modifier','toolTip':'Active le mode édition pour modifier les effets sonores. Cliquer à nouveau pour désactiver'},
                'samplerDeleteButton': {'caption':'Supprimer','toolTip':'Active le mode suppression pour retirer les effets sonores. Cliquer à nouveau pour désactiver'}
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
                'deleteTheme': {'caption':'Voulez vous vraiment supprimer le thème ?', 'title':'Supprimer '},
                'loadLibrary': {'caption':'Veillez charger une librairie DragonShout valide !', 'title':'Fichier invalide'},
                'saveLanguage': {'caption':"Redémarrer l'application pour appliquer le changement.",'title':'Langue changée'},
                'loadMedia': {'caption':"Le lecteur a rencontré une erreur en chargeant la musique. Vérifier que le fichier est pris en charge par votre système d'exploitation.",'title':'Codec manquant ou fichier invalide'},
                'existingTheme': {'caption':'Un thème portant ce nom existe déjà','title':'Thème existant'}
            }

            dialogBoxes = {
                'newTheme': {'caption':'Nouveau thème','toolTip':'Nommer le nouveau thème','question':'Entrer le nom du thème :'},
                'newSample': {'caption':'Nouvel effet sonore','toolTip':'Choisir un nouvel effet sonore','question':'Sélectionner un nouvel effet sonore :'},
                'addMusic': {'caption':'Choisir un morceau à ajouter au thème','toolTip':"Parcours le disque à la recherche d'un morceau à ajouter au thème"},
                'saveLibrary': {'title':'Sauver votre travail'},
                'newIcon': {'question':"Changer l'icone :"},
                'export': {'title':'Exporter votre travail'}
            }

            labels = {
                'scenes' : { 'caption': 'Scènes','toolTip':'Liste des scènes musicales'},
                'playlistLabel' : {'caption': 'Sélectionne un thème à jouer ','toolTip':'Montre la liste de lecture du thème sélectionné'},
                'chooseThemeFirst': {'caption': "Il faut d'abord choisir ou créer un thème"},
                'colorScheme' : {'caption': 'Couleur :'}
            }


        self._localisation = {'buttons': buttons, 'menus': menus, 'menuEntries': menuEntries, 'messageBoxes': messageBoxes,
                                'labels': labels,'dialogBoxes': dialogBoxes}
