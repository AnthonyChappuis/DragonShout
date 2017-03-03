#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for storing all textes of the application
#It also manage which language is used when showing textes.
#
#Application: DragonShout music sampler
#Last Edited: March 03rd 2017
#---------------------------------

class Text:
    def __init__(self,language:str='english'):

        #English
        if language == 'english':

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
                'save' : { 'caption':'Save', 'toolTip': "Save your work"}
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
        if language == 'french':
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
                'save' : { 'caption':'Sauvegarder', 'toolTip': "Sauvegarder votre travail"}
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

    def localisation(self,elementType:str,elementName:str,textType:str = 'caption'):
        return self._localisation[elementType][elementName][textType]
