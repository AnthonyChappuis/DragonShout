#---------------------------------
#Author: Chappuis Anthony
#
#Class responsible for the playlist's collection of widget used in the main window
#
#Application: DragonShout music sampler
#Last Edited: April 10th 2017
#---------------------------------

import os
import random

from classes.interface import MainWindow
from classes.library.Library import Library
from classes.library.Track import Track
from classes.multimedia.MusicPlayer import MusicPlayer

from PyQt5 import Qt
from PyQt5.QtCore import QFileInfo, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QFileDialog, QAbstractItemView

class Playlist(QWidget):

    def __init__(self,mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.tracks = []
        self.label = ''
        self.musicPlayer = MusicPlayer()

        #Label of the tracklist
        playlistVerticalLayout = QVBoxLayout()
        self.label = QLabel(self.mainWindow.text.localisation('labels','playlistLabel','caption'))
        self.label.setAlignment(Qt.Qt.AlignCenter)
        playlistVerticalLayout.addWidget(self.label)

        #tracklist
        self.trackList = QListWidget()
        self.trackList.setSelectionMode(QAbstractItemView.SingleSelection)
        playlistVerticalLayout.addWidget(self.trackList)

        #Controls of the tracklist
        controlsWidget = QWidget(self)
        genericLayout = QHBoxLayout()

        #play button
        playButton = QPushButton()
        playButton.setIcon(QIcon('ressources/interface/play.png'))
        playButton.setMaximumWidth(40)
        playButton.clicked.connect(lambda *args: self.playMusic())
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
        stopButton.clicked.connect(lambda *args: self.stopMusic())
        genericLayout.addWidget(stopButton)

        controlsWidget.setLayout(genericLayout)
        playlistVerticalLayout.addWidget(controlsWidget)

        self.setLayout(playlistVerticalLayout)

    def setList(self,text:str='', tracks:dict=None):
        """Update the tracklist with the provided list of tracks and
            sets the track list label to specified text. Also plays a track of the theme at random if
            theme selection occurs while the music player is active.
            Takes two parameters:
            - text as string
            - list of tracks as a dictionnary of track objects
        """
        self.label.setText(text)
        self.trackList.clear()
        self.tracks = tracks

        for track in tracks:
            self.trackList.addItem(track.name)

        self.addMusicButton.setEnabled(True)

        #Launch a random track if the music player is active.
        if self.musicPlayer.isPlaying():
            self.playMusicAtRandom()

    def addMusicToList(self):
        """Calls a file dialog to choose a music to add to the tracklist.
            Takes no parameter.
        """
        filesList, ok = QFileDialog().getOpenFileNames(self,self.mainWindow.text.localisation('dialogBoxes','addMusic','caption'),os.path.expanduser('~'),"*.mp3 *.wav *.ogg *.flac *.wma *.aiff *.m4a")
        if ok :
            for filePath in filesList :
                name = QFileInfo(filePath).fileName()
                self.tracks.append(Track(name,filePath))
                self.trackList.addItem(name)

    def reset(self):
        """Empty the playlist widget and reset the title label.
            Takes no parameter
        """
        self.label.setText(self.mainWindow.text.localisation('labels','playlistLabel','caption'))
        self.trackList.clear()
        self.addMusicButton.setEnabled(False)

    def playMusic(self):
        """Send the selected file to the music player.
            Takes no parameter.
        """
        if self.trackList.currentItem():
            found = False
            selectedItem = self.trackList.currentItem().text()

            for track in self.tracks :
                if track.name == selectedItem :
                    filepath = track.location
                    found = True

            if found:
                fileUrl = QUrl.fromLocalFile(filepath)
                media = QMediaContent(fileUrl)
                self.musicPlayer.changeMusic(media)

    def playMusicAtRandom(self):
        """Choose randomly a track to play.
            Takes no parameter
        """
        numberOfTracks = len(self.tracks)
        randomTrackNumber = random.randrange(0,numberOfTracks-1)

        self.trackList.setCurrentRow(randomTrackNumber)
        self.playMusic()

    def stopMusic(self):
        """Stop the music player.
            Takes no parameter
        """
        self.musicPlayer.stop()
