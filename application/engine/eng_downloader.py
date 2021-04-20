import sys
import time
import requests
import argparse
from pySmartDL import SmartDL

# http://itaybb.github.io/pySmartDL/examples.html
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests
# https://stackoverflow.com/questions/40691996/python-requests-http-range-not-working

# CLIENT DOWNLOAD MANAGER
# test URL: "https://www.bing.com/th?id=OIP.1L3zMoMScZvtQ9VLhf4MRgHaLH&w=200&h=300&c=8&o=5&pid=1.7"
# test URL: "https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe"

parser = argparse.ArgumentParser(prog='grab', description='download contents from internet using Python')
parser.add_argument('-u', '--url', type=str, required=True, help='The URL of the target file')
parser.add_argument('-d', '--dest', type=str, required=True, help='The download destination')
args = parser.parse_args()

headers_arg = {"Range" : "bytes=0-100"}
headers_dlm_arg = {"headers" : {"Range" : "bytes=0-100"}}


# test if the server accepts range header
r = requests.get(args.url, headers=headers_arg)
assert len(r.text) <= 101
print(r)

fileDLM = SmartDL(args.url, args.dest, request_args=headers_dlm_arg)
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
    # 1. Inform socket server of thread download progress
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

path = fileDLM.get_dest()
