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

        language = "english"
        text = Text()
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        button = QPushButton(text.localisation('buttons','test'), self)
        button.setToolTip('This is a <b>QPushButton</b> widget')
        button.resize(button.sizeHint())
        button.move(50, 50)
