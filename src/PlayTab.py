import sys
from PySide import QtCore, QtGui
from random import choice
from os import system

class PlayTab(QtGui.QWidget):

    def data_to_tree(self, parent, data):
        if isinstance(data, dict):
            parent.setFirstColumnSpanned(True)
            for key,value in data.items():
                child = QtGui.QTreeWidgetItem(parent)
                child.setText(0, key)
                self.data_to_tree(child, value)
        elif isinstance(data, list):
            parent.setFirstColumnSpanned(True)
            for index,value in enumerate(data):
                child = QtGui.QTreeWidgetItem(parent)
                #child.setText(0, str(index))
                self.data_to_tree(child, value)
        else:
            widget1 = QtGui.QLabel(parent.treeWidget())
            widget2 = QtGui.QLabel(parent.treeWidget())

            widget1.setText(str(data[0]))
            widget2.setText(str(data[1]))
            parent.treeWidget().setItemWidget(parent, 1, widget1)
            parent.treeWidget().setItemWidget(parent, 2, widget2)


    def updateRecord(self, record):
        self.tree.clear()
        root = self.tree.invisibleRootItem()
        self.data_to_tree(root, record)
        for i in range(0,int(root.childCount())):
            self.tree.expandItem(root.child(i))

    def setupEditor(self):
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(14)
        editor = QtGui.QTextEdit()
        editor.acceptRichText = False
        editor.setFont(font)
        editor.setFixedHeight(23*15)
        return editor

    paused = False
    counter = 1
    def clear(self):
        self.sayLabel.clear()
        self.counter = 1

    def sayMore(self, txt):
        self.sayLabel.setPlainText(str(self.counter) + ". " + txt + "\n\n" + self.sayLabel.toPlainText())
        self.counter += 1 
    def say(self, txt):
        self.sayLabel.setPlainText(txt)


    def pressedStart(self):
        self.paused = False
        self.advance()

    def pressedPause(self):
        self.paused = True

    def advance(self):
        try:
            if self.timer.value() == 100:
                self.timer.setValue(0)
                self.tick()
                self.callback(self, self.drinkers, self.bar, self.settings, self.says)
            if not self.paused:
                self.timer.setValue(self.timer.value() + 1)
        finally:
            if not self.paused:
                time = self.settings.timeout()
                QtCore.QTimer.singleShot(10*int(time), self.advance)
    def tick(self):
        self.digit.display(self.digit.intValue() + 1)

    def __init__(self, drinkers, bar, settings, says, callback, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.callback = callback
        self.drinkers = drinkers
        self.bar = bar
        self.settings = settings
        self.says = says

        startButton = QtGui.QPushButton(self.tr("Start"))
        pauseButton = QtGui.QPushButton(self.tr("Pause"))

        self.sayLabel = self.setupEditor()
        self.tree = QtGui.QTreeWidget()
        self.tree.setFixedHeight(20*13)
        self.tree.setHeaderLabels(["Drinkers", "Drink", "Consumed"])

        self.timer = QtGui.QProgressBar()
        self.digit = QtGui.QLCDNumber(2)

        startButton.clicked.connect(self.pressedStart)
        pauseButton.clicked.connect(self.pressedPause)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(startButton)
        buttonLayout.addWidget(pauseButton)

        timerLayout = QtGui.QHBoxLayout()
        timerLayout.addWidget(self.timer)
        timerLayout.addWidget(self.digit)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(timerLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.sayLabel)
        mainLayout.addWidget(self.tree)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)


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

        fadeLabel = QtGui.QLabel(self.tr("Command to pause music:"))
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

