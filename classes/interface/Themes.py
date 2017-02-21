#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for the themes' collection of widget used in the main window
#
#Application: DragonShout music sampler
#Last Edited: February 20th 2017
#---------------------------------

from classes.interface import MainWindow

from PyQt5 import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QInputDialog

class Themes(QWidget):

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.Qt.AlignHCenter)
        self.setLayout(self.layout)

        newThemeButton = QPushButton('+')
        newThemeButton.clicked.connect(lambda *args: self.addTheme())
        newThemeButton.setMaximumWidth(100)
        self.layout.addWidget(newThemeButton)

        for theme in self.mainWindow.library.categories:
            self.addTheme(theme.name)

    def addTheme(self):
        """Adds a new theme button to the theme layout.
            Takes no parameter.
        """
        themeName, ok = QInputDialog.getText(self,self.mainWindow.text.localisation('dialogBoxes','newTheme','caption'),self.mainWindow.text.localisation('dialogBoxes','newTheme','question'))

        if ok :
            if themeName == '':
                themeName = self.mainWindow.text.localisation('buttons','newTheme','caption')
            self.mainWindow.library.add_category(themeName)

            themeButton = QPushButton(themeName)
            themeButton.setMaximumWidth(100)
            themeButton.clicked.connect(lambda *args: self.selectTheme(self.sender().text()))
            self.layout.addWidget(themeButton)

    def selectTheme(self,themeName:str):
        """Update the playlist with the music list of the selected theme
            Takes one parameter:
            - themeName as string
        """
        theme = self.mainWindow.library.get_category(themeName)
        if theme :
            self.mainWindow.playlist.setList(themeName,theme.tracks)
            self.mainWindow.playlist.addMusicButton.setEnabled(True)
