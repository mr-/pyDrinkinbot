import sys
from PySide import QtCore, QtGui
from random import choice
from os import system

class EditorTab(QtGui.QWidget):

    def contents(self):
        l = self.editor.toPlainText().splitlines(True)
        return [x.rstrip('\n') for x in l]

    def pressedSave(self):
        f = open(self.file, "w")
        f.write(self.editor.toPlainText())

    def __init__(self, fileName, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.file = fileName
        self.setupEditor()
        saveButton = QtGui.QPushButton(self.tr("Save"))
        cancelButton = QtGui.QPushButton(self.tr("Cancel"))

        saveButton.clicked.connect(self.pressedSave)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(saveButton)
        buttonLayout.addWidget(cancelButton)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.editor)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)



    def setupEditor(self):
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(10)

        self.editor = QtGui.QTextEdit()
        self.editor.acceptRichText = False
        self.editor.setFont(font)
        f = open(self.file, "r")
        
        self.editor.setPlainText(f.read())

