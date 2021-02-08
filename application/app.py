import sys
import os
from PyQt5.QtWidgets import QMainWindow,QHBoxLayout,QWidget,QApplication
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QUrl
from PyQt5 import QtGui

class JDS_CLIENT(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedWidth(1400)
        self.setFixedHeight(800)
        self.setWindowTitle("Joint Downloading System [Desktop client]")
        self.setStyleSheet("QMainWindow {background: '#151515';}")

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo-512x512.png'))

        self.webEngineView = QWebEngineView()
        self.webEngineDebugger = QWebEngineView()

        self.loadWebPage()
        self.loadDebbuger()

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.webEngineView)
        horizontalLayout.addWidget(self.webEngineDebugger)

        widget = QWidget()
        widget.setLayout(horizontalLayout)

        self.setCentralWidget(widget)
        self.show()

    def loadWebPage(self):
        self.webEngineView.load(QUrl("http://localhost/JDS"))

    def loadDebbuger(self):
        self.webEngineDebugger.load(QUrl("http://127.0.0.1:1231"))

def main():
    app = QApplication(sys.argv)
    clientApp = JDS_CLIENT()
    print("APP INITIALIZED")

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
