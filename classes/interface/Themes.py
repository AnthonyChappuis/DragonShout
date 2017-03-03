#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for the themes' collection of widget used in the main window
#
#Application: DragonShout music sampler
#Last Edited: March 03rd 2017
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

            #Theme widget
            self.layout.addWidget(ThemeButtons(themeName, self.mainWindow))


    def deleteTheme(self, themeName:str, themeButtons:ThemeButtons):
        """Delete the theme both in the UI and in the library.
            Takes two parameter:
            - themeName as string
            - themeButtons object
        """
        choice = QMessageBox().question(self,self.mainWindow.text.localisation('messageBoxes','deleteTheme','title')+themeName+' ?',self.mainWindow.text.localisation('messageBoxes','deleteTheme','caption'))

        if choice == QMessageBox.Yes :
            category = self.mainWindow.library.get_category(themeName)

            if category :
                del category
                themeButtons.deleteLater()
