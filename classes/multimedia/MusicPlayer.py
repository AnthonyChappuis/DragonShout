#---------------------------------
#Author: Chappuis Anthony
#
#This class handle the music for the application. Uses two separate QMediaPlayers
#
#Application: DragonShout music sampler
#Last Edited: October 05th 2017
#---------------------------------
from classes.interface import MainWindow

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QAudio
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

class MusicPlayer():

    FadeIn = 1
    FadeOut = -1
    MaxVolume = 100
    MinVolume = 0

    def __init__(self, mainWindow:MainWindow, volume:int=100):
        #Constants
        self.Pause = 50

        self.NoVolume = 0
        self.VolumeStep = 1

        self.InFadingTimer = QTimer()
        self.OutFadingTimer = QTimer()

        #variables
        self.volume = volume
        self.mainWindow = mainWindow

        self.player1 = QMediaPlayer()
        self.player1.setAudioRole(QAudio.MusicRole)
        self.player1.setVolume(self.NoVolume)
        self.player1.mediaStatusChanged.connect(lambda *args: self.handlePlayerSignals(self.player1))

        self.player2 = QMediaPlayer()
        self.player2.setAudioRole(QAudio.MusicRole)
        self.player2.setVolume(self.NoVolume)
        self.player2.mediaStatusChanged.connect(lambda *args: self.handlePlayerSignals(self.player2))


    def handlePlayerSignals(self, player:QMediaPlayer):
        """Check which signal is emmited by the player.
            Takes one parameter :
            - player as QMediaPlayer object.
        """
        #Media loaded in the Player
        if player.mediaStatus() == QMediaPlayer.LoadedMedia:
            player.play()
            self.fadeSound(player,MusicPlayer.FadeIn)
            self.mainWindow.playlist.initiateDurationBar(player.duration())

        #Player reached the end of the current media
        if player.mediaStatus() == QMediaPlayer.EndOfMedia:
            self.mainWindow.playlist.playNextMedia()

        #Player encountered an error relative to the loaded media
        if player.mediaStatus() == QMediaPlayer.InvalidMedia:
            QMessageBox(QMessageBox.Critical,self.mainWindow.text.localisation('messageBoxes','loadMedia','title'),self.mainWindow.text.localisation('messageBoxes','loadMedia','caption')).exec()

    def changeVolume(self, volume:int):
        """Change the volume of the MusicPlayer.
            Takes one parameter:
            - volume as int.
        """
        if volume > MusicPlayer.MaxVolume :
            volume = MusicPlayer.MaxVolume
        if volume < MusicPlayer.MinVolume :
            volume = MusicPlayer.MinVolume

        self.volume = volume
        self.player1.setVolume(self.volume)
        self.player2.setVolume(self.volume)


    def changeMusic(self,media:QMediaContent):
        """Handle the change between two tracks using a fade-in/fade-out mechanism.
            Takes one parameter:
            - media as QMediaContent
        """
        player1State = self.player1.state()
        player2State = self.player2.state()
        #Both player are stopped
        if player1State == QMediaPlayer.StoppedState and player2State == QMediaPlayer.StoppedState :
            self.player1.setMedia(media)
        else:
            #Player 1 is running
            if self.player1.state() == QMediaPlayer.PlayingState :
                self.player2.setMedia(media)
                self.fadeSound(self.player1,MusicPlayer.FadeOut)

            #Player 2 is running
            elif self.player2.state() == QMediaPlayer.PlayingState :
                self.player1.setMedia(media)
                self.fadeSound(self.player2,MusicPlayer.FadeOut)

    def fadeSound(self, player:QMediaPlayer, fadingType:int):
        """Defines if the fading action is a fade-In or a fade-out and call the corresponding timer and incrementOrDecrementVolume() function.
            Takes two parameters:
            - player as QMediaPlayer object.
            - fadingType as MusicPlayer.FadeIn or MusicPlayer.FadeOut constants
        """
        if fadingType == MusicPlayer.FadeIn :
            self.InFadingTimer.timeout.connect(lambda *args: self.incrementOrDecrementVolume(player,MusicPlayer.FadeIn))
            self.mainWindow.themes.toggleThemes(False)
            self.InFadingTimer.start(self.Pause)
        else:
            self.OutFadingTimer.timeout.connect(lambda *args: self.incrementOrDecrementVolume(player,MusicPlayer.FadeOut))
            self.mainWindow.themes.toggleThemes(False)
            self.OutFadingTimer.start(self.Pause)


    def incrementOrDecrementVolume(self, player:QMediaPlayer,fadingType:int):
        """Fades the sound of the given player according to the fading type and stop the fading timer once done.
            Takes two parameters:
            - player as QMediaPlayer object.
            - fadingType as MusicPlayer.FadeIn or MusicPlayer.FadeOut constant.

        """
        self.mainWindow.playlist.durationBar.setValue(player.volume())
        volume = player.volume()
        volume += self.VolumeStep*fadingType
        player.setVolume(volume)

        if (player.volume() >= self.volume) and (fadingType == MusicPlayer.FadeIn) :
            self.InFadingTimer.stop()
            self.InFadingTimer.timeout.disconnect()
            self.mainWindow.themes.toggleThemes(True)

        if (player.volume() <= self.NoVolume) and (fadingType == MusicPlayer.FadeOut) :
            self.OutFadingTimer.stop()
            player.setMedia(QMediaContent())
            player.stop()
            self.OutFadingTimer.timeout.disconnect()
            self.mainWindow.themes.toggleThemes(True)

    def stop(self):
        """Stop all media players.
            Takes no parameter.
        """
        if self.player1.state() == QMediaPlayer.PlayingState :
            self.fadeSound(self.player1,MusicPlayer.FadeOut)

        if self.player2.state() == QMediaPlayer.PlayingState :
            self.fadeSound(self.player2,MusicPlayer.FadeOut)

    def getCurrentMedia(self):
        """Returns the name of the track being played
            Takes no parameter.
        """
        player1State = self.player1.state()
        player2State = self.player2.state()

        if player1State == QMediaPlayer.PlayingState :
            return self.player1.currentMedia()
        elif player2State == QMediaPlayer.PlayingState :
            return self.player2.currentMedia()
        else :
            return False

    def isPlaying(self):
        """Returns true if one of the MediaPlayer is active and false in the contrary.
            Takes no Parameter.
        """
        player1State = self.player1.state()
        player2State = self.player2.state()

        if (player1State or player2State) == QMediaPlayer.PlayingState :
            return True
        else:
            return False
