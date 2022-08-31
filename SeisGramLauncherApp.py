import os
from os import stat
import sys
import subprocess
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow#, QLineEdit, QLabel
from PyQt5 import QtCore
from SeisGramLauncherGUI import Ui_MainWindow

removeDC=' -commands.onread rmean'
visual= False

class SeisgramLauncherApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.bOK.clicked.connect(self.launcher)
        self.ui.eStation.textChanged.connect(self.enableButton)  # textChanged, con esto estoy al tanto del contenido del editLine
        self.ui.eNet.textChanged.connect(self.enableButton)
        self.ui.eLocation.textChanged.connect(self.enableButton)
        self.ui.eCh.textChanged.connect(self.enableButton)
        self.ui.teIPs.textChanged.connect(self.enableButton)
        self.ui.cbLineaBase.stateChanged.connect(self.lineaBase)
        self.ui.cbVisual.stateChanged.connect(self.visual)

        self.show()

    def enableButton(self):
        if (self.ui.eStation.text() and self.ui.eNet.text() and self.ui.eLocation.text()
           and self.ui.eCh.text() and self.ui.teIPs.toPlainText()):  # and len(self.ui.eStation.text())>=3   # La segunda condición es para que tenga un mínimo de caracteres
            self.ui.bOK.setEnabled(True)
        else:
            self.ui.bOK.setEnabled(False)

    def lineaBase(self, state):
        global removeDC
        if (QtCore.Qt.Checked == state):
            removeDC= ''
        else:
            removeDC= ' -commands.onread rmean'

    def visual(self, state):
        global visual
        if (QtCore.Qt.Checked == state):
            visual= True
        else:
            visual= False

    def launcher(self):
        global removeDC, visual
        # Leo todos las entradas de textos
        station= self.ui.eStation.text().strip()
        station= station.split(',')
        net= self.ui.eNet.text()
        location= self.ui.eLocation.text()
        labelchn= self.ui.eCh.text()
        ipAddress= self.ui.teIPs.toPlainText().strip()
        ipAddress= ipAddress.split('\n')
        part1CMD= list()
        # Creo una sección del comando
        # Comando completo START java -cp SeisGram2K60.jar net.alomax.seisgram2k.SeisGram2K  -seedlink "192.168.0.1:18000#XX_SSI:EH?#20" -seedlink.groupchannels YES -commands.onread rmean
        # print(station, type(station))
        for sta in station:
            for ip in ipAddress:
                part1CMD.append(ip+':18000#'+net+'_'+sta+':'+labelchn+'?#20') # Guardo cada IP con su respectiva parte de comando
        # Pregunto si se seleccionó la opción de visualización individual
        if not visual:
            partAuxCMD= ';'.join(part1CMD) # Concateno cada posición de part1CMD y las separo con ;
            if removeDC == '':
                # command= 'START java -cp SeisGram2K60.jar net.alomax.seisgram2k.SeisGram2K -seedlink "'+partAuxCMD+'" -seedlink.groupchannels YES &'
                # for Linux:
                command= 'java -cp SeisGram2K60.jar net.alomax.seisgram2k.SeisGram2K -seedlink "'+partAuxCMD+'" -seedlink.groupchannels YES &'
                p = subprocess.run(command, shell = True)
            else:
                # command= 'START java -cp SeisGram2K60.jar net.alomax.seisgram2k.SeisGram2K -seedlink "'+partAuxCMD+'" -seedlink.groupchannels YES'+removeDC+' &'
                # for Linux:
                command= 'java -cp SeisGram2K60.jar net.alomax.seisgram2k.SeisGram2K -seedlink "'+partAuxCMD+'" -seedlink.groupchannels YES'+removeDC+' &'
                p = subprocess.run(command, shell = True)
            # print(command)
        else:
            if removeDC == '':
                for AuxCMD in part1CMD:
                    # command= 'START java -cp SeisGram2K60.jar net.alomax.seisgram2k.SeisGram2K -seedlink "'+AuxCMD+'" -seedlink.groupchannels YES &'
                    # for Linux:
                    command= 'java -cp SeisGram2K60.jar net.alomax.seisgram2k.SeisGram2K -seedlink "'+partAuxCMD+'" -seedlink.groupchannels YES &'
                    p = subprocess.run(command, shell = True)
            else:
                for AuxCMD in part1CMD:
                    # command= 'START java -cp SeisGram2K60.jar net.alomax.seisgram2k.SeisGram2K -seedlink "'+AuxCMD+'" -seedlink.groupchannels YES'+removeDC+' &'
                    # for Linux:
                    command= 'java -cp SeisGram2K60.jar net.alomax.seisgram2k.SeisGram2K -seedlink "'+partAuxCMD+'" -seedlink.groupchannels YES'+removeDC+' &'
                    p = subprocess.run(command, shell = True)
            # print(command)

#########Slinktool
        #to Linux
        # command= 'ps aux | grep slinktool'
        # p= subprocess.run(command, shell = True)
        # print(p)
        command= 'pkill slinktool'
        p= subprocess.run(command, shell = True)
        # iIP=0
        for iIP in ipAddress:
            command= 'slinktool -vv -s '+labelchn+'? -o data.mseed -A %Y/%n/%s/%c.D/%n.%s.%l.%c.D.%Y.%j.miniseed '+iIP+':18000 &'
            p= subprocess.run(command, shell = True)
            # print(command)

        #to Windows
        # command= 'TASKKILL /IM slinktool-4.0-Win.exe /F'
        # p= subprocess.run(command, shell = True)
        # for iIP in ipAddress:
        #     command= 'slinktool -s '+labelchn+'? -o data.mseed -A %%Y/%%n/%%s/%%c.D/%%n.%%s.%%l.%%c.D.%%Y.%%j.miniseed '+iIP+':18000 &'
        #     p= subprocess.run(command, shell = True)

        # print(station,'\n',net,'\n',location,'\n',labelchn,'\n',ipAddress)
        # print(part1CMD)
        # print(visual)
        # print(removeDC)
        # partAuxCMD= ';'.join(part1CMD)
        # print(partAuxCMD)

if __name__ == '__main__':
    app= QApplication(sys.argv)
    ventana = SeisgramLauncherApp()
    ventana.show()
    sys.exit(app.exec_())