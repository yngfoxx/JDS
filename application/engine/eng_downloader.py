import os
import sys
import time
import requests
import argparse
from pySmartDL import SmartDL

# http://itaybb.github.io/pySmartDL/examples.html
# http://itaybb.github.io/pySmartDL/code.html?highlight=pause#pySmartDL.SmartDL.pause
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests
# https://stackoverflow.com/questions/40691996/python-requests-http-range-not-working

# CLIENT DOWNLOAD MANAGER
# test URL: "https://www.bing.com/th?id=OIP.1L3zMoMScZvtQ9VLhf4MRgHaLH&w=200&h=300&c=8&o=5&pid=1.7"
# test URL: "https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe"

parser = argparse.ArgumentParser(prog='grab', description='download contents from internet using Python')
parser.add_argument('-jid', '--joint_id', type=str, required=True, help='Joint ID of target file')
parser.add_argument('-rid', '--request_id', type=str, required=True, help='Request ID of target file')
parser.add_argument('-chnk', '--chunk_order', type=str, required=True, help='Chunk order number')
parser.add_argument('-bs', '--byte_start', type=str, required=False, help='Byte start of the file stream')
parser.add_argument('-be', '--byte_end', type=str, required=False, help='Byte end of the file stream')
args = parser.parse_args()


def download(arg):
    # Arguments --------------------------------------------------------------->
    engine_config = None
    jointID = arg['jid'].replace("\'", "")
    requestID = arg['rid'].replace("\'", "")
    chunkORDER = arg['order'].replace("\'", "")

    print('[+] Starting download', '-'*80, '\n Joint_ID:\t', jointID, '\n Request_ID:\t', requestID, '\n Chunk_ORDER:\t', chunkORDER, '\n')


    # Paths
    url = 'http://127.0.0.1/JDS/storage/'+jointID+'/'+requestID+'/Arch_'+jointID+'_'+requestID+'.zip'
    storage = "../storage/"+jointID

    # Create default storage folder if missing
    if os.path.exists("../storage") == False:
        os.mkdir("../storage/")


    # Create J0INT download directory
    if os.path.exists(storage) == False:
        os.mkdir(storage)
        storage = storage + "/" + requestID
        if os.path.exists(storage) == False:
            os.mkdir(storage)


    # Directories have been created
    storage = "../storage/" + jointID + "/" + requestID

    # Chunk file destination
    chunkPATH = storage + "/" + "Chnk_"+jointID+"_"+requestID+"_"+chunkORDER+".J0INT"
    chunkCONF = storage + "/chunkconf.json"

    # GET data from J0INT engine_config file
    if os.path.exists(chunkCONF) == True:
        rEngine_config = open(chunkCONF, "r")
        engine_config = rEngine_config.read()
        rEngine_config.close()
        # Validate chunks with engine_config.json


    # Create J0INT engine_config file to be used as a temporary database
    wEngine_config = open(chunkCONF, "w")


    # check if chunk exists and is valid
    if os.path.exists(chunkPATH) == True:
        # compare size to byte_end and hash stored in engine_config
        print("[!] Chunk exists, exiting...")
        print('-'*101)
        return



    # Create chunk
    chunk = open(chunkPATH, 'wb')

    headers_dlm_arg = {}
    if 'byte_start' in arg and 'byte_end' in arg:
        byte_start = arg['byte_start']
        byte_end = arg['byte_end']
        headers_dlm_arg = {
            "headers" : {
                "Range" : "bytes="+str(byte_start)+"-"+str(byte_end),
            }
        }
    else:
        headers_dlm_arg = {"headers":{}}
    # ------------------------------------------------------------------------->


    # Validate url ------------------------------------------------------------>
    headers_arg = {"Range" : "bytes=0-100"}
    r = requests.get(url, headers=headers_arg)
    if r.status_code >= 400:
        print("[-] File status returned: ", r.status_code)
        return
    # ------------------------------------------------------------------------->


    # Smart downloader -------------------------------------------------------->
    fileDLM = SmartDL(url, storage, request_args=headers_dlm_arg)
    fileDLM.start(blocking=False)

    data = {}

    while not fileDLM.isFinished():
        data['speed'] = fileDLM.get_speed(human=True)
        data['size'] = fileDLM.get_dl_size(human=True)
        data['eta'] = fileDLM.get_eta(human=True)
        data['progress'] = (fileDLM.get_progress() * 100)
        data['bar'] = fileDLM.get_progress_bar()
        data['status'] = fileDLM.get_status()

        # print(data)
        # [TODO] MAIN FUNCTIONS =>
        # 1. Inform socket server of download progress
        # 2. Check if a pause request has been sent to this thread by socket communication
        # 3. Check if an unpause request was sent to this thread by socket communication

        time.sleep(0.2)

    if fileDLM.isSuccessful():
        data['path'] = fileDLM.get_dest()
        data['time_elapsed'] = fileDLM.get_dl_time(human=True)
        data['md5'] = fileDLM.get_data_hash('md5')
        data['sha1'] = fileDLM.get_data_hash('sha1')
        data['sha256'] = fileDLM.get_data_hash('sha256')
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
    chunk.write(fileBIN)
    chunk.close()

    # Delete downloaded file
    path = fileDLM.get_dest()
    print('\n[PATH]', path)
    if os.path.exists(path):
        os.remove(path)
        print('[+] Cleaned up temporary file: ', path);
    else:
        print('[-] Could not find file: ',path);

    config.close()

    print('-'*101)

    # ------------------------------------------------------------------------->

if __name__ == '__main__':
    # COMMAND: python eng_downloader.py -jid 'joint_id' -rid 'request_id' -bs 'byte_start' -be 'byte_end'
    # COMMAND: python eng_downloader.py -jid 'LYKW7R' -rid '523' -bs 0 -be 4196
    parms = {}
    parms['jid'] = args.joint_id
    parms['rid'] = args.request_id
    parms['order'] = args.chunk_order
    parms['byte_start'] = args.byte_start
    parms['byte_end'] = args.byte_end
    download(parms)
