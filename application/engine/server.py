# Python 3 server example ----------------------------------------------------->
# https://pythonbasics.org/webserver/
# ----------------------------------------------------------------------------->
import socketserver
import time
import sys
import json
import cgi
import http.server
from io import BytesIO
from sys import platform
from os import curdir, sep

from http.server import SimpleHTTPRequestHandler, HTTPServer
from engine.platform import domainName

# https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
from netifaces import interfaces, ifaddresses, AF_INET


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
        content_length = int(self.headers['Content-Length']) # <--- Gets the data
        content_type = str(self.headers['content-type']) # <--- Gets the content-type of the data
        user_agent = str(self.headers['user-agent']) # <--- Gets the content-type of the data

        recvd_payload = self.rfile.read(content_length) # <--- Gets the data itself

        print('[POST] ', '*'*72)

        # print("[!] Headers: {\n", str(self.headers), "}") # <--- print all headers

        # authentication ------------------------------------------------------>
        if content_type != 'application/json' and user_agent == 'JDS/0.0.1':
            self.send_response(400)
            self.end_headers()
            return

        # print("POST request,\nPath:", str(self.path), "\nHeaders: {", str(self.headers),"\n}\nBody: {\n", recvd_payload.decode('utf-8'),"\n}")
        # --------------------------------------------------------------------->


        # property handling --------------------------------------------------->
        rData = json.loads(recvd_payload.decode('utf-8'))
        rData['received'] = 'ok'
        # --------------------------------------------------------------------->


        # Return message ------------------------------------------------------>
        self._set_response()
        print(json.dumps(rData))
        self.wfile.write(str.encode(json.dumps(rData)))
        # --------------------------------------------------------------------->

        print('*'*80, '\n')


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


    def get_ip_list(self):
        list = []
        for ifName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifName).setdefault(AF_INET, [{'addr':'none'}] )]
            # print( '%s: %s' % (ifName, ', '.join(addresses)) )
            if addresses[0] != 'none' and addresses[0] != '127.0.0.1':
                list.append(addresses[0])
        return list


if __name__ == "__main__":
    try:
        lanServer.start()
    except Exception:
        pass

    sys.exit(lanServer.stop())
