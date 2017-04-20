#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for the themes' collection of widget used in the main window
#
#Application: DragonShout music sampler
#Last Edited: April 20th 2017
#---------------------------------

from classes.interface import MainWindow
from classes.interface.ThemeButtons import ThemeButtons

from PyQt5 import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QInputDialog,
    QHBoxLayout, QMessageBox)

class Themes(QWidget):

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.themeButtons = []
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addStretch(1)
        self.mainLayout.setAlignment(Qt.Qt.AlignHCenter)
        self.setLayout(self.mainLayout)

        self.addNewThemeButton(self.mainLayout)

        self.themeButtonsLayout = QVBoxLayout()
        self.themeButtonsLayout.setAlignment(Qt.Qt.AlignHCenter)
        themeButtonsWidget = QWidget()
        themeButtonsWidget.setLayout(self.themeButtonsLayout)
        self.mainLayout.addWidget(themeButtonsWidget)

        for theme in self.mainWindow.library.categories:
            self.addTheme(theme.name)

    def addNewThemeButton(self, mainLayout:QVBoxLayout):
        """Add a button to add a new theme to the given layout.
            Takes one parameter:
            - layout as QVBoxLayout object.
        """
        newThemeButton = QPushButton('+')
        newThemeButton.clicked.connect(lambda *args: self.addTheme())
        newThemeButton.setMaximumWidth(100)
        self.mainLayout.addWidget(newThemeButton)


    def reset(self):
        for i in reversed(range(self.themeButtonsLayout.count())):
            self.themeButtonsLayout.itemAt(i).widget().setParent(None)
            self.themeButtons = []

    def setThemes(self):
        """Used to create the GUI elements for all existing themes.
            Takes no parameter.
        """
        self.reset()
        for theme in self.mainWindow.library.categories:
            themeButton = ThemeButtons(theme.name,self.mainWindow)
            self.themeButtonsLayout.addWidget(themeButton)
            self.themeButtons.append(themeButton)

    def addTheme(self):
        """Adds a new theme button to the theme main layout.
            Takes no parameter.
        """
        themeName, ok = QInputDialog.getText(self,self.mainWindow.text.localisation('dialogBoxes','newTheme','caption'),self.mainWindow.text.localisation('dialogBoxes','newTheme','question'))

        if ok :
            if themeName == '':
                themeName = self.mainWindow.text.localisation('buttons','newTheme','caption')
            self.mainWindow.library.add_category(themeName)

            #Theme widget
            themeButton = ThemeButtons(themeName, self.mainWindow)
            self.themeButtons.append(themeButton)
            self.themeButtonsLayout.addWidget(themeButton)


    def deleteTheme(self, themeName:str, themeButtons:ThemeButtons):
        """Delete the theme both in the UI and in the library.
            Takes two parameter:
            - themeName as string
            - themeButtons object
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
