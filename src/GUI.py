import sys
from PySide import QtCore, QtGui
from random import choice
from os import system

class DrinkingBot(QtGui.QDialog):
    def __init__(self, callback, parent=None):
        QtGui.QDialog.__init__(self, parent)

        drinkers = EditorTab("../data/drinkers")
        bar = EditorTab("../data/bar")
        says = EditorTab("../data/says")
        settings = SettingsTab()


        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(GeneralTab(drinkers, bar, settings, says, callback), self.tr("General"))
        tabWidget.addTab(drinkers, self.tr("Drinkers"))
        tabWidget.addTab(bar, self.tr("Bar"))
        tabWidget.addTab(says, self.tr("Says"))

        tabWidget.addTab(settings, self.tr("Settings"))



        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)
        self.resize(500, 600)
        self.setWindowTitle(self.tr("pyDrinkinbot"))


class GeneralTab(QtGui.QWidget):

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
        return editor

    paused = False

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
                self.callback(self, self.drinkers, self.bar, self.settings, self.says)

            if not self.paused:
                self.timer.setValue(self.timer.value() + 1)
        finally:
            if not self.paused:
                time = self.settings.timeout()
                QtCore.QTimer.singleShot(10*int(time), self.advance)

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
        self.tree.setHeaderLabels(["Drinkers", "Drink", "Consumed"])

        self.timer = QtGui.QProgressBar()
        startButton.clicked.connect(self.pressedStart)
        pauseButton.clicked.connect(self.pressedPause)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(startButton)
        buttonLayout.addWidget(pauseButton)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.timer)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.sayLabel)
        mainLayout.addWidget(self.tree)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)


class SettingsTab(QtGui.QWidget):

    def bonusrounds(self):
        return self.bonusEdit.text()

    def timeout(self):
        return self.timeoutEdit.text()

    def __init__(self,  parent=None):
        QtGui.QWidget.__init__(self, parent)

        timeoutLabel = QtGui.QLabel(self.tr("Timeout:"))
        self.timeoutEdit = QtGui.QLineEdit("30")

        bonusLabel = QtGui.QLabel(self.tr("Bonusrounds:"))
        self.bonusEdit = QtGui.QLineEdit("6")

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(timeoutLabel)
        mainLayout.addWidget(self.timeoutEdit)
        mainLayout.addWidget(bonusLabel)
        mainLayout.addWidget(self.bonusEdit)
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
        
def runBot(argv, callback):
    app = QtGui.QApplication(argv)
    drinkingBot = DrinkingBot(callback)
    sys.exit(drinkingBot.exec_())