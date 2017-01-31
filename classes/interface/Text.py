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

            buttons = ''

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

            labels = {
                'scenes' : { 'caption': 'Scenes','toolTip':'List of musical scenes'}
            }

        #French
        if language == 'french':
            buttons = ''

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

            labels = {
                'scenes' : { 'caption': 'Scénes','toolTip':'Liste des scènes musicales'}
            }


        self._localisation = {'buttons': buttons, 'menus': menus, 'menuEntries': menuEntries, 'textBoxes': textBoxes,
                                'labels': labels}

    def localisation(self,elementType:str,elementName:str,textType:str = 'caption'):
        return self._localisation[elementType][elementName][textType]
