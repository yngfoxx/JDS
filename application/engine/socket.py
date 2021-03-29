# https://websockets.readthedocs.io/en/stable/intro.html
import asyncio
import signal
import datetime
import random
import json
import socket
import websockets
import sys
import tempfile

from engine.platform import domainName
from engine.server import lanServer

# https://github.com/tornadoweb/tornado/issues/2531
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())


domainObject = domainName()
hostdomain = str(domainObject.getDomain())
# self.payload_file = tempfile.TemporaryFile(prefix='jds_', suffix='_payload.json')
clients = set()
connections = {}

class websocketserver():
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.stopped = False
        self.payload_file = tempfile.TemporaryFile(prefix='jds_', suffix='_payload.json')

    def clients_event(self):
        return json.dumps({"type": "client", "count": len(clients)})


    async def notify_clients(self):
        if clients:  # asyncio.wait doesn't accept an empty list
            message = self.clients_event()
            await asyncio.wait([ws.send(message) for ws in clients])


    # Register the websocket
    async def register(self, websocket):
        clients.add(websocket)
        await self.notify_clients()


    # Unregister the websocket
    async def unregister(self, websocket):
        clients.remove(websocket)
        await self.notify_clients()


    # Register the WebSocket with a socket ID
    async def addSocket(self, websocket, socketID, socketType):
        print("[+] New WebSocket connection: ", socketID)
        connections[str(socketID)] = { "socket": websocket, "type": socketType }
        for ws in connections:
            print("[!] ", ws, " => ", connections[ws])
            if (connections[ws]["socket"].closed == True):
                print("[+] ", ws, " is closed, removing from connection list")
                self.removeSocket(connections[ws], ws)


    # Unregister the WebSocket with a socket ID
    async def removeSocket(self, WebSocket, socketID):
        connections.pop(str(socketID))
        print("[+] A WebSocket connection closed")


    async def main(self, websocket, path):
        while self.stopped == False:
            # await websocket.send("connected")
            # clients.add(websocket)
            await self.register(websocket)
            try:
                # Recieve input from web client ------------------------------->
                wsInput = await websocket.recv()

                # Handle websocket recieved input
                wsRequest = json.loads(wsInput)
                action = wsRequest['action']
                print("[+] Action: "+action);

                # interval = wsRequest['interval']

                # jds_client_connected
                if action == 'jds_client_connected':
                    await self.addSocket(websocket, wsRequest['socketID'], wsRequest['socketType'])

                    # save payload in temporary file -------------------------->
                    payload = str(wsRequest['payload'])
                    self.payload_file.write(str.encode(payload))
                    print("[+] Payload stored!")

                    self.payload_file.seek(0)
                    pLoad = self.payload_file.read().decode('utf-8')
                    pLoad = pLoad.replace("\'", "\"")

                    # local_ip = socket.gethostbyname(socket.gethostname())
                    local_ip = lanServer().get_ip_list()
                    CLIENT_PAYLOAD = {
                        "channel": "desktop_client_connected",
                        "net_addr": local_ip,
                        "payload": pLoad
                    }
                    CLIENT_PAYLOAD_JSON = json.dumps(CLIENT_PAYLOAD)
                    try:
                        await asyncio.wait([ws.send(CLIENT_PAYLOAD_JSON) for ws in clients])
                    except:
                        pass
                    # --------------------------------------------------------->

                # desktop_client_online
                elif action == 'desktop_client_online':
                    await self.addSocket(websocket, wsRequest['socketID'], wsRequest['socketType'])

                    print('[+] Desktop socket connected to socket server')
                    self.payload_file.seek(0)
                    pLoad = self.payload_file.read().decode('utf-8')
                    pLoad = pLoad.replace("\'", "\"")

                    # local_ip = socket.gethostbyname(socket.gethostname())
                    local_ip = lanServer().get_ip_list()
                    CLIENT_PAYLOAD = {
                        "channel": "desktop_client_connected",
                        "net_addr": local_ip,
                        "payload": pLoad
                    }
                    CLIENT_PAYLOAD_JSON = json.dumps(CLIENT_PAYLOAD)
                    try:
                        await asyncio.wait([ws.send(CLIENT_PAYLOAD_JSON) for ws in clients])
                        # await asyncio.wait(websocket.send(CLIENT_PAYLOAD_JSON))
                    except:
                        pass
                    # send data back to client

                elif action == 'fetch_network_users':
                    print('[+] WebSocket request: '+action)
                    print(wsRequest['list'])
                    print('SOCKET_ID => ', wsRequest['socketID'])
                    print('LOCAL_IP => ', wsRequest['netAddr'])
                    # get  local ip of all users of the same Joint group
                    for ws in connections:
                        ws = connections[ws]['socket']
                        # point to [web] socket
                        if ws != websocket:
                            WEB_PAYLOAD = {
                                "channel": "net_scanner",
                                "groups": wsRequest['list'],
                                "net_addr": wsRequest['netAddr']
                            }
                            WEB_PAYLOAD_JSON = json.dumps(WEB_PAYLOAD)
                            await asyncio.wait([ws.send(WEB_PAYLOAD_JSON)])


                elif action == 'refresh_webview':
                    print('[+] Refresh webview command sent!')
                    for ws in connections:
                        ws = connections[ws]['socket']
                        # point to [web] socket
                        if ws != websocket:
                            WEB_PAYLOAD = { "channel": "refresh" }
                            WEB_PAYLOAD_JSON = json.dumps(WEB_PAYLOAD)
                            await asyncio.wait([ws.send(WEB_PAYLOAD_JSON)])

                elif action == 'jds_client_disconnected':
                    await self.removeSocket(websocket, wsRequest['socketID'])
                    print('[!] User logged out!')
                    CLIENT_PAYLOAD = { "channel": "desktop_client_disconnected", "socket": wsRequest['socketID'] }
                    CLIENT_PAYLOAD_JSON = json.dumps(CLIENT_PAYLOAD)

                    try:
                        await asyncio.wait([ws.send(CLIENT_PAYLOAD_JSON) for ws in clients])
                    except:
                        pass
                # ------------------------------------------------------------->
                await asyncio.sleep(random.random() * 3)


            # except websockets.exceptions.ConnectionClosedOK:
            #     print("[+] WebSocket connection closed")
            #     continue
            #
            # except websockets.exceptions.ConnectionClosedError:
            #     print("[+] WebSocket connection error: [Expected]")


            finally:
                self.payload_file.seek(0)
                self.payload_file.truncate()
                await self.unregister(websocket)


    async def initialize(self, stop):
        self.ws = websockets.serve(self.main, hostdomain, self.port)
        async with self.ws:
            await stop



    def start(self):
        self.stopped = False
        # The stop condition is set when receiving SIGTERM.
        # https://docs.python.org/3/library/asyncio-future.html#asyncio.Future
        self.loop = asyncio.get_event_loop()
        self.futurestop = self.loop.create_future()
        # self.loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

        print("[+] Created socket server on port: 5678")
        asyncio.get_event_loop().run_until_complete(self.initialize(self.futurestop))



    def close(self):
        try:
            self.stopped = True # Stop while loop in main()
            self.futurestop.set_result(True) # Stop future loop to terminate the program
            # self.payload_file.close()
            print("[+] WebSocket server stopped")
        except:
            pass


if __name__ == '__main__':
    socketserver = websocketserver(5678)
    socketserver.initialize()
