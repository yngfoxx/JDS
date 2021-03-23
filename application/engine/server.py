# Python 3 server example ----------------------------------------------------->
# https://pythonbasics.org/webserver/
# ----------------------------------------------------------------------------->
import socketserver
import time
import sys
import json
import http.server
from io import BytesIO
from sys import platform
from os import curdir, sep
from http.server import SimpleHTTPRequestHandler, HTTPServer
from engine.platform import domainName


PORT = 8000
domainObject = domainName()
hostName = str(domainObject.getDomain())

# 79 6f 75 6e 67 | 66 6f 78
# 76766 - 65535 (MAX) = 11231

class LocalServer(SimpleHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

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

            elif self.path.endswith(".tff"):
                f = open(curdir + sep + self.path, "rb")
                self.send_response(200)
                self.send_header("Content-type", "font/ttf")
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

        except IOError:
            print("[!] 404 - file not found")
            self.send_error(404, "File Not Found: %s" % self.path)


    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # print("POST request,\nPath:", str(self.path), "\nHeaders: {", str(self.headers),"\n}\nBody: {\n", post_data.decode('utf-8'),"\n}")
        self._set_response()

        post_data = json.loads(post_data.decode('utf-8'))
        print(post_data)
        # Handle request before returning response
        if post_data['event'] == 'sonar':
            self.wfile.write(b"POST request for LAN sonar recieved!")



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
        print("[+] LAN server stopped")


if __name__ == "__main__":
    try:
        lanServer.start()
    except keyboardinterrupt:
        pass

    sys.exit(lanServer.stop())
