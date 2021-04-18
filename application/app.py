import sys
import os
import time
import threading

from threading import Thread
from engine import server
from engine import socket
from engine.platform import domainName

from PyQt5.QtCore import *
from PyQt5.QtWebChannel import *
from PyQt5 import QtGui, QtCore, QtNetwork
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *



app = QApplication(sys.argv)
appIsExiting = False

threads = []
server_lan = server.lanServer()
wSocket = socket.websocketserver(5678);

domainObject = domainName()
hostdomain = str(domainObject.getDomain())
jds_server_domain = "2e52b1f72955.ngrok.io"



class JDS_DEBUGGER(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 800)
        # self.setFixedWidth(1400)
        # self.setFixedHeight(800)
        self.setWindowTitle("Joint Downloading System [Desktop client debugger]")

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo-512x512.png'))

        self.webViewOnline = QWebEngineView()

        self.loadWebPage()

        horizontalBox = QHBoxLayout()
        horizontalBox.addWidget(self.webViewOnline)

        widget = QWidget()
        widget.setLayout(horizontalBox)

        self.setCentralWidget(widget)
        self.show()

    def loadWebPage(self):
        self.webViewOnline.load(QUrl("http://"+hostdomain+":1231"))



# class JDS_CLIENT(QWidget):
class JDS_CLIENT(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.initUI(url)

    def initUI(self, url):
        # Webview ------------------------------------------------------------->
        self.webURL = url
        self.webViewOnline = QWebEngineView()
        self.webViewClient = QWebEngineView()

        self.loadWebPage()
        self.loadClientPage()
        # --------------------------------------------------------------------->


        # Main pane ----------------------------------------------------------->
        horizontalBox = QHBoxLayout()
        horizontalBox.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.webViewOnline) # JDS online webview
        splitter.addWidget(self.webViewClient) # Local Client file sharing

        horizontalBox.addWidget(splitter)

        # horizontalBox.addWidget(self.webViewOnline) # JDS online webview
        # horizontalBox.addWidget(self.webViewClient) # Local Client file sharing

        # widget = QWidget()
        # widget.setLayout(horizontalBox)

        # self.setLayout(horizontalBox)

        parentWidget = QWidget()
        parentWidget.setLayout(horizontalBox)
        self.setCentralWidget(parentWidget)

        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

        self.resize(1300, 800)
        self.setMinimumSize(800, 800)
        self.setWindowTitle("Joint Downloading System [Desktop client]")
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # make window frameless
        self.setStyleSheet("""
            QWidget {
                background-color: '#2d2d2d';
                padding: 0px;
                margin: 0;
            }
            """)
        # --------------------------------------------------------------------->


        # Menu bar ------------------------------------------------------------>
        self.menuBar = self.menuBar()
        self.menuBar.setStyleSheet("""
            QWidget {
                background-color: '#fff';
            }
            """)

        fileMenu = self.menuBar.addMenu('File')
        helpMenu = self.menuBar.addMenu('Help')

        # Debugger ---
        debug_action = QAction('Open debugger', self)
        debug_action.setShortcut('Ctrl+alt+d')
        debug_action.triggered.connect(lambda: JDS_DEBUGGER())
        helpMenu.addAction(debug_action)
        # ------------

        # Exit ---
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(lambda:  app.quit())
        fileMenu.addAction(exit_action)
        # --------

        # --------------------------------------------------------------------->


        # Task bar ------------------------------------------------------------>
        # self.setQuitOnLastWindowClosed(False)
        self.trayIcon = QSystemTrayIcon(QtGui.QIcon("logo-512x512.png"), parent=app)
        self.trayIcon.setToolTip('JDS Client download manager is running in background.')
        self.trayIcon.show()

        self.trayMenu = QMenu()
        self.exitAction = self.trayMenu.addAction('Exit')
        self.exitAction.triggered.connect(lambda: app.quit())

        self.trayIcon.setContextMenu(self.trayMenu)
        # --------------------------------------------------------------------->


        # Window -------------------------------------------------------------->
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + '/images/logo/logo-512x512.png'))
        self.show()
        # --------------------------------------------------------------------->

    def loadWebPage(self):
        self.webViewOnline.load(QUrl(self.webURL))

    def loadClientPage(self):
        self.webViewClient.load(QUrl("http://"+hostdomain+":8000/index.html"))
        self.webViewClient.setMinimumWidth(250)
        self.webViewClient.setMaximumWidth(450)



class Threader (threading.Thread):
    # https://www.tutorialspoint.com/python/python_multithreading.htm
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("[+] Starting " + self.name)

        if (self.name == "LOCAL_HTTP_SERVER"):
            # HTTP SERVER SECTION --------------------------------------------->
            try:
                server_lan.start()
            except Exception as err:
                print("[!] Error while starting LAN server: ", err)
            # ----------------------------------------------------------------->

        elif (self.name == "SOCKET_SERVER"):
            # SOCKET SERVER SECTION ------------------------------------------->
            # https://websockets.readthedocs.io/en/stable/intro.html
            wSocket.start();
            # ----------------------------------------------------------------->

        elif (self.name == "DEBUGGER"):
            # DEBUGGER SECTION ------------------------------------------------>
            clientDebugger = JDS_DEBUGGER() # CLIENT APP DEBUGGER [Inspect element]
            # ----------------------------------------------------------------->

        print("[*] Exiting thread: " + self.name)

        if appIsExiting == False:
            print("[!] Restarting closed services")
            if self.name == "SOCKET_SERVER":
                wSocket.start();


# Exit application ------------------------------------------------------------>
def exit_():
    app.exec_()
    print("\n[!] Exiting application")
    appIsExiting = True
    # app.quit
    for t in threads:
        print(t) # Show thread
        if (t.name == "LOCAL_HTTP_SERVER"):
            try:
                server_lan.stop()
            except:
                print("Error while closing LAN server!")

        elif (t.name == "SOCKET_SERVER"):
            try:
                wSocket.close()
                print("[!] Socket server stopped!")
            except:
                print("Error while closing WebSocket server!")

        # print(t) # Show thread
        t.join()

    print("[!] Closed all threads!")
# ----------------------------------------------------------------------------->



def main():
    # USER INTERFACE ---------------------------------------------------------->
    clientApp = JDS_CLIENT("https://"+jds_server_domain+"/JDS") # CLIENT APPLICATION
    # clientDebugger = JDS_DEBUGGER() # CLIENT APP DEBUGGER [Inspect element]
    # ------------------------------------------------------------------------->


    # THREAD SECTION ---------------------------------------------------------->
    thread1 = Threader(1, "LOCAL_HTTP_SERVER", 1)
    thread1.start()
    threads.append(thread1)
    print("[+] Local server initialized")


    thread2 = Threader(2, "SOCKET_SERVER", 2)
    thread2.start()
    threads.append(thread2)
    print("[+] Socket server initialized")


    # thread3 = Threader(3, "DEBUGGER", 3)
    # thread3.start()
    # threads.append(thread3)
    # print("[+] Debugger initialized")
    # ------------------------------------------------------------------------->


    sys.exit(exit_())



if __name__ == '__main__':
    main()
