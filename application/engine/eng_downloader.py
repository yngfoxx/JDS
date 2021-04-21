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

# http://itaybb.github.io/pySmartDL/examples.html
# http://itaybb.github.io/pySmartDL/code.html?highlight=pause#pySmartDL.SmartDL.pause
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests
# https://stackoverflow.com/questions/40691996/python-requests-http-range-not-working
# https://www.devdungeon.com/content/working-binary-data-python#writefile
# https://docs.python.org/3/library/queue.html

# CLIENT DOWNLOAD MANAGER
# test URL: "https://www.bing.com/th?id=OIP.1L3zMoMScZvtQ9VLhf4MRgHaLH&w=200&h=300&c=8&o=5&pid=1.7"
# test URL: "https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe"


# Download queue -----
downloadQue = Queue()
dParm = {}
# downloads = set()
# download_index = 0
# --------------------


# https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def makeRandomKey(length):
    letters = string.ascii_uppercase + string.digits
    return ( ''.join(random.choice(letters) for i in range(length)) )


# Downloader ------------------------------------------------------------------>
def downloader(arg):
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
    storage = "storage/"+jointID

    # Create default storage folder if missing
    if os.path.exists("storage") == False:
        os.mkdir("storage")


    # Create J0INT download directory
    if os.path.exists(storage) == False:
        os.mkdir(storage)
        storage = storage + "/" + requestID
        if os.path.exists(storage) == False:
            os.mkdir(storage)


    # Directories have been created
    storage = "storage/" + jointID + "/" + requestID


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

    # GET data from J0INT engine_config file
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

                        calcHash = md5(chunkPATH)
                        print('[!] Calculated md5 hash:', calcHash)

                        if storedHash == calcHash:
                            print("[!] Chunk exists, exiting...")
                            # Notify socket server of download completion
                            print('-'*101)
                            return
    else:
        # Generate congig file
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

    # downloads.add({ "id": download_index, "manifest": chunkJSON, "dl": fileDLM })
    # download_index += 1

    data = {}

    while not fileDLM.isFinished():
        # data['speed'] = fileDLM.get_speed(human=True)
        # data['size'] = fileDLM.get_dl_size(human=True)
        # data['eta'] = fileDLM.get_eta(human=True)
        # data['progress'] = (fileDLM.get_progress() * 100)
        # data['bar'] = fileDLM.get_progress_bar()
        # data['status'] = fileDLM.get_status()

        chunkJSON['size'] = fileDLM.get_dl_size()
        chunkJSON['status'] = fileDLM.get_status()

        # print(data)
        # [TODO] MAIN FUNCTIONS =>
        # 1. Inform socket server of download progress
        # 2. Check if a pause request has been sent to this thread by socket communication
        # 3. Check if an unpause request was sent to this thread by socket communication

        time.sleep(0.2)

    if fileDLM.isSuccessful():
        # data['path'] = fileDLM.get_dest()
        # data['time_elapsed'] = fileDLM.get_dl_time(human=True)
        # data['md5'] = fileDLM.get_data_hash('md5')
        # data['sha1'] = fileDLM.get_data_hash('sha1')
        # data['sha256'] = fileDLM.get_data_hash('sha256')

        chunkJSON['hash'] = {
            'time_elapsed' : fileDLM.get_dl_time(human=True),
            'md5' : fileDLM.get_data_hash('md5'),
            'sha1' : fileDLM.get_data_hash('sha1'),
            'sha256' : fileDLM.get_data_hash('sha256'),
        }

        # [TODO] MAIN FUNCTIONS =>
        # 1. Inform socket server of thread download progress

    else:
        print("[!] There were some errors:")
        for e in fileDLM.get_errors():
            print(str(e))
        # [TODO] MAIN FUNCTIONS =>
        # 1. Inform socket server of thread download error


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
    # -------------------------------------------------------------------------/\
# ----------------------------------------------------------------------------->


# Thread object --------------------------------------------------------------->
def worker():
    while True:
        dParm = downloadQue.get()
        downloader(dParm)
        downloadQue.task_done()
# ----------------------------------------------------------------------------->


# Queue manager --------------------------------------------------------------->
def downloadManager(dArg):
    dParm['jid'] = dArg['jid']
    dParm['rid'] = dArg['rid']
    dParm['order'] = dArg['order']
    dParm['byte_start'] = dArg['byte_start']
    dParm['byte_end'] = dArg['byte_end']

    threading.Thread(target=worker, daemon=True).start()

    downloadQue.put(dParm)
    print("[!] Download added to que")

    # block until all tasks are done
    downloadQue.join()
    print('[!] download completed')
# ----------------------------------------------------------------------------->


# Download manager client web socket class handler
class downloadManagerSS():
    def __init__(self):
        super().__init__()
        self.uri = "ws://localhost:5678"
        self.connected = True
        self.socket_id = makeRandomKey(12)
        self.socket_payload = json.dumps({ "action": "download_manager_connected", "socketType": "download_mngr",  "socketID": self.socket_id })


    async def connectSocketServer(self):
        async with websockets.connect(self.uri) as websocket:
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
                                downloadManager(wsRequest['payload'])
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
                    pass

                await asyncio.sleep(random.random() * 3)

    def connect(self):
        self.loop = asyncio.get_event_loop()
        print('[!] Connecting download manager...')
        asyncio.run(self.connectSocketServer())
        # self.loop.ensure_future(self.connectSocketServer())
        print('[!] Download manager exited gracefully')

    def initWS(self):
        threading.Thread(target=self.connect(), daemon=True)


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
