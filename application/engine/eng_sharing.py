import os
import sys
import time
import requests
import argparse
import json
import hashlib
import threading
import asyncio
import websockets
import random
import string

from queue import Queue
from pySmartDL import SmartDL
from concurrent.futures import ThreadPoolExecutor

from engine.eng_standard import stdlib
from engine.eng_platform import domainName


serverDomain = domainName()
stdlib = stdlib()
_executor = ThreadPoolExecutor(1)

# Sharing manager client web socket class handler
class sharingManagerSS():
    def __init__(self):
        super().__init__()
        self.ws = None
        self.uri = "ws://localhost:5678"
        self.connected = True
        self.keepAlive = True
        self.socket_id = stdlib.makeRandomKey(12)
        self.sharingQueue = Queue()
        self.networkList = {}
        self.jointList = set()
        self.threads = []
        self.init = False
        self.u_config_data = None


    async def connectSocketServer(self):
        async with websockets.connect(self.uri, ping_interval=None) as websocket:
            self.ws = websocket
            self.connected = True
            self.socket_payload = json.dumps({ "action": "sharing_manager_connected", "socketType": "sharing_mngr",  "socketID": self.socket_id })
            # sharing manager is now connected
            await websocket.send(self.socket_payload)
            while self.connected == True:
                try:
                    wsInput = await websocket.recv()

                    if wsInput != None:
                        wsRequest = json.loads(wsInput)
                        if 'sMNGR' in wsRequest:
                            if wsRequest['sMNGR'] == "save_sharing_info":
                                print('\n[!] Update sharing manager')
                                self.updateNetList(wsRequest['payload']);

                            elif wsRequest['sMNGR'] == "exit":
                                # exit loop to terminate script
                                self.connected = False
                                self.keepAlive = False
                                break

                        elif self.socket_id in wsRequest:
                            print('[!] Sharing manager received:', wsRequest)

                except Exception as e:
                    print('[-] Error in sharing manager socket connection')
                    print(e)
                    # self.connected = False
                    pass

                await asyncio.sleep(random.random() * 3)


    # Connect socket
    def connect(self):
        print('[!] Connecting sharing manager...')
        while self.keepAlive == True:
            self.loop = asyncio.new_event_loop()
            self.loop.run_until_complete(self.connectSocketServer())
            self.loop.close()
        print('[!] Sharing manager exited')


    # Update network list
    def updateNetList(self, networkList):
        for user in networkList:
            print('[!] New network list: ', networkList[user])
            self.networkList[user] = networkList[user]

        # get user config data to update joint list
        if os.path.exists("u_config.json"):
            uConfig = open('u_config.json', 'r')
            self.u_config_data = json.loads(uConfig.read());
            uConfig.close()
            print('[!] User configuration: ', self.u_config_data)
        else:
            print('[!] Could not find u_config.json')

        if self.init == False:
            print('[!] Initialize file sharing')
            self.init = True
            self.initFileSharing()


    def initFileSharing(self):
        print('[+] File sharing initialized')
        if self.u_config_data != None:
            tempJointList = self.u_config_data['joints']
            print('\n[+++] J0INTs for file sharing:', tempJointList)
            for jds in tempJointList:
                print('[+++] JDS: ', jds['jid'])
                print('[+++] role: ', jds['role'])
                print('[+++] user: ', jds['uid'])
                print('\n')
                if jds['role'] == 'owner':
                    # add J0INTs owned by user
                    self.jointList.add(jds['jid'])
        else:
            print('[---] No J0INTs available')

        if len(self.jointList) > 0:
            # get config data of joints from network users
            for J0INT in self.jointList:
                print(J0INT)
        print('\n')
