# Python 3 server example ----------------------------------------------------->
# https://pythonbasics.org/webserver/
# ----------------------------------------------------------------------------->
from os import curdir, sep
import http.server
from http.server import SimpleHTTPRequestHandler, HTTPServer
import socketserver
import time
import sys

hostName = "127.0.0.1"
PORT = 8000
# 79 6f 75 6e 67 | 66 6f 78
# 76766 - 65535 (MAX) = 11231

class LocalServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith(".html"):
                f = open(curdir + sep + self.path, "rb")
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            elif self.path.endswith(".less"):
                f = open(curdir + sep + self.path, "rb")
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            elif self.path.endswith(".css"):
                f = open(curdir + sep + self.path, "rb")
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            elif self.path.endswith(".js"):
                f = open(curdir + sep + self.path, "rb")
                self.send_response(200)
                self.send_header("Content-type", "text/javascript")
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

        except IOError:
            print("[!] 404 - file not found")
            self.send_error(404, "File Not Found: %s" % self.path)


class lanServer():
    def __init__(self):
        super().__init__()

    def start(self):
        self.server = socketserver.TCPServer(("", PORT), LocalServer)
        print("[+] LAN server started.")
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        print("[+] LAN server stopped.")


if __name__ == "__main__":
    try:
        lanServer.start()
    except keyboardinterrupt:
        pass

    sys.exit(lanServer.stop())