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
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QApplication, QSystemTrayIcon, QMenu



app = QApplication(sys.argv)

threads = []
server_lan = server.lanServer()
wSocket = socket.websocketserver(5678);

domainObject = domainName()
hostdomain = str(domainObject.getDomain())
jds_server_domain = "50941b8c69cd.ngrok.io"



class JDS_CLIENT(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.initUI(url)

    def initUI(self, url):
        self.webURL = url
        self.resize(1300, 800)
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

        # self.setQuitOnLastWindowClosed(False)
        self.trayIcon = QSystemTrayIcon(QtGui.QIcon("logo-512x512.png"), parent=app)
        self.trayIcon.setToolTip('JDS Client download manager is running in background.')
        self.trayIcon.show()

        self.trayMenu = QMenu()
        self.exitAction = self.trayMenu.addAction('Exit')
        self.exitAction.triggered.connect(app.quit)

        self.trayIcon.setContextMenu(self.trayMenu)

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + '/images/logo/logo-512x512.png'))

        self.webViewOnline = QWebEngineView()
        self.webViewClient = QWebEngineView()

        self.loadWebPage()
        self.loadClientPage()

        # Main pane
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.addWidget(self.webViewOnline) # JDS online webview
        horizontalLayout.addWidget(self.webViewClient) # Local Client file sharing

        widget = QWidget()
        widget.setLayout(horizontalLayout)

        self.setCentralWidget(widget)
        self.show()

    def loadWebPage(self):
        self.webViewOnline.load(QUrl(self.webURL))

    def loadClientPage(self):
        self.webViewClient.load(QUrl("http://"+hostdomain+":8000/index.html"))
        self.webViewClient.setFixedWidth(350)



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

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(self.webViewOnline)

        widget = QWidget()
        widget.setLayout(horizontalLayout)

        self.setCentralWidget(widget)
        self.show()

    def loadWebPage(self):
        self.webViewOnline.load(QUrl("http://"+hostdomain+":1231"))



class Threader (threading.Thread):
    # https://www.tutorialspoint.com/python/python_multithreading.htm
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter


    def run(self):
        print("[+] Starting " + self.name)

        if (self.name == "LOCAL_HTTP_SERVER"):
            try:
                server_lan.start()
            except:
                print("[!] Error while starting LAN server!")

        elif (self.name == "SOCKET_SERVER"):
            # SOCKET SERVER SECTION ------------------------------------------->
            # https://websockets.readthedocs.io/en/stable/intro.html
            wSocket.start();
            # ----------------------------------------------------------------->

        print("[*] Exiting thread: " + self.name)


# Exit application ------------------------------------------------------------>
def exit_():
    app.exec_()
    # app.quit
    for t in threads:
        # print(t) # Show thread
        if (t.name == "LOCAL_HTTP_SERVER"):
            try:
                server_lan.stop()
            except:
                print("Error while closing LAN server!")

        elif (t.name == "SOCKET_SERVER"):
            try:
                wSocket.close()
            except:
                print("Error while closing WebSocket server!")

        t.join()
    print("[+] Threads killed!")
# ----------------------------------------------------------------------------->


def main():
    # USER INTERFACE ---------------------------------------------------------->
    clientApp = JDS_CLIENT("https://"+jds_server_domain+"/JDS") # CLIENT APPLICATION
    clientDebugger = JDS_DEBUGGER() # CLIENT APP DEBUGGER [Inspect element]
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
    # ------------------------------------------------------------------------->


    sys.exit(exit_())



if __name__ == '__main__':
    main()
