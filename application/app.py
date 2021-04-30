import sys
import os
import time
import threading

from threading import Thread
from engine import eng_server
from engine import eng_socket
from engine.eng_platform import domainName
from engine.eng_downloader import downloadManagerSS
from engine.eng_sharing import sharingManagerSS

from PyQt5.QtCore import *
from PyQt5.QtWebChannel import *
from PyQt5 import QtGui, QtCore, QtNetwork
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *



app = QApplication(sys.argv)
appIsExiting = False

threads = []
server_lan = eng_server.lanServer()
wSocket = eng_socket.websocketserver(5678);

downloadMngrService = downloadManagerSS()
sharingMngrService = sharingManagerSS()

domainObject = domainName()
hostdomain = str(domainObject.getDomain())
jds_server_domain = str(domainObject.getServerDomain())



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
        self.trayIcon.hide()

        self.trayMenu = QMenu()
        self.exitAction = self.trayMenu.addAction('Exit')
        self.exitAction.triggered.connect(lambda: app.quit())

        self.exitAction = self.trayMenu.addAction('Restore')
        self.exitAction.triggered.connect(lambda: self.restore_window())

        self.trayIcon.setContextMenu(self.trayMenu)
        # --------------------------------------------------------------------->


        # Window -------------------------------------------------------------->
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + '/images/logo/logo-512x512.png'))
        self.show()
        # --------------------------------------------------------------------->

    def event(self, event):
        if (event.type() == QtCore.QEvent.WindowStateChange and
                self.isMinimized()):
            # The window is already minimized at this point.  AFAIK,
            # there is no hook stop a minimize event. Instead,
            # removing the Qt.Tool flag should remove the window
            # from the taskbar.
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.Tool)
            self.trayIcon.show()
            return True
        else:
            return super(JDS_CLIENT, self).event(event)


    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Message',"Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            self.trayIcon.show()
            self.hide()
            event.ignore()


    def restore_window(self):
        self.trayIcon.hide()
        # Restore the window
        self.showNormal()



    def loadWebPage(self):
        self.webViewOnline.load(QUrl(self.webURL))


    def loadClientPage(self):
        self.webViewClient.load(QUrl("http://"+hostdomain+":8000/index.html"))
        self.webViewClient.setMinimumWidth(395)
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

        if self.name == "LOCAL_HTTP_SERVER":
            # HTTP SERVER SECTION --------------------------------------------->
            try:
                server_lan.start()
            except Exception as err:
                print("[!] Error while starting LAN server: ", err)
            # ----------------------------------------------------------------->

        elif self.name == "SOCKET_SERVER":
            # SOCKET SERVER SECTION ------------------------------------------->
            # https://websockets.readthedocs.io/en/stable/intro.html
            wSocket.start()
            # ----------------------------------------------------------------->

        elif self.name == "DOWNLOAD_MNGR":
            # DOWNLOAD MANAGER SECTION ---------------------------------------->
            downloadMngrService.connect()
            # ----------------------------------------------------------------->

        elif self.name == "SHARING_MNGR":
            # DOWNLOAD MANAGER SECTION ---------------------------------------->
            sharingMngrService.connect()
            # ----------------------------------------------------------------->

        elif self.name == "DEBUGGER":
            # DEBUGGER SECTION ------------------------------------------------>
            clientDebugger = JDS_DEBUGGER() # CLIENT APP DEBUGGER [Inspect element]
            # ----------------------------------------------------------------->

        print("[*] Exiting thread: " + self.name)

        if os.path.exists("u_config.json"):
            print("[!] Restarting closed services")
            if self.name == "SOCKET_SERVER":
                wSocket.start()

            elif self.name == "DOWNLOAD_MNGR":
                downloadMngrService.connect()

            elif self.name == "SHARING_MNGR":
                sharingMngrService.connect()


# Exit application ------------------------------------------------------------>
def exit_():
    app.exec_()
    print("\n[!] Exiting application")

    if os.path.exists("u_config.json"):
        os.remove("u_config.json")
    else:
        print("[!] User configuration could not be located")

    # app.quit
    for t in threads:
        print(t) # Show thread
        if (t.name == "LOCAL_HTTP_SERVER"):
            try:
                server_lan.stop()
            except:
                print("[-] Error while closing LAN server!")


        elif (t.name == "SOCKET_SERVER"):
            try:
                wSocket.close()
                print("[!] Socket server stopped!")
            except Exception as e:
                print("[-] Error while closing WebSocket server:", e)


        elif (t.name == "DOWNLOAD_MNGR"):
            try:
                # downloadMngrService.exit()
                print("[!] Close download manager service")
            except:
                print("[-] Error while closing download manager service!")


        elif (t.name == "SHARING_MNGR"):
            try:
                # sharingMngrService.exit()
                print("[!] Close sharing manager service")
            except:
                print("[-] Error while closing sharing manager service!")

        # print(t) # Show thread
        t.join()

    print("[+] Closed all threads!")
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


    thread3 = Threader(3, "DOWNLOAD_MNGR", 3)
    thread3.start()
    threads.append(thread3)
    print("[+] Download manager initialized")


    thread4 = Threader(4, "SHARING_MNGR", 4)
    thread4.start()
    threads.append(thread4)
    print("[+] Sharing manager initialized")


    # thread4 = Threader(4, "DEBUGGER", 4)
    # thread4.start()
    # threads.append(thread4)
    # print("[+] Debugger initialized")
    # ------------------------------------------------------------------------->


    sys.exit(exit_())



if __name__ == '__main__':
    main()
