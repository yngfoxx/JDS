# SCRIPT BY OSUNRINDE STEPHEN ADEBAYO
import time, requests, argparse, random, math
from pySmartDL import SmartDL
import socketio

# WebSocket object
sio = socketio.Client()

# Connect to websocket
# sio.connect('http://localhost:8000/', namespaces='/py-1213'); # connect python api to a socket channel

channel_id = "/py_" + str(math.floor((random.random() * (9999999 - 1000000 + 1)) + 1000000));

sio.connect('http://localhost:8000/', namespaces=channel_id); # connect python api to a socket channel
# sio.connect('http://localhost:8000/'); # connect python api to a socket channel

# sio.connect('https://ws-jds-eu.herokuapp.com', headers={'auth':'qPyFMKAdjtfL3Gq5pk2xDgy0SKMpEmLz'}, namespaces=channel_id); # connect python api to a socket channel

# Socket connection events
@sio.event
def connect():
    print("[connected] socket_id: ", sio.sid)
    sio.emit("msg", {"txt":"Hello world"}, channel_id);

@sio.event
def connect_error():
    print("[failed] socket connection")

@sio.event
def disconnect():
    print("[disconnected]")


# accepts argument from command e.g "python grab.py -u https://www.filedomain.com/file.zip"
parser = argparse.ArgumentParser(prog='grab', description='download contents from internet using Python')


# accept URL with "-u" or "--url"
parser.add_argument('-u', '--url', type=str, required=True, help='The URL of the target file')
parser.add_argument('-j', '--jid', type=str, required=True, help='The joint id for further processing')
parser.add_argument('-d', '--dest', type=str, help='Download destination')


# assign arguments to object
args = parser.parse_args()

# Assign arguments in object to variables
URL = args.url
JOINT_ID = args.jid

DESTINATION = './'

# DEFINE THE DOWNLOAD OBJECT
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

# disconnect from socket server
sio.disconnect()
