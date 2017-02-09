#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for storing all textes of the application
#It also manage which language is used when showing textes.
#
#Application: DragonShout music sampler
#Last Edited: September 13th 2016
#---------------------------------

class Text:
    def __init__(self,language:str='english'):

        #English
        if language == 'english':

            buttons = {
                'scene': {'caption':'Scene','toolTip':"Changes the scene and gives access to a new group of themes"},
                'new_theme': {'caption':'New theme','toolTip':"Change the musical theme"}
            }

            menus = {
                'files': {'caption':"Files",'toolTip': 'This is a <b>QWidget</b> widget'},
                'options': {'caption':'Options','toolTip': 'Software options'}
            }

            menuEntries = {
                'exit': { 'caption':'Exit', 'toolTip': "Exit the application"},
                'language': { 'caption':'Language', 'toolTip': "Select the language of the application"},
                'save' : { 'caption':'Save', 'toolTip': "Save your work"}
            }

            textBoxes = ''

            dialogBoxes = {
                'newTheme': {'caption':'New theme','toolTip':'Name the new theme','question':'Enter the theme name :'}
            }

            labels = {
                'scenes' : { 'caption': 'Scenes','toolTip':'List of musical scenes'},
                'playlistLabel' : {'caption': 'Select a theme to play','toolTip':'Shows the playlist of the selected theme'}
            }

        #French
        if language == 'french':
            buttons = {
                'scene': {'caption':'Scène','toolTip':"Change de scène et accède à un nouveau groupe de thèmes"},
                'new_theme': {'caption':'Nouveau thème','toolTip':"Change le thème musical"}
            }

            menus =  {
                'files': {'caption':"Fichiers",'toolTip': 'Ceci est un widget <b>QWidget</b>'},
                'options': {'caption':'Options','toolTip': 'Options du programme'}
            }

            menuEntries = {
                'exit': { 'caption':'Quitter', 'toolTip':"Quitter l'application."},
                'language': { 'caption':'Langue', 'toolTip': "Sélectionner la langue de l'application"},
                'save' : { 'caption':'Sauvegarder', 'toolTip': "Sauvegarder votre travail"}
            }

            textBoxes = ''

            dialogBoxes = {
                'newTheme': {'caption':'Nouveau thème','toolTip':'Nommer le nouveau thème','question':'Entrer le nom du thème :'}
            }

            labels = {
                'scenes' : { 'caption': 'Scènes','toolTip':'Liste des scènes musicales'},
                'playlistLabel' : {'caption': 'Sélectionne un thème à jouer ','toolTip':'Montre la liste de lecture du thème sélectionné'}
            }


        self._localisation = {'buttons': buttons, 'menus': menus, 'menuEntries': menuEntries, 'textBoxes': textBoxes,
                                'labels': labels,'dialogBoxes': dialogBoxes}

    def localisation(self,elementType:str,elementName:str,textType:str = 'caption'):
        return self._localisation[elementType][elementName][textType]
