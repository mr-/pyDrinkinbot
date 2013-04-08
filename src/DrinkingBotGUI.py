import sys
from PySide import QtCore, QtGui
from random import choice
from os import system

from EditorTab import EditorTab
from SettingsTab import SettingsTab
from PlayTab import PlayTab

def runBot(argv, callback, drinkersFile = "../data/drinkers", 
                           barFile="../data/bar", 
                           saysFile="../data/says"):
    app = QtGui.QApplication(argv)
    drinkingBot = DrinkingBot(callback, drinkersFile, barFile, saysFile)
    sys.exit(drinkingBot.exec_())


class DrinkingBot(QtGui.QDialog):
    def __init__(self, callback, drinkersFile, barFile, saysFile, parent=None):
        QtGui.QDialog.__init__(self, parent)

        drinkers = EditorTab(drinkersFile)
        bar = EditorTab(barFile)
        says = EditorTab(saysFile)
        settings = SettingsTab()


        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(PlayTab(drinkers, bar, settings, says, callback), self.tr("General"))
        tabWidget.addTab(drinkers, self.tr("Drinkers"))
        tabWidget.addTab(bar, self.tr("Bar"))
        tabWidget.addTab(says, self.tr("Says"))

        tabWidget.addTab(settings, self.tr("Settings"))



        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)
        self.resize(700, 700)
        self.setWindowTitle(self.tr("pyDrinkinbot"))

