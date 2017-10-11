#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for the themes' collection of widget used in the main window
#
#Application: DragonShout music sampler
#Last Edited: May 19th 2017
#---------------------------------

from classes.interface import MainWindow
from classes.interface.ThemeButtons import ThemeButtons
from classes.interface.ThemeButtonDialogBox import ThemeButtonDialogBox

from PyQt5 import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QInputDialog,
    QHBoxLayout, QMessageBox)

class Themes(QWidget):

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.themeButtons = []

        #Main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.Qt.AlignHCenter)
        self.setLayout(self.mainLayout)

        #New theme button
        self.addNewThemeButton(self.mainLayout)

        #theme buttons layout
        self.themeButtonsLayout = QVBoxLayout()
        self.themeButtonsLayout.setAlignment(Qt.Qt.AlignHCenter)
        themeButtonsWidget = QWidget()
        themeButtonsWidget.setLayout(self.themeButtonsLayout)
        self.mainLayout.addWidget(themeButtonsWidget)

        for theme in self.mainWindow.library.categories:
            self.addTheme(theme.name)

        self.mainLayout.addStretch(1)

    def addNewThemeButton(self, mainLayout:QVBoxLayout):
        """Add a button to add a new theme to the given layout.
            Takes one parameter:
            - layout as QVBoxLayout object.
            Returns nothing
        """
        newThemeButton = QPushButton(self.mainWindow.text.localisation('buttons','newTheme','caption'))
        newThemeButton.clicked.connect(lambda *args: self.addTheme())
        self.mainLayout.addWidget(newThemeButton)


    def reset(self):
        """Used to reset the themes layout by removing each childrens.
            Takes no parameter.
            Returns nothing.
        """
        for i in reversed(range(self.themeButtonsLayout.count())):
            self.themeButtonsLayout.itemAt(i).widget().setParent(None)
            self.themeButtons = []

    def setThemes(self):
        """Used to create the GUI elements for all existing themes.
            Takes no parameter.
            Returns nothing.
        """
        self.reset()
        for theme in self.mainWindow.library.categories:
            themeButton = ThemeButtons(theme.name, theme.iconPath, self.mainWindow)
            self.themeButtonsLayout.addWidget(themeButton)
            self.themeButtons.append(themeButton)

    def addTheme(self):
        """Adds a new theme button to the theme main layout.
            Takes no parameter.
            Returns nothing.
        """
        ok = False

        themeName, themeIconPath, ok = ThemeButtonDialogBox(self.mainWindow).getItems()

        if ok :
            if themeName == '' or not isinstance(themeName, str):
                themeName = self.mainWindow.text.localisation('buttons','newTheme','caption')
            self.mainWindow.library.add_category(themeName,themeIconPath)

            #Theme widget
            themeButton = ThemeButtons(themeName, themeIconPath, self.mainWindow)
            self.themeButtons.append(themeButton)
            self.themeButtonsLayout.addWidget(themeButton)


    def deleteTheme(self, themeName:str, themeButtons:ThemeButtons):
        """Delete the theme both in the UI and in the library.
            Takes two parameter:
            - themeName as string
            - themeButtons object
            Returns nothing.
        """
        choice = QMessageBox(QMessageBox.Question,self.mainWindow.text.localisation('messageBoxes','deleteTheme','title')+themeName+' ?',
                                                    self.mainWindow.text.localisation('messageBoxes','deleteTheme','caption'),
                                                    QMessageBox.Yes | QMessageBox.No).exec()

        if choice == QMessageBox.Yes :
            category = self.mainWindow.library.get_category(themeName)

            if themeName == self.mainWindow.playlist.label.text():
                self.mainWindow.playlist.reset()

            if themeButtons in self.themeButtons :
                self.themeButtons.remove(themeButtons)

            if category :
                del category
                themeButtons.deleteLater()

    def toggleThemes(self, toggleType:bool):
        """Used to disable or enable the themeButtons.
            Takes one parameter:
            - toggleType as boolean.
            Returns nothing.
        """
        for theme in self.themeButtons :
            themeButton = theme.themeButton

            if toggleType == True :
                themeButton.setEnabled(True)
            elif toggleType == False :
                themeButton.setEnabled(False)
