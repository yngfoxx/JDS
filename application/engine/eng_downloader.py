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

stdlib = stdlib()
_executor = ThreadPoolExecutor(1)

# http://itaybb.github.io/pySmartDL/examples.html
# http://itaybb.github.io/pySmartDL/code.html?highlight=pause#pySmartDL.SmartDL.pause
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests
# https://stackoverflow.com/questions/40691996/python-requests-http-range-not-working
# https://www.devdungeon.com/content/working-binary-data-python#writefile
# https://docs.python.org/3/library/queue.html

# CLIENT DOWNLOAD MANAGER
# test URL: "https://www.bing.com/th?id=OIP.1L3zMoMScZvtQ9VLhf4MRgHaLH&w=200&h=300&c=8&o=5&pid=1.7"
# test URL: "https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe"


# Download manager client web socket class handler
class downloadManagerSS():
    def __init__(self):
        super().__init__()
        self.uri = "ws://localhost:5678"
        self.connected = True
        self.socket_id = stdlib.makeRandomKey(12)
        self.downloadQueue = Queue()
        self.socket_payload = json.dumps({ "action": "download_manager_connected", "socketType": "download_mngr",  "socketID": self.socket_id })
        self.ws = None


    async def connectSocketServer(self):
        async with websockets.connect(self.uri) as websocket:
            self.ws = websocket
            # download manager is now connected
            await websocket.send(self.socket_payload)
            while self.connected == True:
                try:
                    wsInput = await websocket.recv()

                    if wsInput != None:
                        wsRequest = json.loads(wsInput)
                        if 'dMNGR' in wsRequest:
                            if wsRequest['dMNGR'] == "validate_download_data":
                                print('\n[!] Download manager activity', '='*80+'>')
                                self.downloadManager(wsRequest['payload'])
                                print('='*110+'>')

                            elif wsRequest['dMNGR'] == "exit":
                                # exit loop to terminate script
                                self.connected = False
                                break

                        elif self.socket_id in wsRequest:
                            print('[!] Download manager received:', wsRequest)

                except Exception as e:
                    print('[-] Error in download manager socket connection')
                    print(e)
                    self.connected = False
                    pass

                await asyncio.sleep(random.random() * 3)


    #
    def connect(self):
        self.loop = asyncio.get_event_loop()
        print('[!] Connecting download manager...')
        self.loop.run_until_complete(self.connectSocketServer())
        self.loop.close()
        print('[!] Download manager exited')
    # ------------------------------------------------------------------------->

    # Downloader -------------------------------------------------------------->
    async def downloader(self, arg):
        if self.ws != None:
            print('[!] WebSocket is accessible:', self.ws)

        # Arguments ---------------------------------------------------------------\/
        engine_config = None
        jointID = arg['jid'].replace("\'", "")
        requestID = arg['rid'].replace("\'", "")
        chunkORDER = arg['order'].replace("\'", "")
        headers_dlm_arg = {}
        if 'byte_start' in arg and 'byte_end' in arg:
            byte_start = float(arg['byte_start'])
            byte_end = float(arg['byte_end'])
            headers_dlm_arg = {
                "headers" : {
                    "Range" : "bytes="+str(byte_start)+"-"+str(byte_end),
                }
            }
        else:
            headers_dlm_arg = {"headers":{}}

        print('[+] Starting download', '-'*80, '\n Joint_ID:\t', jointID, '\n Request_ID:\t', requestID, '\n Chunk_ORDER:\t', chunkORDER, '\n')


        # Paths
        url = 'http://127.0.0.1/JDS/storage/'+jointID+'/'+requestID+'/Arch_'+jointID+'_'+requestID+'.zip'

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


        # Chunk file destination
        chunkPATH = storage + "/" + "Chnk_"+jointID+"_"+requestID+"_"+chunkORDER+".J0INT"
        chunkCONF = storage + "/config.json"


        # Chunk config data
        chunkJSON = {}
        chunkJSON['id'] = int(chunkORDER);
        chunkJSON['jid'] = jointID;
        chunkJSON['rid'] = requestID;
        chunkJSON['filename'] = "Chnk_"+jointID+"_"+requestID+"_"+chunkORDER+".J0INT";
        chunkJSON['byte_start'] = float(byte_start);
        chunkJSON['byte_end'] = float(byte_end);
        chunkJSON['status'] = None;


        # GET data from existing J0INT config file
        if os.path.exists(chunkCONF) == True:
            with open(chunkCONF, "r") as chConf:
                for line in chConf:
                    chnkJSON = json.loads(line)
                    if jointID == str(chnkJSON['jid']) and requestID == str(chnkJSON['rid']) and chunkORDER == str(chnkJSON['id']):
                        chnkNAME = "Chnk_"+jointID+"_"+requestID+"_"+chunkORDER+".J0INT";
                        # check if chunk is valid
                        if os.path.exists(chunkPATH) == True:
                            # compare size and hash stored in config.json
                            # to the available file in chunkPATH
                            print('[+]', chnkNAME, '~ File match found\n')

                            storedHash = chnkJSON['hash']['md5']
                            print('[!] Stored md5 hash:', storedHash)

                            calcHash = stdlib.md5(chunkPATH)
                            print('[!] Calculated md5 hash:', calcHash)

                            if storedHash == calcHash:
                                print("[!] Chunk exists, exiting...")
                                # Append missing parameters
                                # Notify socket server of download completion
                                if self.connected == True:
                                    wsJSON = chnkJSON
                                    wsJSON['action'] = 'realtime_download_progress'
                                    wsPayload = json.dumps(wsJSON)
                                    await self.ws.send(wsPayload)
                                    print('[!] Sent realtime data ~ Already exists')
                                else:
                                    print('[!] Download manager socket is not connected')
                                print('-'*101)
                                return
        else:
            # Generate config file
            wEngine_config = open(chunkCONF, "w")
            wEngine_config.close()
        # -------------------------------------------------------------------------/\


        # Validate url ------------------------------------------------------------\/
        headers_arg = {"Range" : "bytes=0-100"}
        r = requests.get(url, headers=headers_arg)
        if r.status_code >= 400:
            print("[-] File status returned: ", r.status_code)
            return
        # -------------------------------------------------------------------------/\


        # Smart downloader --------------------------------------------------------\/
        fileDLM = SmartDL(url, storage, request_args=headers_dlm_arg)
        fileDLM.start(blocking=False)

        data = {}

        while not fileDLM.isFinished():
            # MAIN FUNCTIONS =>
            # 1. Inform socket server of download progress
            # 2. Check if a pause request has been sent to this thread by socket communication
            # 3. Check if an unpause request was sent to this thread by socket communication

            chunkJSON['size'] = fileDLM.get_dl_size()
            chunkJSON['status'] = fileDLM.get_status()
            chunkJSON['eta'] = fileDLM.get_eta(human=True)
            chunkJSON['progress'] = (fileDLM.get_progress() * 100)
            if self.ws != None:
                wsJSON = chunkJSON
                wsJSON['action'] = 'realtime_download_progress'
                wsPayload = json.dumps(wsJSON)
                try:
                    await self.ws.send(wsPayload)
                    print('[!] Sent realtime data ~ Downloading')
                except Exception as e:
                    print('[-] Error while sending RealTime data:', e)

            await asyncio.sleep(random.random() * 3)

        if fileDLM.isSuccessful():
            # MAIN FUNCTIONS =>
            # 1. Inform socket server of thread download progress

            chunkJSON['time_elapsed'] = fileDLM.get_dl_time(human=True)
            chunkJSON['hash'] = {
                'md5' : fileDLM.get_data_hash('md5'),
                'sha1' : fileDLM.get_data_hash('sha1'),
                'sha256' : fileDLM.get_data_hash('sha256'),
            }
            if self.ws != None:
                wsJSON = chunkJSON
                wsJSON['action'] = 'realtime_download_progress'
                wsPayload = json.dumps(wsJSON)
                await self.ws.send(wsPayload)
                print('[!] Sent realtime data ~ Finished')


        else:
            print("[!] There were some errors:")
            # MAIN FUNCTIONS =>
            # 1. Inform socket server of thread download error

            for e in fileDLM.get_errors():
                print(str(e))

            if self.ws != None:
                chunkJSON['error'] = fileDLM.get_errors()
                wsPayload = json.dumps(chunkJSON)
                await self.ws.send(wsPayload)


        # Store binary data into file
        fileBIN = fileDLM.get_data(binary=True)
        # print('\n[BINARY]\n', fileBIN)

        with open(chunkCONF, 'a') as chunkDATA:
            chunkDATA.write(json.dumps(chunkJSON)+'\n')

        # Create chunk, store bytes in J0INT file
        chunk = open(chunkPATH, 'wb')
        chunk.write(fileBIN)
        chunk.close()

        # Delete downloaded file
        path = fileDLM.get_dest()
        print('\n[TEMP]', path)
        if os.path.exists(path):
            os.remove(path)
            print('[+] Cleaned up temporary file: ', path);
        else:
            print('[-] Could not find file: ',path);

        print('-'*101)
        return "done"
        # ---------------------------------------------------------------------/\
    # ------------------------------------------------------------------------->

    # Thread object ----------------------------------------------------------->
    def worker(self):
        while True:
            dQueueItem = self.downloadQueue.get()
            asyncio.get_event_loop().run_until_complete(self.downloader(dQueueItem))
            self.downloadQueue.task_done()
    # ------------------------------------------------------------------------->


    # Queue manager ----------------------------------------------------------->
    def downloadManager(self, dArg):
        dParm = {}

        for dParm in dArg:
            threading.Thread(target=self.worker, daemon=True).start()

            self.downloadQueue.put(dParm)
            print("[!] Download added to que")

            # block until all tasks are done
            self.downloadQueue.join()
            print('[!] download completed')
    # ------------------------------------------------------------------------->


if __name__ == '__main__':
    # COMMAND: python eng_downloader.py -jid 'joint_id' -rid 'request_id' -bs 'byte_start' -be 'byte_end' -chnk 'chunk_order_number'
    # COMMAND: python eng_downloader.py -jid 'LYKW7R' -rid '523' -bs 0 -be 36563480 -chnk 0
    parser = argparse.ArgumentParser(prog='grab', description='download contents from internet using Python')
    parser.add_argument('-jid', '--joint_id', type=str, required=True, help='Joint ID of target file')
    parser.add_argument('-rid', '--request_id', type=str, required=True, help='Request ID of target file')
    parser.add_argument('-chnk', '--chunk_order', type=str, required=True, help='Chunk order number')
    parser.add_argument('-bs', '--byte_start', type=str, required=False, help='Byte start of the file stream')
    parser.add_argument('-be', '--byte_end', type=str, required=False, help='Byte end of the file stream')
    args = parser.parse_args()

    parms = {}
    parms['jid'] = args.joint_id
    parms['rid'] = args.request_id
    parms['order'] = args.chunk_order
    parms['byte_start'] = args.byte_start
    parms['byte_end'] = args.byte_end

    response = downloader(parms)
    print(response)
