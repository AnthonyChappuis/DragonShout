#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for the playlist's collection of widget used in the main window
#
#Application: DragonShout music sampler
#Last Edited: September 13th 2016
#---------------------------------

from classes.interface.Text import Text
from classes.library.Library import Library

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton

class Playlist(QWidget):

    def __init__(self,text:Text):
        super().__init__()

        #Label of the currant playlist
        playlistVerticalLayout = QVBoxLayout()
        self.label = QLabel(text.localisation('labels','playlistLabel','caption'))
        self.label.setAlignment(Qt.Qt.AlignCenter)
        playlistVerticalLayout.addWidget(self.label)

        #Playlist of the selected theme
        self.trackList = QListWidget()
        playlistVerticalLayout.addWidget(self.trackList)

        #Controls of the playlist
        controlsWidget = QWidget(self)
        genericLayout = QHBoxLayout()

        #play button
        playButton = QPushButton()
        playButton.setIcon(QIcon('ressources/interface/play.png'))
        playButton.setMaximumWidth(40)
        genericLayout.addWidget(playButton)

        #add button
        addButton = QPushButton("+")
        addButton.setMaximumWidth(40)
        addButton.clicked.connect(lambda *args: self.addMusicToTheme())
        genericLayout.addWidget(addButton)

        #stop button
        stopButton = QPushButton()
        stopButton.setIcon(QIcon('ressources/interface/stop.png'))
        stopButton.setMaximumWidth(40)
        genericLayout.addWidget(stopButton)

        controlsWidget.setLayout(genericLayout)
        playlistVerticalLayout.addWidget(controlsWidget)

        self.setLayout(playlistVerticalLayout)

    def setTheme(self,themeName:str, tracks:dict=None):
        """Update the playlist with the music list of the selected theme
            Takes one parameter:
            - themeName as string
        """
        self.label.setText(themeName)
        self.trackList.clear()

        for track in tracks:
            self.trackList.addItem(track.name)
