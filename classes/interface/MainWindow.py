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

class MainWindow(QWidget):

    def __init__(self,application:QApplication):
        super().__init__()
        screen = application.desktop().screenGeometry()

        self.resize(screen.width(),screen.height())
        self.move(0,0)
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon('dragonShout.png'))

        text = Text('french')
        QToolTip.setFont(QFont('SansSerif', 10))


        button = QPushButton(text.localisation('buttons','test','caption'), self)
        button.setToolTip(text.localisation('buttons','test','toolTip'))
        button.resize(button.sizeHint())
        button.move(50, 50)
