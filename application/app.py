import sys
import os
from PyQt5 import QtGui, QtCore, QtNetwork
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow,QHBoxLayout,QWidget,QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel


class JDS_CLIENT(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(1200, 800)
        self.setMinimumSize(800, 800)
        self.setWindowTitle("Joint Downloading System [Desktop client]")
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # make window frameless
        self.setStyleSheet("""
            QMainWindow {
                background: '#2d2d2d';
                padding: 0px;
                margin: 0;
            }
            """)

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo-512x512.png'))

        self.webEngineView = QWebEngineView()

        self.loadWebPage()

        horizontalLayout = QHBoxLayout()
        horizontalLayout.setContentsMargins(0, 0, 0, 0);
        horizontalLayout.addWidget(self.webEngineView)

        widget = QWidget()
        widget.setLayout(horizontalLayout)

        self.setCentralWidget(widget)
        self.show()

    def loadWebPage(self):
        self.webEngineView.load(QUrl("http://localhost/JDS"))


class JDS_DEBUGGER(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.setFixedWidth(1400)
        # self.setFixedHeight(800)
        self.setWindowTitle("Joint Downloading System [Desktop client debugger]")

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo-512x512.png'))

        self.webEngineView = QWebEngineView()

        self.loadWebPage()

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.webEngineView)

        widget = QWidget()
        widget.setLayout(horizontalLayout)

        self.setCentralWidget(widget)
        self.show()

    def loadWebPage(self):
        self.webEngineView.load(QUrl("http://127.0.0.1:1231"))


def main():
    app = QApplication(sys.argv)
    clientApp = JDS_CLIENT() # CLIENT APPLICATION
    # clientDebugger = JDS_DEBUGGER() # CLIENT APP DEBUGGER [Inspect element]
    print("APP INITIALIZED")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
