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
import requests
import time
import os
import threading

try:
    import thread
except ImportError:
    import _thread as thread

from engine.eng_standard import stdlib
from engine.eng_server import lanServer
from engine.eng_platform import domainName
# from engine.eng_downloader import downloadManagerSS

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
        self.payload_file = tempfile.NamedTemporaryFile(prefix='jds_', suffix='_payload.json')
        self.local_net_scanner = True
        self.init = True


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


    # Unregister the WebSocket with a socket ID
    def removeSocket(self, WebSocket, socketID):
        connections.pop(str(socketID))
        print("[+] A WebSocket connection closed")
        print(clients)


    # Register the WebSocket with a socket ID
    def addSocket(self, websocket, socketID, socketType):
        print("[+] New WebSocket connection: ", socketID)
        connections[str(socketID)] = { "socket": websocket, "type": socketType }
        for ws in connections:
            print("[!] ", ws, " => ", connections[ws])
            if connections[ws]["socket"].closed == True or not connections[ws]["socket"]:
                print("[+] ", ws, " is closed, removing from connection list")
                self.removeSocket(connections[ws], ws)



    async def main(self, websocket, path):
        while self.stopped == False and self.init == True:
            # await websocket.send("connected")
            # clients.add(websocket)
            await self.register(websocket)
            try:
                wsInput = None
                # Recieve input from web client ------------------------------->
                try:
                    wsInput = await websocket.recv()
                except Exception as e:
                    print('[-] Could not receive websocket data, reason:', e)
                    for sock in connections:
                        if connections[sock]['socket'] == websocket:
                            print('[!] Socket error origin:', websocket, '\n[!] SEO type:', connections[sock]['type']+'\n')

                    break

                # Handle websocket recieved input
                wsRequest = json.loads(wsInput)
                if 'action' in wsRequest and wsInput != None:
                    action = wsRequest['action']
                    print("[+] Action: "+action);

                    # jds_client_connected
                    if action == 'jds_client_connected':
                        self.addSocket(websocket, wsRequest['socketID'], wsRequest['socketType'])

                        # save payload in temporary file -------------------------->
                        payload = str(wsRequest['payload'])
                        self.payload_file.truncate()
                        self.payload_file.write(str.encode(payload))
                        print("[+] Payload stored in temp file!")

                        self.payload_file.seek(0)
                        pLoad = self.payload_file.read().decode('utf-8')
                        pLoad = pLoad.replace("\'", "\"")

                        # Store uconfig in lan server -----------------------------
                        lanServer().set_uconfig(pLoad)

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


                    if action == "jds_client_refresh":
                        # save payload in temporary file -------------------------->
                        payload = str(wsRequest['payload'])
                        self.payload_file.truncate()
                        self.payload_file.write(str.encode(payload))
                        print("[+] Payload stored in temp file!")

                        self.payload_file.seek(0)
                        pLoad = self.payload_file.read().decode('utf-8')
                        pLoad = pLoad.replace("\'", "\"")

                        # Store uconfig in lan server -----------------------------
                        lanServer().set_uconfig(pLoad)

                        # local_ip = socket.gethostbyname(socket.gethostname())
                        local_ip = lanServer().get_ip_list()
                        CLIENT_PAYLOAD = {
                            "channel": "desktop_client_refresh",
                            "net_addr": local_ip,
                            "payload": pLoad
                        }
                        CLIENT_PAYLOAD_JSON = json.dumps(CLIENT_PAYLOAD)
                        try:
                            await asyncio.wait([ws.send(CLIENT_PAYLOAD_JSON) for ws in clients])
                        except:
                            pass
                        # --------------------------------------------------------->


                    # App is now connected to websocket
                    elif action == 'desktop_client_online':
                        self.addSocket(websocket, wsRequest['socketID'], wsRequest['socketType'])

                        print('[+] Desktop socket connected to local socket server')
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
                        print('[!] Sent: desktop_client_connected')


                    # Fetch users on local network
                    elif action == 'fetch_network_users':
                        print('[+] WebSocket request: '+action)
                        print(wsRequest['list'])
                        print('[!] SOCKET_ID => ', wsRequest['socketID'])
                        print('[!] LOCAL_IP => ', wsRequest['netAddr'])
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


                    # Scan users on local network
                    elif action == 'scan_network_users':
                        # Use payload to scan given IP's on local network
                        # print(wsRequest['payload'])
                        attempts = 0
                        self.local_net_scanner = True

                        while self.local_net_scanner == True:
                            time.sleep(20)
                            attempts += 1
                            print('[+] SCANNING JOINT USERS ON NETWORK (', attempts, '/ 1 )\n')

                            for jointGrp in wsRequest['payload']:
                                print("[!] SENDING POST", jointGrp, "="*90)
                                local_ip = lanServer().get_ip_list()

                                if not os.path.exists("u_config.json"):
                                    self.stop()
                                    break

                                uconfigFile = open("u_config.json", 'r')
                                uconfigData = json.loads(uconfigFile.read())
                                uconfigFile.close()

                                for userData in wsRequest['payload'][jointGrp]:
                                    for addr in userData['user_net_addr']:
                                        if addr == '':
                                            print("[!] ERROR: empty address found!")
                                            continue

                                        targetDomain = 'http://'+str(addr)+':8000'
                                        print('[!] TARGET => ', targetDomain)

                                        payload = { 'event': 'sonar', 'origin_joint': jointGrp, 'origin_addr': local_ip }
                                        payload['origin_uid'] = uconfigData['userID'] # belongs to host
                                        payload['origin_uname'] = uconfigData['username'] # belongs to host

                                        origin_joints = json.loads(str(uconfigData['joints']).replace("\'", "\""))
                                        for jnt in origin_joints:
                                            if jnt['jid'] == payload['origin_joint']:
                                                payload['joint_role'] = jnt['role']
                                                break

                                        cHeaders = { 'user-agent': 'JDS/0.0.1', 'content-type': 'application/json' }
                                        time.sleep(0.5)

                                        # Begin LAN handshake ----------------------------------------------------------->
                                        response = None
                                        try:
                                            req = requests.post(targetDomain, data=json.dumps(payload), headers=cHeaders, timeout=(2, 5))
                                            if req.status_code == 200:
                                                response = json.loads(req.text)
                                                print('[!] RESPONSE => ', response)
                                            req.close()
                                        except Exception as e:
                                            # print(e)
                                            print('[-] Request from ',targetDomain,'responded unexpectedly')

                                        if response != None:
                                            for ws in connections:
                                                ws = connections[ws]['socket']
                                                # point to [web] socket
                                                if ws != websocket:
                                                    WEB_PAYLOAD = {
                                                        "channel": "net_user_discovered",
                                                        "payload": response
                                                    }
                                                    WEB_PAYLOAD_JSON = json.dumps(WEB_PAYLOAD)
                                                    await asyncio.wait([ws.send(WEB_PAYLOAD_JSON)])
                                                    print('[!] Net user discovered')
                                        # ------------------------------------------------------------------------------->

                                print("="*114, '\n')

                            # Increment net scan attempts
                            if attempts >= 1:
                                print("[*] Local network scanner completed!")
                                self.local_net_scanner = False
                                for ws in connections:
                                    ws = connections[ws]['socket']
                                    # point to [web] socket
                                    if ws != websocket:
                                        WEB_PAYLOAD = {
                                            "channel": "net_scanner_completed",
                                            "payload": {"foo": "bar"}
                                        }
                                        WEB_PAYLOAD_JSON = json.dumps(WEB_PAYLOAD)
                                        await asyncio.wait([ws.send(WEB_PAYLOAD_JSON)])
                                break


                    # Refresh webview data
                    elif action == 'refresh_webview':
                        print('[+] Refresh webview command sent!')
                        for ws in connections:
                            ws = connections[ws]['socket']
                            # point to [web] socket
                            if ws != websocket:
                                WEB_PAYLOAD = { "channel": "refresh" }
                                WEB_PAYLOAD_JSON = json.dumps(WEB_PAYLOAD)
                                await asyncio.wait([ws.send(WEB_PAYLOAD_JSON)])


                    # Fetch J0INT download info
                    elif action == 'update_download_manager':

                        print('[!] Updating download manager...')
                        # Send request to web app
                        for ws in connections:
                            ws = connections[ws]['socket']
                            # point to [web] socket
                            if ws != websocket:
                                WEB_PAYLOAD = {
                                    "channel": "fetch_download_info",
                                    "payload": wsRequest['payload'],
                                    "socketid": wsRequest['sid']
                                }
                                WEB_PAYLOAD_JSON = json.dumps(WEB_PAYLOAD)
                                await asyncio.wait([ws.send(WEB_PAYLOAD_JSON)])


                    # Add download manager to socket connections
                    elif action == 'download_manager_connected':
                        print('[+] Download manager connected')
                        self.addSocket(websocket, wsRequest['socketID'], wsRequest['socketType'])
                        for ws in connections:
                            wsType = connections[ws]['type']
                            ws = connections[ws]['socket']
                            # point to [web] socket
                            if wsType != 'download_mngr':
                                WEB_PAYLOAD = {
                                "channel": "download_manager_connected",
                                "socketID": wsRequest['socketID']
                                }
                                WEB_PAYLOAD_JSON = json.dumps(WEB_PAYLOAD)
                                await asyncio.wait([ws.send(WEB_PAYLOAD_JSON)])


                    elif action == 'download_manager_data':
                        print('[+] Fill download manager');
                        print(wsRequest['payload']);
                        # initialize download manager
                        for jid in wsRequest['payload']:
                            jointPayload = wsRequest['payload'][jid]
                            print('[+] Download manager on J0INT:', jid);
                            dArgSet = []
                            for chunk in wsRequest['payload'][jid]:
                                if os.path.exists("u_config.json"):
                                    uconfigFile = open("u_config.json", 'r')
                                    uconfigData = json.loads(uconfigFile.read())
                                    uconfigFile.close()

                                    # Only download chunks assigned to the user
                                    if uconfigData['userID'] == chunk['uid']:
                                        dArg = {
                                            'jid' : jid,
                                            'rid' : chunk['rid'],
                                            'cid' : chunk['cid'],
                                            'order' : chunk['order'],
                                            'byte_start' : chunk['byte_start'],
                                            'byte_end' : chunk['byte_end'],
                                        }
                                        dArgSet.append(dArg)

                            for program in connections:
                                wsType = connections[program]['type']
                                ws = connections[program]['socket']
                                # point to [dMNGR] socket
                                DMNGR_PAYLOAD = { "dMNGR": "validate_download_data", "payload": dArgSet }
                                DMNGR_PAYLOAD_JSON = json.dumps(DMNGR_PAYLOAD)
                                # /storage/JointID/RequestID/Arch_JointID_RequestID.zip
                                await asyncio.wait([ws.send(DMNGR_PAYLOAD_JSON)])
                            await asyncio.sleep(random.random() * 3)


                    # Get realtime chunk download progress from download manager
                    elif action == 'realtime_download_progress':
                        print('[+] Live chunk download progress received')
                        await asyncio.sleep(random.random() * 3)
                        wsPload = {}
                        for wsData in wsRequest:
                            if wsData != 'action':
                                wsPload[wsData] = wsRequest[wsData]

                        wsPload['channel'] = 'realtime_download_progress'
                        # print(wsPload)
                        for wSKT in connections:
                            wsType = connections[wSKT]['type']
                            ws = connections[wSKT]['socket']
                            # point to [desktop] socket
                            if wsType == 'desktop':
                                WEB_PAYLOAD_JSON = json.dumps(wsPload)
                                await asyncio.wait([ws.send(WEB_PAYLOAD_JSON)])


                    elif action == 'jds_client_disconnected':
                        self.removeSocket(websocket, wsRequest['socketID'])
                        print('[!] User logged out!')
                        # Delete u_config.json
                        if os.path.exists("u_config.json"):
                            os.remove("u_config.json")
                        else:
                            print("[!] User configuration could not be located")

                        CLIENT_PAYLOAD = { "channel": "desktop_client_disconnected", "socket": wsRequest['socketID'] }
                        CLIENT_PAYLOAD_JSON = json.dumps(CLIENT_PAYLOAD)

                        try:
                            await asyncio.wait([ws.send(CLIENT_PAYLOAD_JSON) for ws in clients])
                        except:
                            pass


                    elif action == 'exit':
                        print('[!] Closing all multi-threaded programs')

                    # ------------------------------------------------------------->

                    await asyncio.sleep(random.random() * 3)


            except websockets.exceptions.ConnectionClosedOK:
                print("[+] WebSocket connection closed")
                if self.init == True:
                    self.stopped = True
                    # self.close()
                continue

            except websockets.exceptions.ConnectionClosedError:
                print("[+] WebSocket connection error: [Expected]")
                if self.init == True:
                    self.stopped = True
                    # self.close()
                continue


            finally:
                self.payload_file.seek(0)
                self.payload_file.truncate()
                await self.unregister(websocket)


    async def initialize(self, stop):
        self.ws = websockets.serve(self.main, hostdomain, self.port)


    def start(self):
        # The stop condition is set when receiving SIGTERM.
        # https://docs.python.org/3/library/asyncio-future.html#asyncio.Future
        self.stopped = False

        self.loop = asyncio.get_event_loop()
        self.start_server = websockets.serve(self.main, hostdomain, self.port, ping_interval=None)

        # self.futurestop = self.loop.create_future()
        # self.loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

        print("[+] Created socket server on port: 5678")
        # asyncio.get_event_loop().run_until_complete(self.initialize(self.futurestop))

        self.loop.run_until_complete(self.start_server)
        self.loop.run_forever()
        print('[!] Socket server has shutdown')
        print('[!] Application status:', self.init)

    async def gracefulExit(self):
        for wSKT in connections:
            wsType = connections[wSKT]['type']
            ws = connections[wSKT]['socket']

            SOCKT_PAYLOAD = { "channel": "exit" } if wsType == 'desktop' else  { "dMNGR": "exit" }
            SOCKT_PAYLOAD_JSON = json.dumps(SOCKT_PAYLOAD)
            await asyncio.wait([ws.send(SOCKT_PAYLOAD_JSON)])
            await asyncio.sleep(1)
            print("[+] Exit signal sent to a socket")

    def close(self):
        asyncio.run(self.gracefulExit())
        self.init = False
        try:
            # self.futurestop.set_result(True) # Stop future loop to terminate the program
            # self.futurestop.cancel("[!] Loop cancelled.")
            self.loop.stop()
            self.local_net_scanner = False
            self.stopped = True # Stop while loop in main()
            # self.payload_file.close()
            print("[!] Stopping socket server")
        except e:
            print('[-] Error while closing socket: ', e)


    def restart(self):
        print('[!] Restarting socket server')
        try:
            # self.futurestop.set_result(True) # Stop future loop to terminate the program
            # self.futurestop.cancel("[!] Loop cancelled.")
            self.loop.stop()
            self.local_net_scanner = False
            self.stopped = True # Stop while loop in main()
            # self.payload_file.close()
            print("[!] Stopping socket server")
        except e:
            print('[-] Error while closing socket: ', e)

        time.sleep(10)

        print('[!] Restarting websocket...')
        self.start()



if __name__ == '__main__':
    socketserver = websocketserver(5678)
    socketserver.initialize()
