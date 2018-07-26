# DragonShout
Music sampler for Tabletop RPG

The project provides a simple music player and a sound effect sampler for table top role playing games. It provides a simple way to regroup
songs by themes or ambiance and a quick way to switch from one theme to another without interuption (fade in/ fade out mechanism).

The musical themes are symbolized by dedicated set of buttons that can be customized with name and icons. Each track of a theme are displayed on a playlist showing which one is being played. The progress of a song is show on a progress bar.

The sound effects are accessible by using dedicated buttons. That grants the user with the possibility to quickly start or stop independently each effect. The interface also show which effect is being played for easier recognition. Each effect can also be customized whith its own icon.

Both features, music and effect players, own a separated volume control to help the user armonized them.

The goals are:
- To keep the players immersed in the game by providing a continuous and consistant musical background.
- To have transitions between tracks and theme being as transparent as possible.
- To give the game master quick access to musical themes.
- To offer to the game master a tool to immerse player even more in the story thanks to judiciously placed sound effects.

The last used technologies are:
- Python 3.6.6
- PyQt 5.11.2
- SIP 4.19.8

Note:
- Installing libqt5multimedia5-plugins might be necessary to use sources with your system if you obtain :
 "defaultServiceProvider::requestService(): no service found for - "org.qt-project.qt.mediaplayer"" error.
- Qt Media Player used in this software is not compatible with FLAC music format at the moment.
