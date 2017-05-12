#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for the theme and its collection of buttons used in the themes widget
#
#Application: DragonShout music sampler
#Last Edited: Mai 07th 2017
#---------------------------------

from classes.interface import MainWindow

from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.Qt import Qt

class ThemeButtons(QWidget):

    DefaultThemeIcon = 'ressources/interface/defaultThemeIcon.png'

    def __init__(self, themeName:str, mainWindow:MainWindow, iconPath:str=''):
        super().__init__()

        self.mainWindow = mainWindow
        layout = QHBoxLayout()

        if iconPath == '':
            iconPath = ThemeButtons.DefaultThemeIcon

        #Theme button
        self.themeButton = QPushButton(themeName)
        self.themeButton.setIcon(QIcon(iconPath))
        self.themeButton.setIconSize(QSize(100,100))
        self.themeButton.setFlat(True)
        self.themeButton.clicked.connect(lambda *args: self.selectTheme(self.sender().text()))
        layout.addWidget(self.themeButton)

        #Edit button
        self.editButton = QPushButton('Edit')
        self.editButton.setMaximumWidth(50)
        self.editButton.clicked.connect(lambda *args: self.editThemeName(self.themeButton.text()))
        layout.addWidget(self.editButton)

        #Remove button
        self.removeButton = QPushButton('X')
        self.removeButton.setMaximumWidth(20)
        self.removeButton.clicked.connect(lambda *args: self.mainWindow.themes.deleteTheme(self.themeButton.text(),self))
        layout.addWidget(self.removeButton)

        self.setLayout(layout)

    def selectTheme(self,themeName:str):
        """Update the playlist with the music list of the selected theme.
            Takes one parameter:
            - themeName as string
        """
        theme = self.mainWindow.library.get_category(themeName)
        if theme :
            self.mainWindow.playlist.setList(themeName,theme.tracks)
            self.mainWindow.playlist.toggleSuppressButton()

    def editThemeName(self, themeName:str):
        """Change the name of a theme both in the UI and in the library.
            Takes one parameter:
            - themeName as string
        """
        newThemeName, ok = QInputDialog.getText(self,themeName,self.mainWindow.text.localisation('dialogBoxes','newTheme','question'))
        category = self.mainWindow.library.get_category(themeName)

        if ok and category:
            self.themeButton.setText(newThemeName)
            category.name = newThemeName

            if self.mainWindow.playlist.label.text() == themeName:
                self.mainWindow.playlist.label.setText(newThemeName)
