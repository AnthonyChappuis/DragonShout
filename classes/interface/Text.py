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
                'test': "test",
                'iteration': "iteration"
            }
            menus = ''
            textBoxes = ''


        self._localisation = {'buttons': buttons, 'menus': menus, 'textBoxes': textBoxes}

    def localisation(self,textType:str,textName:str):
        return self._localisation[textType][textName]
