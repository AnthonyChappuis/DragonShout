#---------------------------------
#Author: Chappuis Anthony
#
#This class handle the music for the application. Uses two separate QMediaPlayers
#
#Application: DragonShout music sampler
#Last Edited: March 23th 2017
#---------------------------------

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QAudio
from threading import Thread
import time

class MusicPlayer():

    def __init__(self, volume:int=50):

        self.volume = volume

        self.player1 = QMediaPlayer()
        self.player1.setAudioRole(QAudio.MusicRole)
        self.player1.mediaStatusChanged.connect(lambda *args: self.playWhenLoaded(self.player1))

        self.player2 = QMediaPlayer()
        self.player2.setAudioRole(QAudio.MusicRole)
        self.player2.mediaStatusChanged.connect(lambda *args: self.playWhenLoaded(self.player2))

        #Constants
        self.Pause = 0.05
        self.VolumeStep = 1
        self.NoVolume = 0

        self.FadeIn = 1
        self.FadeOut = 0

    def playWhenLoaded(self, player:QMediaPlayer):
        """Verify if the media is loaded and launch the player.
            Takes one parameter :
            - player as QMediaPlayer object.
        """
        if player.mediaStatus() == QMediaPlayer.LoadedMedia:
            player.play()
            Thread(target = self.fadeSound(player,self.FadeIn)).start()

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
            self.player1.setVolume(self.NoVolume)
        else:
            #Player 1 is running
            if self.player1.state() == QMediaPlayer.PlayingState :
                self.player2.setMedia(media)
                Thread(target = self.fadeSound(self.player1,self.FadeOut)).start()

            #Player 2 is running
            elif self.player2.state() == QMediaPlayer.PlayingState :
                self.player1.setMedia(media)
                Thread(target = self.fadeSound(self.player2,self.FadeOut)).start()

    def fadeSound(self, player:QMediaPlayer, fadingType:int):
        """Used to fade the volume of a mediaplayer from zero to MusicPlayer.volume and vice et versa.
            Takes two parameters:
            - player as QMediaPlayer object.
            - fadingType as MusicPlayer.FadeIn or MusicPlayer.FadeOut constants
        """
        if fadingType == self.FadeIn :
            #Wait the time the media is loading
            #while player.mediaStatus() == QMediaPlayer.LoadingMedia :
            #Play the media and fade the volume from 0
            volume = self.NoVolume
            while volume < self.volume :
                volume += self.VolumeStep
                player.setVolume(volume)
                time.sleep(self.Pause)
        else:
            #fade the volume to 0 and stop the player
            volume = player.volume()
            while volume > self.NoVolume :
                volume -= self.VolumeStep
                player.setVolume(volume)
                time.sleep(self.Pause)

            #Clears the player from any media shen stopping
            player.setMedia(QMediaContent())
            player.stop()

    def stop(self):
        """Stop all media players.
            Takes no parameter.
        """
        Thread(target = self.fadeSound(self.player1,self.FadeOut)).start()
        Thread(target = self.fadeSound(self.player2,self.FadeOut)).start()

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
