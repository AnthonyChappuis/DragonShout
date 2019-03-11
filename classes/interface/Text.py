#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for storing all textes of the application
#It also manage which language is used when showing textes.
#
#Application: DragonShout music sampler
#Last Edited: October 01st 2018
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
                'samplerDeleteButton': {'caption':'Delete','toolTip':'Activate delete mode to suppress sound effects. Click again to deactivate.'},
                'edit': {'caption':'Edit'},
                'close': {'caption':'Close'},
                'export': {'caption':'Export'},
                'import': {'caption':'Import'},
                'showHide': {'caption':'Show/Hide'}
            }

            menus = {
                'files': {'caption':"Files",'toolTip': 'This is a <b>QWidget</b> widget'},
                'options': {'caption':'Options','toolTip': 'Software options'}
            }

            menuEntries = {
                'exit': { 'caption':'Exit', 'toolTip': "Exit the application"},
                'language': { 'caption':'Language', 'toolTip': "Select the language of the application"},
                'save' : { 'caption':'Save', 'toolTip': "Save your work"},
                'load' : {'caption':'Load', 'toolTip': "Load an existing library"},
                'export' : {'caption':'Export','toolTip': "Stock your work inside an archive in order to export it to another computer."},
                'import' : {'caption':'Import','toolTip': "Import an archive which contains the work files coming from another computer."}
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
                'export': {'title':'Export your work', 'question': 'Choose a destination directory and name for the archive:'},
                'import': {'title':'Import a work environement','question':'Choose the file or destination:'}
            }

            labels = {
                'scenes' : { 'caption': 'Scenes','toolTip':'List of musical scenes'},
                'playlistLabel' : {'caption': 'Select a theme to play','toolTip':'Shows the playlist of the selected theme'},
                'chooseThemeFirst': {'caption': 'Choose or create a theme first'},
                'colorScheme' : {'caption': 'Color :'},
                'archiveFilePathLabel' : {'caption': 'Archive file:'}
            }

            logs = {
                'exportStart' : { 'caption': "Export begins."},
                'importStart' : {'caption': "Import begins."},
                'archiveCreation': {'caption': 'Creating archive file: '},
                'playlist': {'caption': 'Exporting themes and their playlists.'},
                'inTheme': {'caption': "Theme: "},
                'sampler': {'caption': 'Exporting sound effects'},
                'file': {'caption':'File: '},
                'exportSuccess': {'caption': 'Export successful.'},
                'importSuccess': {'caption': 'Import successful.'},
                'fileExists': {'caption': 'The file already exists, choose a different file name.'},
                'error': {'caption': 'An error occured, cleaning temporary files.'},
                'wrongFile': {'caption': 'Selected file is not compatible.'},
                'archiveOpening': {'caption': "Archive opening."},
                'extraction': {'caption': 'Extraction: '},
                'themesImport': {'caption': "Importing themes and their playlists."},
                'effectsImport': {'caption': "Importing effects."},
                'movingFiles': {'caption': "Moving files to destination folder."},
                'themesMoved': {'caption': "Themes loaded and moved to "},
                'effectsMoved': {'caption': "Sound effects loaded and moved to "},
                'addThemeIcon': {'caption': "Icon added: "}
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
                'samplerDeleteButton': {'caption':'Supprimer','toolTip':'Active le mode suppression pour retirer les effets sonores. Cliquer à nouveau pour désactiver'},
                'edit': {'caption':'Modifier'},
                'close': {'caption':'Fermer'},
                'export': {'caption':'Exporter'},
                'import': {'caption':'Importer'},
                'showHide': {'caption':'Afficher/Masquer'}
            }

            menus =  {
                'files': {'caption':"Fichiers",'toolTip': 'Ceci est un widget <b>QWidget</b>'},
                'options': {'caption':'Options','toolTip': 'Options du programme'}
            }

            menuEntries = {
                'exit': { 'caption':'Quitter', 'toolTip':"Quitter l'application."},
                'language': { 'caption':'Langue', 'toolTip': "Sélectionner la langue de l'application"},
                'save' : { 'caption':'Sauvegarder', 'toolTip': "Sauvegarder votre travail"},
                'load' : {'caption':'Charger', 'toolTip': "Charger une librairie existante"},
                'export' : {'caption':'Exporter','toolTip': "Stock votre travail dans une archive pour l'exporter vers un autre ordinateur."},
                'import' : {'caption':'Importer','toolTip': "Importe une archive contenant les fichiers de travail en provenance d'un autre ordinateur."}
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
                'export': {'title':'Exporter votre travail', 'question': "Choisir un dossier de destination pour l'archive:"},
                'import': {'title':'Importer un environement de travail','question':'Choisir le fichier ou la destination:'}
            }

            labels = {
                'scenes' : { 'caption': 'Scènes','toolTip':'Liste des scènes musicales'},
                'playlistLabel' : {'caption': 'Sélectionne un thème à jouer ','toolTip':'Montre la liste de lecture du thème sélectionné'},
                'chooseThemeFirst': {'caption': "Il faut d'abord choisir ou créer un thème"},
                'colorScheme' : {'caption': 'Couleur :'},
                'archiveFilePathLabel' : {'caption': "Fichier archive:"}
            }

            logs = {
                'exportStart' : { 'caption': "Début de l'exportation."},
                'importStart' : {'caption': "Début de l'importation."},
                'archiveCreation': {'caption': "Création du fichier d'archive: "},
                'playlist': {'caption': 'Export des thèmes et de leurs listes de lecture.'},
                'inTheme': {'caption': "Thème: "},
                'sampler': {'caption': 'Export des effets sonores.'},
                'file': {'caption':'Fichier: '},
                'exportSuccess': {'caption': 'Exportation réussie.'},
                'importSuccess': {'caption': 'Importation réussie.'},
                'fileExists': {'caption': 'Le fichier existe déjà, choisissez un autre nom de fichier.'},
                'error': {'caption': 'Une erreure est survenue, nettoyage des fichiers temporaires.'},
                'wrongFile': {'caption': "le fichier sélectionné n'est pas compatible."},
                'archiveOpening': {'caption': "Ouverture de l'archive."},
                'extraction': {'caption': 'Extraction: '},
                'themesImport': {'caption': "Import des thèmes et de leurs listes de lecture."},
                'effectsImport': {'caption': "Import des effets sonores."},
                'movingFiles': {'caption': "Place les fichiers dans le dossier de destination."},
                'themesMoved': {'caption': "Thèmes chargés et placés dans "},
                'effectsMoved': {'caption': "Effets sonores chargés et placés dans "},
                'addThemeIcon': {'caption': "Icon ajouté: "}
            }


        self._localisation = {'buttons': buttons, 'menus': menus, 'menuEntries': menuEntries, 'messageBoxes': messageBoxes,
                                'labels': labels,'dialogBoxes': dialogBoxes, 'logs': logs}
