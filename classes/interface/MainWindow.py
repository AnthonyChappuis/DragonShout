#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for main window of the application
#
#Application: DragonShout music sampler
#Last Edited: September 13th 2016
#---------------------------------

from constants import *
from classes.interface.Text import Text

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp

class MainWindow(QMainWindow):

    def __init__(self,application:QApplication):
        super().__init__()
        screen = application.desktop().screenGeometry()

        self.setGeometry(50, 50, screen.width(), screen.height())
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon('dragonShout.png'))

        text = Text('english')

        #Creating status bar
        self.statusBar().showMessage('Ready')
        self.statusBar().setGeometry(0, self.height()-self.height()/20, self.width(), self.height()/20)

        #Defining menus actions
        exitAction = QAction(QIcon('exit.png'), text.localisation('menuEntries','exit','caption'), self)
        exitAction.setShortcut('Alt+F4')
        exitAction.setStatusTip(text.localisation('menuEntries','exit','toolTip'))
        exitAction.triggered.connect(qApp.quit)

        #Creating menu bar
        menuBar = self. menuBar()
        fileMenu = menuBar.addMenu(text.localisation('menus','files','caption'))
        fileMenu.addAction(exitAction)

        self.show()
