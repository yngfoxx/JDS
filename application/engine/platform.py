from sys import platform

class domainName(object):
    def __init__(self):
        super(domainName, self).__init__()

    def getDomain(self):
        if platform == "linux" or platform == "linux2":
            # Linux OS
            self.domain = "localhost"
        elif platform == "darwin":
            # OS X
            self.domain = "192.168.64.2"
        elif platform == "win32":
            # Windows
            self.domain = "localhost"
        return str(self.domain)

if __name__ == '__main__':
    domainOBJ = domainName()
    domainOBJ.getDomain()
