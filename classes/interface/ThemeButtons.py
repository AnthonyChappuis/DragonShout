#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for the theme and its collection of buttons used in the themes widget
#
#Application: DragonShout music sampler
#Last Edited: September 13th 2018
#---------------------------------

from classes.interface import MainWindow
from classes.interface.ThemeButtonDialogBox import ThemeButtonDialogBox

from classes. ressourcesFilepath import Stylesheets, Images

from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.Qt import Qt

class ThemeButtons(QWidget):

    def __init__(self, themeName:str, themeIconPath:str, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        layout = QHBoxLayout()

        #Verify if themeIconPath is a str item and defaults it if not.
        if themeIconPath == '' or not isinstance(themeIconPath, str) :
            themeIconPath = ThemeButtonDialogBox.DefaultThemeIconPath

        stylesheet = open(Stylesheets.themeButtons,'r',encoding='utf-8').read()

        #Theme button
        self.themeButton = QPushButton(themeName)
        self.themeIconPath = themeIconPath
        self.themeButton.setIcon(QIcon(self.themeIconPath))
        self.themeButton.setIconSize(QSize(100,100))
        self.themeButton.setStyleSheet(stylesheet)
        self.themeButton.clicked.connect(lambda *args: self.selectTheme(self.sender().text()))
        layout.addWidget(self.themeButton)

        #Edit button
        self.editButton = QPushButton(self.mainWindow.text.localisation('buttons','edit','caption'))
        self.editButton.setStyleSheet(stylesheet)
        self.editButton.clicked.connect(lambda *args: self.editTheme(self.themeButton.text()))
        layout.addWidget(self.editButton)

        #Remove button
        self.removeButton = QPushButton()
        self.removeButton.setIcon(QIcon(Images.deleteButtonIcon))
        self.removeButton.setStyleSheet(stylesheet)
        self.removeButton.setMinimumWidth(50)
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

    def editTheme(self, themeName:str):
        """Change the name of a theme both in the UI and in the library.
            Takes one parameter:
            - themeName as string
        """
        newThemeName, newThemeIconPath, ok = ThemeButtonDialogBox(self.mainWindow, self.themeButton.text(), self.themeIconPath).getItems()
        category = self.mainWindow.library.get_category(themeName)

        if ok and category:
            self.themeButton.setText(newThemeName)
            self.themeButton.setIcon(QIcon(newThemeIconPath))
            category.name = newThemeName
            category.iconPath = newThemeIconPath

            if self.mainWindow.playlist.label.text() == themeName:
                self.mainWindow.playlist.label.setText(newThemeName)
