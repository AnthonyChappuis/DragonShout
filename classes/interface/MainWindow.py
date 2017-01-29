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
from PyQt5.QtWidgets import QWidget, QApplication , QToolTip, QPushButton

class MainWindow(QtGui.QWindow):

    def __init__(self,application:QApplication):
        super().__init__()
        screen = application.desktop().screenGeometry()

        self.setGeometry(50, 50, screen.width(), screen.height())
        self.setTitle(APP_NAME)
        self.setIcon(QIcon('dragonShout.png'))

        text = Text('english')
        QToolTip.setFont(QFont('SansSerif', 10))

        #Creating status bar
        self.statusBar().showMessage('Ready')

        self.setGeometry(0, self.height()-self.height()/20, self.width(), self.height()/20)
        self.setWindowTitle('Statusbar')
        self.show()
