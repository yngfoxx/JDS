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
threads = []

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

                            elif wsRequest['sMNGR'] == "init":
                                # Initialize from socket
                                self.init = False
                                break

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
        # Compare network list
        for user in networkList:
            if not self.networkList:
                self.networkList[user] = networkList[user]
            elif self.networkList[user] != networkList[user]:
                print('[!] New network list: ', networkList[user])
                self.networkList[user] = networkList[user]
                self.init = False

        # get user config data to update joint list
        if os.path.exists("u_config.json"):
            uConfig = open('u_config.json', 'r')
            self.u_config_data = json.loads(uConfig.read());
            uConfig.close()
            print('[!] User configuration: ', self.u_config_data)
        else:
            print('[!] Could not find u_config.json')

        self.initFileShareSeeker()

        # if self.init == False:
        #     print('[!] Initialize file sharing')
        #     self.init = True
        #     self.initFileShareSeeker()


    # initiatialize file sharing seeker
    def initFileShareSeeker(self):
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
                for usr in self.networkList:
                    inJoint = False
                    for usrJoint in self.networkList[usr]['joints']:
                        if usrJoint['jid'] == J0INT:
                            inJoint = True

                    if inJoint == True:
                        # Create threads to handle file downloading
                        print('[!] J0INT member found: ', self.networkList[usr]['netAddr'])
                        usrIPaddress = self.networkList[usr]['netAddr'][0]

                        # Get jconf.json
                        # uri = "http://"+usrIPaddress+":8000/?req=jconf&jds="+J0INT
                        uri = "http://"+usrIPaddress+":8000/storage/"+J0INT+"/jconf.json"
                        print('[!] J0INT config uri:', uri)
                        reqJCONF = requests.get(uri)
                        thPayload = json.loads(reqJCONF.text)
                        thPayload.append({"source": usrIPaddress})

                        self.sharingManager(thPayload)

                        # logger = open('log_'+J0INT+'.txt', 'w')
                        # logger.write(json.dumps(thPayload))
        print('\n')


    # Thread worker ----------------------------------------------------------->
    def worker(self):
        while True:
            sQueueItem = self.sharingQueue.get()
            try:
                # https://www.aeracode.org/2018/02/19/python-async-simplified/
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self.fileSeeker(sQueueItem))
            except Exception as e:
                print('[!] Error in worker:', e)

            self.sharingQueue.task_done()
            print('[+] A task completed..')
    # ------------------------------------------------------------------------->


    # Queue manager ----------------------------------------------------------->
    def sharingManager(self, dArg):
        workerIndex = 0
        goalSource = None
        jointArr = []

        for x in dArg:
            if 'source' in x:
                goalSource = x['source']
            else:
                jointArr.append(x)

        for sParm in jointArr:
            sParm['source'] = goalSource
            self.sharingQueue.put(sParm)
            print("[!] Shared file added to que")

            workerThread = threading.Thread(target=self.worker, name=f'worker_{workerIndex}', daemon=True)
            workerThread.start()
            self.threads.append(workerThread)

            # block until all tasks are done
            self.sharingQueue.join()

        print('[!] File sharing completed')
        print('[!] All file downloads ended, validating files...')
        self.makeFile(jointArr[0]['jid'], jointArr[0]['rid'])
    # ------------------------------------------------------------------------->


    # File seeker ------------------------------------------------------------->
    async def fileSeeker(self, arg):
        if self.ws != None:
            print('[!] WebSocket is accessible:', self.ws)

        # Arguments ---------------------------------------------------------------\/
        jointID = arg['jid']
        requestID = arg['rid']
        chunkID = arg['cid']
        orderID = int(arg['oid'])
        uDomain = arg['source']


        # Create storage folder if missing
        if os.path.exists("storage") == False:
            os.mkdir("storage")

        # Create J0INT directory if missing
        storage = "storage/"+jointID
        if os.path.exists(storage) == False:
            os.mkdir(storage)

        # Create request directory if missing
        storage = "storage/" + jointID + "/" + requestID
        if os.path.exists(storage) == False:
            os.mkdir(storage)


        uri = "http://"+uDomain+":8000/storage/" + jointID + "/" + requestID + "/Chnk_"+jointID+"_"+requestID+"_"+chunkID+"_"+str(orderID)+".J0INT"
        dest = "storage/" + jointID + "/" + requestID
        seekPATH = dest + "/Chnk_"+jointID+"_"+requestID+"_"+chunkID+"_"+str(orderID)+".J0INT"
        seekCONF = dest + "/config.json"


        # Chunk/Seek config data
        seekJSON = {}
        seekJSON['jid'] = arg['jid']
        seekJSON['rid'] = arg['rid']
        seekJSON['cid'] = arg['cid']
        seekJSON['id'] = int(arg['oid'])
        seekJSON['byte_start'] = arg['byte_start']
        seekJSON['byte_end'] = arg['byte_end']
        seekJSON['uDomain'] = arg['source']


        # GET data from existing J0INT config file
        if os.path.exists(seekCONF) == True:
            with open(seekCONF, "r") as chConf:
                lineIndex = 0
                for line in chConf:
                    skJSON = json.loads(line)
                    if jointID == str(skJSON['jid']) and requestID == str(skJSON['rid']) and str(orderID) == str(skJSON['id']):
                        skNAME = "Chnk_"+jointID+"_"+requestID+"_"+chunkID+"_"+str(orderID)+".J0INT";
                        # check if chunk is valid
                        if os.path.exists(seekPATH) == True:
                            # compare size and hash stored in config.json
                            # to the available file in seekPATH
                            print('[+]', skNAME, '~ File match found\n')

                            storedHash = skJSON['hash']['md5']
                            print('[!] Stored md5 hash:', storedHash)

                            calcHash = stdlib.md5(seekPATH)
                            print('[!] Calculated md5 hash:', calcHash)

                            if storedHash == calcHash:
                                print("[!] File exists, exiting...")
                                # Edit config.json, Append missing parameters
                                # REF: https://www.kite.com/python/answers/how-to-edit-a-specific-line-in-a-text-file-in-python#:~:text=Use%20file.,at%20a%20certain%20line%20number.
                                # revalidate file data based (due to hash authenticity)

                                skJSON['size'] = os.path.getsize(seekPATH)
                                skJSON['progress'] = 100.0
                                skJSON['status'] = "finished"
                                skJSON['action'] = 'realtime_share_progress'
                                wsPayload = json.dumps(skJSON)

                                # Get line to edit in config.json
                                configFile = open(seekCONF, 'r')
                                configLines = configFile.readlines()
                                configLines[lineIndex] = wsPayload+'\n'

                                # Set edited line in config.json
                                configFile = open(seekCONF, 'w')
                                configFile.writelines(configLines)
                                configFile.close()

                                # Notify socket server of download completion
                                if self.connected == True:
                                    await self.ws.send(wsPayload)
                                    print('[!] Sent (Shared) realtime data ~ Already exists')
                                else:
                                    print('[!] File sharing manager socket is not connected')
                                print('-'*101)
                                return
                    lineIndex += 1
        else:
            # Generate config file
            wEngine_config = open(seekCONF, "w")
            wEngine_config.close()
        # -------------------------------------------------------------------------/\


        # Validate uri ------------------------------------------------------------\/
        headers_arg = {"Range" : "bytes=0-100"}
        r = requests.get(uri, headers=headers_arg)
        if r.status_code >= 400:
            print("[-] Shared file status returned: ", r.status_code)
            return
        # -------------------------------------------------------------------------/\


        print('\n[+] ->', seekJSON['uDomain'], '<-', '-'*75)
        print(' URI\t', uri)
        # Smart downloader --------------------------------------------------------\/
        fileDLM = SmartDL(uri, dest)
        fileDLM.start(blocking=False)

        while not fileDLM.isFinished():
            # MAIN FUNCTIONS =>
            # 1. Inform socket server of download progress
            # 2. Check if a pause request has been sent to this thread by socket communication
            # 3. Check if an unpause request was sent to this thread by socket communication

            seekJSON['size'] = fileDLM.get_dl_size()
            seekJSON['status'] = fileDLM.get_status()
            seekJSON['eta'] = fileDLM.get_eta(human=True)
            seekJSON['progress'] = (fileDLM.get_progress() * 100)
            if self.ws != None:
                wsJSON = seekJSON
                wsJSON['action'] = 'realtime_share_progress'
                wsPayload = json.dumps(wsJSON)
                try:
                    await self.ws.send(wsPayload)
                    print('[!] Sent (Shared) realtime data ~ Downloading')
                except Exception as e:
                    print('\n\n[-] Error while sending RealTime (shared) data:', e)

            await asyncio.sleep(random.random() * 3)

        if fileDLM.isSuccessful():
            # MAIN FUNCTIONS =>
            # 1. Inform socket server of thread download progress
            seekJSON['size'] = fileDLM.get_dl_size()
            seekJSON['status'] = fileDLM.get_status()
            seekJSON['eta'] = fileDLM.get_eta(human=True)
            seekJSON['progress'] = (fileDLM.get_progress() * 100)
            seekJSON['time_elapsed'] = fileDLM.get_dl_time(human=True)
            seekJSON['hash'] = {
                'md5' : fileDLM.get_data_hash('md5'),
                'sha1' : fileDLM.get_data_hash('sha1'),
                'sha256' : fileDLM.get_data_hash('sha256'),
            }
            if self.ws != None:
                wsJSON = seekJSON
                wsJSON['action'] = 'realtime_share_progress'
                wsPayload = json.dumps(wsJSON)
                try:
                    await self.ws.send(wsPayload)
                    print('[!] Sent (Shared) realtime data ~ Finished')
                except Exception as e:
                    print('\n\n[-] Error while sending RealTime (shared) data:', e)


        else:
            print("[!] There were some errors:")
            # MAIN FUNCTIONS =>
            # 1. Inform socket server of thread download error

            for e in fileDLM.get_errors():
                print(str(e))

            if self.ws != None:
                seekJSON['error'] = fileDLM.get_errors()
                seekJSON['action'] = 'realtime_share_progress'
                wsPayload = json.dumps(seekJSON)
                try:
                    await self.ws.send(wsPayload)
                    print('[!] Sent (Shared) realtime data ~ Error')
                except Exception as e:
                    print('\n\n[-] Error while sending RealTime (shared) data:', e)

        # log = open('share_log.txt', 'a')
        # log.write(json.dumps(arg)+'\n')
        # log.close()
        # await asyncio.sleep(4)
        path = fileDLM.get_dest()
        print('[+] Done ~', path)

        # Write data of new file to config.json
        configFile = open(seekCONF, 'a')
        configFile.write(json.dumps(seekJSON)+'\n')
        configFile.close()

        print('[+]', '-'*97, '\n')
    # ------------------------------------------------------------------------->


    # File validator/merger --------------------------------------------------->
    def makeFile(self, jid, rid):
        print('[!] VALIDATING FILES: [JointID]>', jid, '[RequestID]>', rid)
        storage = "storage/"+str(jid)+"/"+str(rid)
        config = storage + "/config.json"
        destFile = storage+'/Arch_'+jid+'_'+rid+'.zip'


        configFile = None
        configData = []
        fileCount = 0
        if os.path.exists(config):
            print('[!] Config exists!')
            configFile = open(config, 'r')
            for line in configFile:
                configData.append(json.loads(line))
                fileCount += 1

        # Sort config data by id
        sConfigData = sorted(configData, key = lambda k: k['id'])
        open('log_'+jid+'_'+rid+'.txt', 'a').write(json.dumps(sConfigData)+"\n\n")

        mainFile = open(destFile, 'ab')
        mJdata = None
        if os.path.exists(storage+'/make.json'):
            print('[!] File already exists, skipping ...')
            makeJsonChk = open(storage+'/make.json', 'r')
            mJdata = json.loads(makeJsonChk.read())
            makeJsonChk.close()

        # Validate file before merging
        for chunk in sConfigData:
            fOrderID = chunk['id']
            fJointID = chunk['jid']
            fRequestID = chunk['rid']
            fChunkID = chunk['cid']
            fname = 'Chnk_'+fJointID+'_'+str(fRequestID)+'_'+str(fChunkID)+'_'+str(fOrderID)+'.J0INT'
            fMD5 = chunk['hash']['md5']

            if mJdata != None:
                print('[!] CHECKING LAST FILE ORDER FOR MERGING')
                if fOrderID <= mJdata['lastOrder']:
                    # skip loop to next loop
                    continue
                print('[!] FILE MERGING CONTINUED')


            fPath = "storage/"+fJointID+"/"+fRequestID+"/"+fname
            if os.path.exists(fPath) == False:
                print('[-] FILE NOT FOUND EXITING MERGER:', fPath)
                return

            elif os.path.exists(fPath) == True:
                print('[+] FILE FOUND, PROCEEDING')
                # Compare MD5 hash
                calcHash = stdlib.md5(fPath)

                if fMD5 == calcHash:
                    print('[+] FILE IS VALID')

                    # read file in bytes
                    chunkFile = open(fPath, 'r')
                    chunkBytes = chunkFile.read()

                    # add bytes to main file
                    mainFile.write(chunkBytes)
                    chunkFile.close()

            print('[!] Chunk from eng_sharing.py:', chunk)
            makeJson = open(storage+'/make.json', 'w')
            makeJson.write(json.dumps({
                'filename': 'Arch_'+jid+'_'+rid+'.zip',
                'size': os.path.getsize(destFile),
                'hash': {'md5': stdlib.md5(destFile)},
                'jid': jid,
                'rid': rid,
                'lastOrder': fOrderID,
                'lastChunk': fChunkID
            }))
            makeJson.close()

        mainFile.close()
        print('[+] FILE MERGING COMPLETED')

    # ------------------------------------------------------------------------->
