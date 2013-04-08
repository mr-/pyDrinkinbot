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
        self.updateTotals(record)

    def updateTotals(self, record):
        s = ""
        for name in sorted(self.drinkers.contents()):
            s += "" +name + "\t" + self.totalFromRec(record, name) + "\n"
        self.totals.setPlainText(s)

    def totalFromRec(self,record,name):
        if not name in record.keys(): return str(0)
        return str(sum( [x[1] for x in record[name]]))


    sayCounter = 1

    def clear(self):
        self.sayLabel.clear()
        self.counter = 1

    def sayMore(self, txt):
        self.sayLabel.setPlainText(str(self.counter) + ". " + txt + "\n\n" + self.sayLabel.toPlainText())
        self.counter += 1 

    def say(self, txt):
        self.sayLabel.setPlainText(txt)


    def tick(self):
        self.digit.display(self.digit.intValue() + 1)

    def gameRound(self):
        return self.digit.intValue()


    paused = False

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


    def __init__(self, drinkers, bar, settings, says, callback, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.callback = callback
        self.drinkers = drinkers
        self.bar = bar
        self.settings = settings
        self.says = says

        startButton = QtGui.QPushButton(self.tr("Start"))
        pauseButton = QtGui.QPushButton(self.tr("Pause"))

        self.sayLabel = self.setupEditor(14)

        self.totals = self.setupEditor(12)
        self.tree = QtGui.QTreeWidget()
        self.tree.setFixedHeight(20*13)
        self.tree.setHeaderLabels(["Drinkers", "Drink", "Consumed"])

        statsLayout = QtGui.QHBoxLayout()
        statsLayout.addWidget(self.tree)
        statsLayout.addWidget(self.totals)

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
        mainLayout.addLayout(statsLayout)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

    def setupEditor(self, lines):
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(14)
        editor = QtGui.QTextEdit()
        editor.acceptRichText = True
        editor.setFont(font)
        editor.setFixedHeight(23*lines)
        return editor
