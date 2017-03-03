#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for the playlist's collection of widget used in the main window
#
#Application: DragonShout music sampler
#Last Edited: March 03rd 2017
#---------------------------------

import os

from classes.interface.Text import Text
from classes.library.Library import Library
from classes.library.Track import Track

from PyQt5 import Qt
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QFileDialog

class Playlist(QWidget):

    def __init__(self,text:Text):
        super().__init__()

        self.text = text
        self.tracks = []

        #Label of the tracklist
        playlistVerticalLayout = QVBoxLayout()
        self.label = QLabel(text.localisation('labels','playlistLabel','caption'))
        self.label.setAlignment(Qt.Qt.AlignCenter)
        playlistVerticalLayout.addWidget(self.label)

        #tracklist
        self.trackList = QListWidget()
        playlistVerticalLayout.addWidget(self.trackList)

        #Controls of the tracklist
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
        addButton.clicked.connect(lambda *args: self.addMusicToList())
        addButton.setEnabled(False)
        genericLayout.addWidget(addButton)
        self.addMusicButton = addButton

        #stop button
        stopButton = QPushButton()
        stopButton.setIcon(QIcon('ressources/interface/stop.png'))
        stopButton.setMaximumWidth(40)
        genericLayout.addWidget(stopButton)

        controlsWidget.setLayout(genericLayout)
        playlistVerticalLayout.addWidget(controlsWidget)

        self.setLayout(playlistVerticalLayout)

    def setList(self,text:str='', tracks:dict=None):
        """Update the tracklist with the provided list of tracks and
            sets the track list label to specified text
            Takes two parameters:
            - text as string
            - list of tracks as a dictionnary of track objects
        """
        self.label.setText(text)
        self.trackList.clear()
        self.tracks = tracks

        for track in tracks:
            self.trackList.addItem(track.name)

    def addMusicToList(self):
        """Calls a file dialog to choose a music to add to the tracklist.
            Takes no parameter.
        """
        filePath, ok = QFileDialog().getOpenFileName(self,self.text.localisation('dialogBoxes','addMusic','caption'),os.path.expanduser('~'),"*.mp3 *.wav *.ogg *.flac *.wma *.aiff *.m4a")
        if ok :
            name = QFileInfo(filePath).fileName()
            self.tracks.append(Track(name,filePath))
            self.trackList.addItem(name)
