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
parser.add_argument('-u', '--url', type=str, required=True, help='The URL of the target file')
parser.add_argument('-d', '--dest', type=str, required=True, help='The download destination')
parser.add_argument('-bs', '--byte_start', type=str, required=False, help='Byte start of the file stream')
parser.add_argument('-be', '--byte_end', type=str, required=False, help='Byte end of the file stream')
args = parser.parse_args()


def download(arg):
    # Arguments --------------------------------------------------------------->
    url = arg['url']
    dest = arg['dest']
    headers_dlm_arg = {}

    downloads = open('d_config.txt', 'w')
    # downloads.write(payload)
    # downloads.close()

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
        return ("File status returned: ", r.status_code)
    # ------------------------------------------------------------------------->


    # Smart downloader -------------------------------------------------------->
    fileDLM = SmartDL(url, dest, request_args=headers_dlm_arg)
    downloads.add(fileDLM)
    fileDLM.start(blocking=False)

    data = {}

    while not fileDLM.isFinished():
        data['speed'] = fileDLM.get_speed(human=True)
        data['size'] = fileDLM.get_dl_size(human=True)
        data['eta'] = fileDLM.get_eta(human=True)
        data['progress'] = (fileDLM.get_progress() * 100)
        data['bar'] = fileDLM.get_progress_bar()
        data['status'] = fileDLM.get_status()

        print(data)
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
        print("There were some errors:")
        for e in fileDLM.get_errors():
            print(str(e))
        # [TODO] MAIN FUNCTIONS =>
        # 1. Inform socket server of thread download error


    # data = fileDLM.get_data()
    # print('\n[DATA]\n', data)

    path = fileDLM.get_dest()
    print('\n[PATH]\n', path)

    # json = fileDLM.get_json()
    # print('\n[JSON]\n', json)

    hash = fileDLM.get_data_hash(False)
    print('\n[HASH]\n', hash)
    # ------------------------------------------------------------------------->

if __name__ == '__main__':
    parms = {}
    parms['url'] = args.url
    parms['dest'] = args.dest
    parms['byte_start'] = args.byte_start
    parms['byte_end'] = args.byte_end
    download(parms)
