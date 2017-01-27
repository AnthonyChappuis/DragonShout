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
                'Files': {'caption':"Files",'toolTip': 'This is a <b>QWidget</b> widget'},
            }

            menus = ''

            textBoxes = ''

        #French
        if language == 'french':
            buttons = {
                'Files': {'caption':"Fichiers",'toolTip': 'Ceci est un widget <b>QWidget</b>'},
            }

            menus = ''

            textBoxes = ''


        self._localisation = {'buttons': buttons, 'menus': menus, 'textBoxes': textBoxes}

    def localisation(self,elementType:str,elementName:str,textType:str = 'caption'):
        return self._localisation[elementType][elementName][textType]
