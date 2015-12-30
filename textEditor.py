#!/usr/bin/python
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.updateUI()

    def updateUI(self):
        self.textArea = QTextEdit()
        self.setCentralWidget(self.textArea)
        self.menuBar = self.menuBar()
        self.updateMenuBar()
        self.formatBar = self.addToolBar("Format")
        self.formatBar.setMovable(False)
        self.formatBar.setFloatable(False)
        self.updateFormatBar()
        self.statusBar = self.statusBar()
        self.updateStatusBar()

    def sizeHint(self):
        height = 500
        width = 700
        return QSize(width, height)

    def updateMenuBar(self):
        self.fileMenu = self.menuBar.addMenu('&File')
        self.editMenu = self.menuBar.addMenu('&Edit')
        self.viewMenu = self.menuBar.addMenu('&View')
        self.updateViewMenu()
        self.insertMenu = self.menuBar.addMenu('&Insert')
        self.updateInsertMenu()

    def updateInsertMenu(self):
        self.imageAction = QAction(QIcon(''), "Image", self)
        self.connect(self.imageAction, SIGNAL("triggered()"), self.insertImage)
        self.insertMenu.addAction(self.imageAction)

    def updateViewMenu(self):
        fullScreenAction = QAction(QIcon(''), 'Full Screen', self,
                                   checkable=True)
        fullScreenAction.setShortcut(QKeySequence(Qt.Key_F11))
        self.connect(fullScreenAction, SIGNAL("triggered()"), self.fullScreen)
        self.viewMenu.addAction(fullScreenAction)
        self.toolbarAction = QAction(QIcon(''), 'Toolbar', self,
                                     checkable=True)
        self.toolbarAction.setChecked(True)
        self.connect(self.toolbarAction, SIGNAL("triggered()"),
                     self.showHideToolbar)
        self.viewMenu.addAction(self.toolbarAction)

    def showHideToolbar(self):
        if self.toolbarAction.isChecked() is True:
            self.formatBar.show()
        else:
            self.formatBar.hide()

    def fullScreen(self):
        if self.isFullScreen() is True:
            self.showNormal()
        else:
            self.showFullScreen()

    def updateFormatBar(self):
        print "updateFormatBar"
        # #Code

    def updateStatusBar(self):
        self.zoomSlider = QSlider(Qt.Horizontal, self.statusBar)
        self.zoomSlider.setTickPosition(QSlider.TicksAbove)
        self.zoomSlider.setTickInterval(10)
        self.zoomSlider.setValue(80)
        self.zoomSlider.setRange(70, 90)
        self.curZoomValue = 80
        self.countLabel = QLabel(self)
        self.positionLabel = QLabel(self)
        self.emptyLabel = QLabel(self)
        self.statusBar.insertPermanentWidget(0, self.emptyLabel, 10)
        self.statusBar.insertPermanentWidget(1, self.positionLabel, 10)
        self.statusBar.insertPermanentWidget(2, self.countLabel, 10)
        self.statusBar.insertPermanentWidget(3, self.zoomSlider, 4)
        self.cursorPosition()
        self.connect(self.zoomSlider, SIGNAL("valueChanged(int)"), self.zoom)
        self.connect(self.textArea, SIGNAL("cursorPositionChanged()"),
                     self.cursorPosition)

    def zoom(self):
        value = self.zoomSlider.value()
        if self.curZoomValue > value:
            self.textArea.zoomOut((self.curZoomValue - value))
        else:
            self.textArea.zoomIn((value - self.curZoomValue))
        self.curZoomValue = value

    def cursorPosition(self):
        cursor = self.textArea.textCursor()
        curLine = str(cursor.blockNumber() + 1)
        curCol = str(cursor.columnNumber())
        # #print curLine, curCol
        self.positionLabel.setText(curLine + ',' + curCol)
        self.wordSymbolCount()

    def wordSymbolCount(self):
        selectedText = self.textArea.textCursor().selectedText()
        if selectedText == '':
            text = self.textArea.toPlainText()
            wordCount = len(text.split(' '))
            symbolCount = len(text)
        else:
            wordCount = len(selectedText.split(' '))
            symbolCount = len(selectedText)
        # #print wordCount, symbolCount
        self.countLabel.setText("Word: " + str(wordCount) + ", " +
                                "Symbols: " + str(symbolCount))

    def insertImage(self):
        filename = QFileDialog.getOpenFileName(self, 'Insert image', ".",
                                               "Images(*.png *.xpm *.jpg *.bmp\
                                               *.gif)")
        if filename:
            image = QImage(filename)
            if image.isNull():
                popup = QMessageBox(QMessageBox.Critical, "Image load error",
                                    "Could not load image file!",
                                    QMessageBox.Ok, self)
                popup.show()
            else:
                cursor = self.textArea.textCursor()
                cursor.insertImage(image, filename)


def main():
    app = QApplication(sys.argv)
    textEditor = mainWindow()
    textEditor.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()