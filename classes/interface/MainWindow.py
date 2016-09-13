from constants import *
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QApplication , QToolTip

class MainWindow(QWidget):

    def __init__(self,application:QApplication):
        super().__init__()
        screen = application.desktop().screenGeometry()

        self.resize(screen.width(),screen.height())
        self.move(0,0)
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon('dragonShout.png'))

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        button = QPushButton('Button', self)
        button.setToolTip('This is a <b>QPushButton</b> widget')
        button.resize(button.sizeHint())
        button.move(50, 50)
