#---------------------------------
#Author: Chappuis Anthony
#
#This class handle the music for the application. Uses two separate QMediaPlayers
#
#Application: DragonShout music sampler
#Last Edited: March 23th 2017
#---------------------------------

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QAudio


class MusicPlayer():

    def __init__(self, volume:int=100):

        self.volume = volume

        self.player1 = QMediaPlayer()
        self.player1.setAudioRole(QAudio.MusicRole)

        self.player2 = QMediaPlayer()
        self.player2.setAudioRole(QAudio.MusicRole)

    def changeMusic(self,media:QMediaContent):
        """Handle the change between two tracks using a fade-in/fade-out mechanism.
            Takes one parameter:
            - media as QMediaContent
        """
        player1State = self.player1.state()
        player2State = self.player2.state()

        #Both player are stopped
        if player1State == QMediaPlayer.StoppedState and player2State == QMediaPlayer.StoppedState :
            print('No player -> player 1')
            self.player1.setMedia(media)
            self.player1.setVolume(self.volume)
            self.player1.play()
        else:
            #Player 1 is running
            if self.player1.state() == QMediaPlayer.PlayingState :
                print('Player 1 -> player 2')
                self.player2.setMedia(media)
                self.player2.play()

                player1Volume = self.volume
                player2Volume = 0
                while player2Volume < self.volume :
                    self.player1.setVolume(player1Volume)
                    self.player2.setVolume(player2Volume)
                    player1Volume -= 1
                    player2Volume += 1

                self.player1.stop()

            #Player 2 is running
            elif self.player2.state() == QMediaPlayer.PlayingState :
                print('Player 2 -> Player 1')
                self.player1.setMedia(media)
                self.player1.play()

                player2Volume = self.volume
                player1Volume = 0
                while player1Volume < self.volume :
                    self.player1.setVolume(player1Volume)
                    self.player2.setVolume(player2Volume)
                    player1Volume += 1
                    player2Volume -= 1

                self.player2.stop()

    def stop(self):
        """Stop all media players.
            Takes no parameter.
        """
        self.player1.stop()
        self.player2.stop()

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
