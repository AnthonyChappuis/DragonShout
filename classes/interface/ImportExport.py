#---------------------------------
#Author: Chappuis Anthony
#
#Two Pop-up windows that manage import/export feature
#
#Application: DragonShout music sampler
#Last Edited: October 04th 2018
#---------------------------------
import os
import tarfile
import traceback
import shutil
from pathlib import Path

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QTextEdit,
                            QProgressBar, QFileDialog)
from PyQt5.QtGui import QIcon, QGuiApplication
from PyQt5.QtCore import QStandardPaths, QCoreApplication

from classes.interface import MainWindow
from classes.interface.SoundEffect import SoundEffect
from classes.library.Track import Track

from classes.ressourcesFilepath import Stylesheets, Images

class ImportExport():
    ArchiveThemesFolderName = 'themes'
    ArchiveSamplesFolderName = 'soundEffects'
    ExtractionDirectoryName = 'extraction'
    TempExtension = '.default'
    ArchiveFileExtension = '.dsa'
    themeIconID = '.themeIcon'

    Border1 = '********************************************************'
    Border2 = '--------------------------------------------------------'
    WarningBorder = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    BlankLine = ''

    def __init__(self):
        #Directory paths
        self.tempDirectoryPath = Path(MainWindow.MainWindow.AppDataFolder)/ImportExport.ExtractionDirectoryName

        #Windows dimensions
        screen = QGuiApplication.primaryScreen()
        screenGeometry = screen.geometry()

        self.width = screenGeometry.width()*1/3
        self.height = screenGeometry.height()*1/2

        #ColorIDs and relative stylesheets
        self.styleSheetsVsIDs = []

        self.styleSheetsVsIDs.append([Stylesheets.effectButtons,'U'])
        self.styleSheetsVsIDs.append([Stylesheets.redEffectButtons,'R'])
        self.styleSheetsVsIDs.append([Stylesheets.yellowEffectButtons,'Y'])
        self.styleSheetsVsIDs.append([Stylesheets.greyEffectButtons,'G'])
        self.styleSheetsVsIDs.append([Stylesheets.purpleEffectButtons,'P'])
        self.styleSheetsVsIDs.append([Stylesheets.blueEffectButtons,'B'])

    def getStylesheet(self, colorID:str):
        """Search the styleSheetsVsIDs table for the styleSheet relative to the given colorID.
            Defaults to the first colorID in case of no match.
            Takes one parameter:
            - colorID as str.
            Returns:
            - styleSheet as str.
        """
        stylesheet = self.styleSheetsVsIDs[0][0]

        for matchTableRow in self.styleSheetsVsIDs:
            if matchTableRow[1] == colorID :
                stylesheet = matchTableRow[0]

        return stylesheet

    def getColorID(self, styleSheet:str):
        """Searche the styleSheetsVsIDs table for the colorID relative to the given styleSheet.
            Defaults to the first styleSheet in case of no match.
            Takes one parameter:
            - styleSheet as str.
            Returns:
            - colorID as str.
        """
        colorID = self.styleSheetsVsIDs[0][1]

        for matchTableRow in self.styleSheetsVsIDs:
            if matchTableRow[0] == styleSheet:
                colorID = matchTableRow[1]

        return colorID

class ExportDialogBox(QDialog):

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.archiveFilePath = Path(QStandardPaths.locate(QStandardPaths.HomeLocation, '', QStandardPaths.LocateDirectory))

        #Window dimensions
        self.setMinimumWidth(ImportExport().width)
        self.setMinimumHeight(ImportExport().height)

        #window title and icon
        self.setWindowIcon(QIcon(Images.applicationIcon))
        self.setWindowTitle(self.mainWindow.text.localisation('dialogBoxes','export','title'))

        styleSheet = open(Stylesheets.globalStyle,'r', encoding='utf-8').read()
        self.setStyleSheet(styleSheet)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        #File dialog
        layout = QHBoxLayout()
        fileDialogWidget = QWidget()
        fileDialogWidget.setLayout(layout)

        fileLabel = QLabel(self.mainWindow.text.localisation('labels','archiveFilePathLabel','caption'))
        layout.addWidget(fileLabel)

        self.archiveFileSelectButton = QPushButton('...')
        self.archiveFileSelectButton.clicked.connect(lambda *args: self.getNewFilePath())
        layout.addWidget(self.archiveFileSelectButton)

        #Progress Bar
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)

        #text edit
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        #export button
        self.exportButton = QPushButton(self.mainWindow.text.localisation('buttons','export','caption'))
        self.exportButton.setEnabled(False)
        self.exportButton.clicked.connect(lambda *args: self.export())

        #close button
        self.closeButton = QPushButton(self.mainWindow.text.localisation('buttons','close','caption'))
        self.closeButton.clicked.connect(lambda *args: self.close())

        #Main layout widgets
        self.mainLayout.addWidget(fileDialogWidget)
        self.mainLayout.addWidget(self.progressBar)
        self.mainLayout.addWidget(self.textEdit)
        self.mainLayout.addWidget(self.exportButton)
        self.mainLayout.addWidget(self.closeButton)

    def addLogEntry(self, entry:str):
        """Adds a line to the text edit with given text.
            Takes one parameter:
            - entry as string.
            Returns nothing.
        """
        self.textEdit.append(entry)

    def getNewFilePath(self):
        """Opens a filesystem dialog to choose a folder and filename for the archive.
            Takes no parameter.
            Returns nothing.
        """
        archiveFileDialog = QFileDialog()
        archiveFileDialog.setAcceptMode(QFileDialog.AcceptSave)

        rawFilepath, ok = archiveFileDialog.getSaveFileName(self,self.mainWindow.text.localisation('dialogBoxes','export','question'),os.path.expanduser(self.archiveFilePath),ImportExport.ArchiveFileExtension)

        if ok :
            filepath = Path(rawFilepath)

            if filepath.suffix != ImportExport.ArchiveFileExtension :
                filepath = filepath.with_suffix(ImportExport.ArchiveFileExtension)

            self.archiveFilePath = filepath
            self.archiveFileSelectButton.setText(filepath.name)
            self.exportButton.setEnabled(True)

    def resetProgressBar(self):
        """Reset progress bar by gathering file number and setting it's min/max values and progress steps.
            Takes no parameter.
            Returns nothing.
        """
        trackNumber = 0
        effectNumber = 0

        for category in self.mainWindow.library.categories :
            trackNumber += len(category.tracks)

        effectNumber = self.mainWindow.sampler.countEffects()

        self.progressBar.reset()
        self.progressBar.setRange(0,trackNumber+effectNumber)
        self.progressBar.setValue(0)

    def bumpProgressBar(self):
        """Bump the value of the progress bar.
            Takes no parameter.
            Returns nothing.
        """
        self.progressBar.setValue(self.progressBar.value()+1)

    def toggleControls(self):
        """Enable or disable UI buttons during export.
            Takes no parameter.
            Returns nothing.
        """
        if self.closeButton.isEnabled() :
            self.closeButton.setEnabled(False)
        else:
            self.closeButton.setEnabled(True)

        if self.exportButton.isEnabled() :
            self.exportButton.setEnabled(False)
        else:
            self.exportButton.setEnabled(True)

        if self.archiveFileSelectButton.isEnabled() :
            self.archiveFileSelectButton.setEnabled(False)
        else:
            self.archiveFileSelectButton.setEnabled(True)

    def export(self):
        """Used to export library and 'atttached' sound files as an archive that can be transfered to another computer and/or operating system. Use gzip compression module.
            Takes no parameter.
            Returns nothing.
        """

        self.textEdit.clear()
        self.resetProgressBar()
        self.toggleControls()

        try:
            archiveFilePath = self.archiveFilePath

            #Create archive
            archive = tarfile.open(archiveFilePath.resolve(),'x:gz')
            self.addLogEntry(self.mainWindow.text.localisation('logs','archiveCreation','caption')+archiveFilePath.name)
            self.addLogEntry(ImportExport.BlankLine)

            self.addLogEntry(ImportExport.Border1)
            self.addLogEntry(self.mainWindow.text.localisation('logs','exportStart','caption'))
            self.addLogEntry(ImportExport.Border1)
            self.addLogEntry(ImportExport.BlankLine)

            QCoreApplication.processEvents()

            #Archive the themes and their playlists
            #themes folder defined by category name

            self.addLogEntry(ImportExport.Border2)
            self.addLogEntry(self.mainWindow.text.localisation('logs','playlist','caption'))
            self.addLogEntry(ImportExport.Border2)
            self.addLogEntry(ImportExport.BlankLine)

            for theme in self.mainWindow.library.categories:
                self.addLogEntry(self.mainWindow.text.localisation('logs','inTheme','caption')+theme.name)
                self.addLogEntry(ImportExport.Border2)
                self.addLogEntry(ImportExport.BlankLine)
                subFolderName = theme.name

                #filling theme folder with given tracks
                for track in theme.tracks:
                    archive.add(track.location,ImportExport.ArchiveThemesFolderName+'/'+subFolderName+'/'+track.name)
                    self.addLogEntry(self.mainWindow.text.localisation('logs','file','caption')+track.location)
                    self.bumpProgressBar()
                    QCoreApplication.processEvents()

                self.addLogEntry(ImportExport.BlankLine)

                #Adding theme icon
                iconPath = Path(theme.iconPath)
                archive.add(iconPath.resolve(),ImportExport.ArchiveThemesFolderName+'/'+subFolderName+'/'+iconPath.name+ImportExport.themeIconID)
                self.addLogEntry(self.mainWindow.text.localisation('logs','addThemeIcon','caption')+iconPath.name)
                self.addLogEntry(ImportExport.BlankLine)

            self.addLogEntry(ImportExport.Border2)
            self.addLogEntry(self.mainWindow.text.localisation('logs','sampler','caption'))
            self.addLogEntry(ImportExport.Border2)
            self.addLogEntry(ImportExport.BlankLine)

            #Archive the sound effects from the sampler
            for row in self.mainWindow.sampler.sampleButtons:
                for sampleButton in row :
                    buttonCoordinatesID = str(sampleButton.coordinates[0])+str(sampleButton.coordinates[1])
                    typeFolder = str(sampleButton.buttonType)

                    #user defined sound effects
                    if sampleButton.buttonType == SoundEffect.SOUNDEFFECTBUTTON :

                        colorID = ImportExport().getColorID(sampleButton.styleSheetPath)

                        sampleFilepath = Path(sampleButton.filepath)
                        endName = buttonCoordinatesID+colorID+sampleFilepath.name
                        self.addLogEntry(self.mainWindow.text.localisation('logs','file','caption')+str(sampleFilepath.resolve()))
                        archive.add(sampleFilepath.resolve(),ImportExport.ArchiveSamplesFolderName+'/'+typeFolder+'/'+endName)
                    #default buttons without effects
                    elif sampleButton.buttonType == SoundEffect.NEWEFFECTBUTTON :
                        endName = buttonCoordinatesID+ImportExport.TempExtension
                        defaultButtonTempPath = Path(MainWindow.MainWindow.AppDataFolder+endName)
                        defaultButtonTempPath.touch() #temp file to add to the archive
                        archive.add(defaultButtonTempPath.resolve(),ImportExport.ArchiveSamplesFolderName+'/'+typeFolder+'/'+endName)
                        defaultButtonTempPath.unlink() #remove the temp file
                    #Any other cases stops the export and triggers clean-up actions
                    else:
                        raise Exception

                    self.bumpProgressBar()

            self.addLogEntry(ImportExport.BlankLine)

            archive.close()

            self.addLogEntry(ImportExport.Border1)
            self.addLogEntry(self.mainWindow.text.localisation('logs','exportSuccess','caption'))
            self.addLogEntry(ImportExport.Border1)
            QCoreApplication.processEvents()

        except FileExistsError:
            self.addLogEntry(ImportExport.WarningBorder)
            self.addLogEntry(self.mainWindow.text.localisation('logs','fileExists','caption'))
            self.addLogEntry(ImportExport.WarningBorder)
            QCoreApplication.processEvents()

        except Exception as e:
            self.addLogEntry(ImportExport.WarningBorder)
            self.addLogEntry(self.mainWindow.text.localisation('logs','error','caption'))
            self.addLogEntry(ImportExport.WarningBorder)
            self.addLogEntry(ImportExport.BlankLine)
            QCoreApplication.processEvents()

            #Clean archive
            if 'archive' in locals():
                archive.close()
                Path.unlink(archiveFilePath)

            #Clean temp files
            workFolder = Path(MainWindow.MainWindow.AppDataFolder)
            for child in workFolder.iterdir():
                if child.name.endswith(ImportExport.TempExtension):
                    child.unlink()

            self.addLogEntry(traceback.format_exc())

        self.toggleControls()

class ImportDialogBox(QDialog):

    ArchiveType = 0
    DestinationType = 1

    def __init__(self, mainWindow:MainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.archiveFilePath = Path(QStandardPaths.locate(QStandardPaths.HomeLocation, '', QStandardPaths.LocateDirectory))
        self.destinationPath = self.archiveFilePath

        #Window dimensions
        self.setMinimumWidth(ImportExport().width)
        self.setMinimumHeight(ImportExport().height)

        #window title and icon
        self.setWindowIcon(QIcon(Images.applicationIcon))
        self.setWindowTitle(self.mainWindow.text.localisation('dialogBoxes','import','title'))

        styleSheet = open(Stylesheets.globalStyle,'r', encoding='utf-8').read()
        self.setStyleSheet(styleSheet)

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        #Archive file dialog
        layout = QHBoxLayout()
        archiveFileDialogWidget = QWidget()
        archiveFileDialogWidget.setLayout(layout)

        fileLabel = QLabel(self.mainWindow.text.localisation('labels','archiveFilePathLabel','caption'))
        layout.addWidget(fileLabel)

        self.archiveFileSelectButton = QPushButton('...')
        self.archiveFileSelectButton.clicked.connect(lambda *args: self.getNewPath(ImportDialogBox.ArchiveType))
        layout.addWidget(self.archiveFileSelectButton)

        #Destination filedialog
        layout = QHBoxLayout()
        destinationDialogWidget = QWidget()
        destinationDialogWidget.setLayout(layout)

        fileLabel = QLabel('Destination')
        layout.addWidget(fileLabel)

        self.destinationSelectButton = QPushButton(self.destinationPath.name)
        self.destinationSelectButton.clicked.connect(lambda *args: self.getNewPath(ImportDialogBox.DestinationType))
        layout.addWidget(self.destinationSelectButton)

        #Progress Bar
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)

        #text edit
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        #Import button
        self.importButton = QPushButton(self.mainWindow.text.localisation('buttons','import','caption'))
        self.importButton.setEnabled(False)
        self.importButton.clicked.connect(lambda *args: self.importArchive())

        #Close button
        self.closeButton = QPushButton(self.mainWindow.text.localisation('buttons','close','caption'))
        self.closeButton.clicked.connect(lambda *args: self.close())

        #Main layout widgets
        self.mainLayout.addWidget(archiveFileDialogWidget)
        self.mainLayout.addWidget(destinationDialogWidget)
        self.mainLayout.addWidget(self.progressBar)
        self.mainLayout.addWidget(self.textEdit)
        self.mainLayout.addWidget(self.importButton)
        self.mainLayout.addWidget(self.closeButton)

    def getNewPath(self, fileType:int):
        """Opens a filesystem dialog to choose a filepath for the archive or destination.
            Takes one parameter:
            - fileType as either ImportDialogBox.ArchiveType or ImportDialogBox.DestinationType.
            Returns nothing.
        """
        archiveFileDialog = QFileDialog()

        if fileType == ImportDialogBox.ArchiveType:
            rawFilepath, ok = archiveFileDialog.getOpenFileName(self,self.mainWindow.text.localisation('dialogBoxes','export','question'),os.path.expanduser(self.archiveFilePath))

            if ok :
                filepath = Path(rawFilepath)
                self.archiveFilePath = filepath
                self.archiveFileSelectButton.setText(filepath.name)

        elif fileType == ImportDialogBox.DestinationType:
            rawFilepath = archiveFileDialog.getExistingDirectory(self,self.mainWindow.text.localisation('dialogBoxes','export','question'),os.path.expanduser(self.archiveFilePath))

            if rawFilepath :
                filepath = Path(rawFilepath)
                self.destinationPath = filepath
                self.destinationSelectButton.setText(filepath.name)

        self.checkReady()

    def addLogEntry(self, entry:str):
        """Adds a line to the text edit with given text.
            Takes one parameter:
            - entry as string.
            Returns nothing.
        """
        self.textEdit.append(entry)

    def checkReady(self):
        """Checks if both archive and destination are selected before enabling import button.
            Takes no parameter.
            Returns nothing.
        """
        self.textEdit.clear()

        archiveReady = False
        destinationReady = False

        if self.archiveFilePath.exists() and self.archiveFilePath.suffix == ImportExport.ArchiveFileExtension:
            archiveReady = True
        else:
            self.addLogEntry(ImportExport.WarningBorder)
            self.addLogEntry(self.mainWindow.text.localisation('logs','wrongFile','caption'))
            self.addLogEntry(ImportExport.WarningBorder)

        if self.destinationPath.exists():
            destinationReady = True

        if archiveReady and destinationReady :
            self.importButton.setEnabled(True)
        else:
            self.importButton.setEnabled(False)

    def resetProgressBar(self,maxValue:int):
        """Reset progress bar by gathering file number and setting it's min/max values and progress steps.
            Takes no parameter.
            Returns nothing.
        """
        maxValue += 4
        self.progressBar.reset()
        self.progressBar.setRange(0,maxValue)
        self.progressBar.setValue(0)

    def bumpProgressBar(self):
        """Bump the value of the progress bar.
            Takes no parameter.
            Returns nothing.
        """
        self.progressBar.setValue(self.progressBar.value()+1)

    def toggleControls(self):
        """Enable or disable UI buttons during export.
            Takes no parameter.
            Returns nothing.
        """
        if self.closeButton.isEnabled() :
            self.closeButton.setEnabled(False)
        else:
            self.closeButton.setEnabled(True)

        if self.importButton.isEnabled() :
            self.importButton.setEnabled(False)
        else:
            self.importButton.setEnabled(True)

        if self.archiveFileSelectButton.isEnabled() :
            self.archiveFileSelectButton.setEnabled(False)
        else:
            self.archiveFileSelectButton.setEnabled(True)

        if self.destinationSelectButton.isEnabled() :
            self.destinationSelectButton.setEnabled(False)
        else:
            self.destinationSelectButton.setEnabled(True)

    def importArchive(self):
        """Import a new library and attached files from a .dsa archive (.tar.gz) and place the extracted files to given destination.
            Takes no parameterself.
            Returns nothing.
        """
        self.textEdit.clear()
        workDirectoryPath = ImportExport().tempDirectoryPath
        self.toggleControls()
        self.resetProgressBar(0)

        try:
            #Ouverture de l'archive
            self.addLogEntry(self.mainWindow.text.localisation('logs','archiveOpening','caption')+self.archiveFilePath.name)
            self.addLogEntry(ImportExport.BlankLine)

            QCoreApplication.processEvents()
            #Open archive
            archive = tarfile.open(self.archiveFilePath.resolve(),'r:gz')

            #Resetting progress bar
            members = archive.getmembers()
            maxValue = len(members)
            self.resetProgressBar(maxValue)

            self.addLogEntry(ImportExport.Border1)
            self.addLogEntry(self.mainWindow.text.localisation('logs','importStart','caption'))
            self.addLogEntry(ImportExport.Border1)
            self.addLogEntry(ImportExport.BlankLine)

            QCoreApplication.processEvents()

            #Extraction
            self.addLogEntry(self.mainWindow.text.localisation('logs','extraction','caption'))
            self.addLogEntry(ImportExport.Border2)
            self.addLogEntry(ImportExport.BlankLine)

            archive.extractall(workDirectoryPath.resolve(), self.extractAndLog(members) )
            archive.close()

            #Moving files to destination
            self.addLogEntry(ImportExport.BlankLine)
            self.addLogEntry(self.mainWindow.text.localisation('logs','movingFiles','caption'))
            self.addLogEntry(ImportExport.Border2)
            self.addLogEntry(ImportExport.BlankLine)

            #Themes
            themesTempDirectoryPath = workDirectoryPath/ImportExport.ArchiveThemesFolderName
            themesDestinationFolderPath = self.destinationPath/ImportExport.ArchiveThemesFolderName
            shutil.copytree(themesTempDirectoryPath, themesDestinationFolderPath.resolve())
            self.bumpProgressBar()

            #Loading files
            self.mainWindow.themes.importThemes(themesDestinationFolderPath)
            self.bumpProgressBar()
            self.addLogEntry(self.mainWindow.text.localisation('logs','themesMoved','caption')+str(themesDestinationFolderPath.resolve()))

            #Effects
            effectsTempDirectoryPath = workDirectoryPath/ImportExport.ArchiveSamplesFolderName/str(1)
            effectsDestinationFolderPath = self.destinationPath/ImportExport.ArchiveSamplesFolderName
            shutil.copytree(effectsTempDirectoryPath, effectsDestinationFolderPath.resolve())
            self.bumpProgressBar()

            #Loading files
            self.bumpProgressBar()
            self.addLogEntry(self.mainWindow.text.localisation('logs','effectsMoved','caption')+str(effectsDestinationFolderPath.resolve()))

            self.addLogEntry(ImportExport.BlankLine)

            #Cleaning temp files
            if workDirectoryPath.exists():
                shutil.rmtree(workDirectoryPath)

            self.addLogEntry(ImportExport.Border1)
            self.addLogEntry(self.mainWindow.text.localisation('logs','importSuccess','caption'))
            self.addLogEntry(ImportExport.Border1)

            self.toggleControls()

        except Exception as e:
            self.addLogEntry(ImportExport.WarningBorder)
            self.addLogEntry(self.mainWindow.text.localisation('logs','error','caption'))
            self.addLogEntry(ImportExport.WarningBorder)
            self.addLogEntry(ImportExport.BlankLine)
            QCoreApplication.processEvents()

            #Cleaning temp files
            if workDirectoryPath.exists():
                shutil.rmtree(workDirectoryPath)

            #Closing archive
            if 'archive' in locals():
                archive.close()

            self.addLogEntry(traceback.format_exc())

            self.toggleControls()

    def extractAndLog(self, members:list):
        """Generator used to log and update progressbar during files extraction.
            Takes one parameter:
            - members as list.
            Yields:
            - one member of parameter 'members' per iteration.
        """
        currentSection = None
        for member in members:
            yield member
            self.bumpProgressBar()
            memberPath = Path(member.name)
            if memberPath.suffix != ImportExport.TempExtension :
                self.addLogEntry(self.mainWindow.text.localisation('logs','file','caption')+member.name)
                QCoreApplication.processEvents()