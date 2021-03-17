import asyncio
import datetime
import random
import json
import websockets

from engine.platform import domainName
from tornado.platform.asyncio import AnyThreadEventLoopPolicy

# https://github.com/tornadoweb/tornado/issues/2531
asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

domainObject = domainName()
hostdomain = domainObject.getDomain()

class websocketserver():
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.stopped = False

    async def main(self, websocket, path):
        while self.stopped == False:
            # await websocket.send("connected")
            try:
                # Recieve input from web client ------------------------------->
                wsInput = await websocket.recv()

                # Handle websocket recieved input
                wsRequest = json.loads(wsInput)
                action = wsRequest['action']
                interval = wsRequest['interval']

                print("[+] Action:"+action+"; Interval:"+interval)

                # client_connected
                # get_lan_hosts

                # ------------------------------------------------------------->
            except:
                print("[!] Error while waiting for user request")

            await asyncio.sleep(random.random() * 3)

    def initialize(self):
        self.server = websockets.serve(self.main, hostdomain, self.port)

        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    def close(self):
        self.stopped = True
        try:
            websockets.close()
            asyncio.get_event_loop().close()
        except:
            print("[!] Error while closing web socket in socket.py")


if __name__ == '__main__':
    socketserver = websocketserver(5678)
    socketserver.initialize()
