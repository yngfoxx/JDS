# https://websockets.readthedocs.io/en/stable/intro.html
import asyncio
import signal
import datetime
import random
import json
import websockets
import sys
import tempfile

from engine.platform import domainName
from tornado.platform.asyncio import AnyThreadEventLoopPolicy

# https://github.com/tornadoweb/tornado/issues/2531
asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

domainObject = domainName()
hostdomain = str(domainObject.getDomain())
JDS_PAYLOAD_FILE = tempfile.TemporaryFile(prefix='jds_', suffix='_payload.json')
clients = set()

class websocketserver():
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.stopped = False

    async def main(self, websocket, path):
        while self.stopped == False:
            # await websocket.send("connected")
            clients.add(websocket)
            try:
                # Recieve input from web client ------------------------------->
                wsInput = await websocket.recv()

                # Handle websocket recieved input
                wsRequest = json.loads(wsInput)
                action = wsRequest['action']
                interval = wsRequest['interval']

                print("[+] Action:"+action+"; Interval:"+interval);

                # jds_client_connected
                if action == 'jds_client_connected':
                    payload = str(wsRequest['payload'])
                    # save payload in temporary file -------------------------->
                    JDS_PAYLOAD_FILE.write(str.encode(payload))
                    print("[+] Payload stored!")
                    # await asyncio.wait([websocket.send("jds_client_connected_true") for websocket in clients])
                    # --------------------------------------------------------->

                # desktop_client_online
                elif action == 'desktop_client_online':
                    print('[+] Desktop socket is now connected')
                    JDS_PAYLOAD_FILE.seek(0)
                    pLoad = JDS_PAYLOAD_FILE.read().decode('utf-8')
                    CLIENT_PAYLOAD = {
                        'channel': "desktop_client",
                        'payload': pLoad
                    }
                    CLIENT_PAYLOAD_JSON = json.dumps(CLIENT_PAYLOAD)
                    await asyncio.wait([ws.send(CLIENT_PAYLOAD_JSON) for ws in clients])
                    # send network data back to client

                # ------------------------------------------------------------->
                await asyncio.sleep(random.random() * 3)

            except websockets.exceptions.ConnectionClosedOK:
                print("[+] Connection closed")

            finally:
                clients.remove(websocket)
                # JDS_PAYLOAD_FILE.close()


    async def initialize(self, stop):
        # self.server = websockets.serve(self.main, hostdomain, self.port)
        async with websockets.serve(self.main, hostdomain, self.port):
            await stop



    def start(self):
        self.loop = asyncio.get_event_loop()

        # The stop condition is set when receiving SIGTERM.
        self.futurestop = self.loop.create_future()
        # loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

        print("[+] Created socket server on port: 5678")
        asyncio.get_event_loop().run_until_complete(self.initialize(self.futurestop))



    def close(self):
        # Stop while loop in main()
        self.stopped = True

        # Stop future loop to terminate the program
        self.futurestop.set_result(True)


if __name__ == '__main__':
    socketserver = websocketserver(5678)
    socketserver.initialize()
