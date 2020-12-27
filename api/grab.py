# SCRIPT BY OSUNRINDE STEPHEN ADEBAYO (SID 20010266)
import time, requests, argparse, random, math
from pySmartDL import SmartDL
import socketio


# PARSE INLINE COMMAND ARGUMENTS ---------------------------------------------->
# accepts argument from command e.g "python grab.py -u https://www.filedomain.com/file.zip"
parser = argparse.ArgumentParser(prog='grab', description='download contents from internet using Python')


# accept URL with "-u" or "--url"
parser.add_argument('-u', '--url', type=str, required=True, help='The URL of the target file')
parser.add_argument('-r', '--rid', type=str, required=True, help='The request id attached to the svr_download_request table')
parser.add_argument('-nsp', '--namespace', type=str, required=True, help='Node.js Websocket namespace')
parser.add_argument('-d', '--destination', type=str, required=True, help='Download destination also known as server_path')


# assign arguments to object
args = parser.parse_args()

# Assign arguments in object to variables
URL = args.url
REQUEST_ID = args.rid
NAMESPACE = args.namespace
DESTINATION = args.destination
# ----------------------------------------------------------------------------->



# CONNECT TO WEBSOCKET -------------------------------------------------------->
sio = socketio.Client() # WebSocket object

channel_id = "/py_" + NAMESPACE;
# channel_id = "/py_" + str(math.floor((random.random() * (9999999 - 1000000 + 1)) + 1000000)); # generate ID

sio.connect('https://ws-jds-eu.herokuapp.com/', namespaces=channel_id); # connect python api to generated socket channel id
# sio.connect('https://ws-jds-eu.herokuapp.com', headers={'auth':'qPyFMKAdjtfL3Gq5pk2xDgy0SKMpEmLz'}, namespaces=channel_id); # connect python api to generated socket channel id
# sio.connect('http://localhost:8000/', namespaces=channel_id); # connect python api to generated socket channel id


# SOCKET EVENTS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@sio.event
def connect():
    sio.emit("msg", {"foo":"bar"}, channel_id)
    print("[connected] socket_id: ", sio.sid)

@sio.event
def connect_error():
    print("[failed] socket connection")

@sio.event
def disconnect():
    print("[disconnected]")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ----------------------------------------------------------------------------->


# SMART DOWNLOADER OPERATION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
obj = SmartDL(URL, DESTINATION)


# INITIALIZE THE DOWNLOAD ----------------------------------------------------->
obj.start(blocking=False)

while not obj.isFinished():
        sio.emit('msg', {
            'speed': obj.get_speed(human=True),
            'downloaded': obj.get_dl_size(human=True),
            'ETA': obj.get_eta(human=True),
            'progress': (obj.get_progress()*100),
            'bar': obj.get_progress_bar(),
            'status': obj.get_status()
        }, channel_id);
        print("|")
        print("|-----> socket message sent")
        print("|")
        # print("Speed: %s" % obj.get_speed(human=True))
        # print("Already downloaded: %s" % obj.get_dl_size(human=True))
        # print("Eta: %s" % obj.get_eta(human=True))
        # print("Progress: %d%%" % (obj.get_progress()*100))
        # print("Progress bar: %s" % obj.get_progress_bar())
        # print("Status: %s" % obj.get_status())
        # print("\n"*2+"="*50+"\n"*2)
        time.sleep(0.2)

if obj.isSuccessful():
        sio.emit('msg', {
            'download_path': obj.get_dest(),
            'download_time_length': obj.get_dl_time(human=True),
            'MD5': obj.get_data_hash('md5'),
            'SHA1': obj.get_data_hash('sha1'),
            'SHA256': obj.get_data_hash('sha256')
        }, channel_id);
        print("|")
        print("|-----> download took %s" % obj.get_dl_time(human=True))
        print("|")
        # print("downloaded file to '%s'" % obj.get_dest())
        # print("download task took %ss" % obj.get_dl_time(human=True))
        # print("File hashes:")
        # print(" * MD5: %s" % obj.get_data_hash('md5'))
        # print(" * SHA1: %s" % obj.get_data_hash('sha1'))
        # print(" * SHA256: %s" % obj.get_data_hash('sha256'))
else:
        print("There were some errors:")
        for e in obj.get_errors():
                print(str(e))
# ----------------------------------------------------------------------------->
# [*] 0.23 Mb / 0.37 Mb @ 88.00Kb/s [##########——–] [60%, 2s left]


# STORE DOWNLOADED FILE IN GIVEN DESTINATION
path = obj.get_dest()
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# disconnect from socket server
sio.disconnect()
