import os
import socket
from sys import platform
from engine.eng_server import lanServer

class domainName(object):
    def __init__(self):
        super(domainName, self).__init__()

    def getDomain(self):
        if platform == "linux" or platform == "linux2":
            # Linux OS
            self.domain = "localhost"
        elif platform == "darwin":
            # OS X
            self.domain = str(socket.gethostbyname(socket.gethostname()))
        elif platform == "win32":
            # Windows
            self.domain = "localhost"
        return str(self.domain)


    def getServerDomain(self):
        # This is a temporary solution to easily
        # update ngrok server address
        netconf = None
        if os.path.exists('netconf.json'):
            netconfFile = open('netconf.json', 'r')
            netconf = json.loads(netconfFile.read())
            netconfFile.close()
            return netconf['server']
        else:
            return "cf80d7746327.ngrok.io"

if __name__ == '__main__':
    domainOBJ = domainName()
    domainOBJ.getDomain()
