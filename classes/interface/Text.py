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
            }

            menuEntries = {
                'exit': { 'caption':'Exit', 'toolTip': "Exit the application"},
            }

            textBoxes = ''

        #French
        if language == 'french':
            buttons = ''

            menus =  {
                'files': {'caption':"Fichiers",'toolTip': 'Ceci est un widget <b>QWidget</b>'},
            }

            menuEntries = {
                'exit': { 'caption':'Quitter', 'toolTip':"Quitter l'application."},
            }

            textBoxes = ''


        self._localisation = {'buttons': buttons, 'menus': menus, 'menuEntries': menuEntries, 'textBoxes': textBoxes}

    def localisation(self,elementType:str,elementName:str,textType:str = 'caption'):
        return self._localisation[elementType][elementName][textType]
