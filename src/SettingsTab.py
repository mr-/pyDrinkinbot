import sys
from PySide import QtCore, QtGui
from random import choice
from os import system

class SettingsTab(QtGui.QWidget):

    def bonusrounds(self):

        def convert(s):
            try:
                return float(s)
            except ValueError:
                num, denom = s.split('/')
                return float(num) / float(denom)

        return convert(self.bonusEdit.text())

    def timeout(self):
        return int(self.timeoutEdit.text())

    def fadeCommand(self):
        return self.fadeEdit.text()

    def quiet(self):
        return self.quietBox.isChecked()

    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self, parent)

        timeoutLabel = QtGui.QLabel(self.tr("Time to action in seconds:"))
        self.timeoutEdit = QtGui.QLineEdit("30")
        self.timeoutEdit.setFixedWidth(40)


        bonusLabel = QtGui.QLabel(self.tr("Probability for Bonusround:"))
        self.bonusEdit = QtGui.QLineEdit("1/6")
        self.bonusEdit.setFixedWidth(40)

        fadeLabel = QtGui.QLabel(self.tr("Command to pause music: (use : for nothing)"))
        self.fadeEdit = QtGui.QLineEdit("rhythmbox-client --play-pause")
        fadeLayout = QtGui.QHBoxLayout()
        fadeLayout.addWidget(fadeLabel)
        fadeLayout.addWidget(self.fadeEdit)
        #self.fadeEdit.setFixedWidth(40)

        self.quietBox = QtGui.QCheckBox("Quiet")
        timeoutLayout = QtGui.QHBoxLayout()
        timeoutLayout.addWidget(timeoutLabel)
        timeoutLayout.addWidget(self.timeoutEdit)

        bonusLayout = QtGui.QHBoxLayout()
        bonusLayout.addWidget(bonusLabel)
        bonusLayout.addWidget(self.bonusEdit)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(timeoutLayout)
        mainLayout.addLayout(bonusLayout)
        mainLayout.addLayout(fadeLayout)
        mainLayout.addWidget(self.quietBox)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)
