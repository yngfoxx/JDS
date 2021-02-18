# SCRIPT BY OSUNRINDE STEPHEN ADEBAYO (SID 20010266)
import sys
import time
import requests
# import argparse
import socketio
from pySmartDL import SmartDL


# PARSE INLINE COMMAND ARGUMENTS ---------------------------------------------->
# accepts argument from command e.g "python grab.py -u https://www.filedomain.com/file.zip"
# parser = argparse.ArgumentParser(prog='grab', description='download contents from internet using Python')
#
#
# # accept URL with "-u" or "--url"
# parser.add_argument('-u', '--url', type=str, required=True, help='The URL of the target file')
# parser.add_argument('-r', '--rid', type=str, required=True, help='The request id attached to the svr_download_request table')
# parser.add_argument('-nsp', '--namespace', type=str, required=True, help='Node.js Websocket namespace')
# parser.add_argument('-d', '--destination', type=str, required=True, help='Download destination also known as server_path')
#
#
# # assign arguments to object
# args = parser.parse_args()
#
# # Assign arguments in object to variables
# URL = args.url
# REQUEST_ID = args.rid
# NAMESPACE = args.namespace
# DESTINATION = args.destination
# ----------------------------------------------------------------------------->

def download(URL, JOINT_ID, REQUEST_ID, NAMESPACE, DESTINATION):
    # CONNECT TO WEBSOCKET -------------------------------------------------------->
    sio = socketio.Client()  # WebSocket object

    channel_id = "/py_" + NAMESPACE

    sio.connect('https://ws-jds-eu.herokuapp.com/', headers={'foo':'qPyFMKAdjtfL3Gq5pk2xDgy0SKMpEmLz'}, namespaces=channel_id)  # connect python api to generated
    # sio.connect('http://localhost:8000/', namespaces=channel_id)  # connect python api to generated socket channel id

    # SOCKET EVENTS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\/
    @sio.event
    def connect():
        sio.emit("msg", {"foo": "bar"}, channel_id)
        print("[connected] socket_id: ", sio.sid)

    @sio.event
    def connect_error():
        print("[failed] socket connection")

    @sio.event
    def disconnect():
        print("[disconnected]")

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>/\
    # ----------------------------------------------------------------------------->

    # SMART DOWNLOADER OPERATION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\/
    obj = SmartDL(URL, DESTINATION)

    # INITIALIZE THE DOWNLOAD ------------------------------------------------->
    obj.start(blocking=False)

    while not obj.isFinished():
        try:
            sio.emit('event', {
                'namespace': NAMESPACE,
                'request_id': REQUEST_ID,
                'joint_id': JOINT_ID,
                'file_data': {
                    'speed': obj.get_speed(human=True),
                    'downloaded': obj.get_dl_size(human=True),
                    'ETA': obj.get_eta(human=True),
                    'progress': (obj.get_progress() * 100),
                    'bar': obj.get_progress_bar(),
                    'status': obj.get_status()
                }
            }, channel_id)

            # Update PHP of file status
            payload = {
                'jdsUpd': 'QtWuiJ7JrlcWbIV8GzYS8243Jb7pZKPs',
                'joint_id': JOINT_ID,
                'request_id': REQUEST_ID,
                'progress': (obj.get_progress() * 100),
                'status': obj.get_status()
            }
            req = requests.post('http://localhost/JDS/req/req_handler.php', data=payload)
        except:
            print("Failed to connect to socket")
            # Update PHP of file status
            payload = {
                'jdsUpd': 'QtWuiJ7JrlcWbIV8GzYS8243Jb7pZKPs',
                'joint_id': JOINT_ID,
                'request_id': REQUEST_ID,
                'progress': 0,
                'status': "internal_error",
                'error_msg': "Failed to send socket data."
            }
            req = requests.post('http://localhost/JDS/req/req_handler.php', data=payload)
            obj.stop()

        print("||")
        print("||")
        if req:
            print("|-----> JDS UPDATED BY SOCKET AND POST REQUEST")
        else:
            print("|-----> JDS WAS NOT UPDATED")
        print(req)
        print(req.text)
        print("||")
        print("||")
        time.sleep(0.2)

    if obj.isSuccessful():
        sio.emit('event', {
            'namespace': NAMESPACE,
            'request_id': REQUEST_ID,
            'joint_id': JOINT_ID,
            'file_data': {
                'download_path': obj.get_dest(),
                'download_time_length': obj.get_dl_time(human=True),
                'MD5': obj.get_data_hash('md5'),
                'SHA1': obj.get_data_hash('sha1'),
                'SHA256': obj.get_data_hash('sha256')
            }
        }, channel_id)
        # Update PHP of file status
        payload = {
            'jdsUpd': 'QtWuiJ7JrlcWbIV8GzYS8243Jb7pZKPs',
            'joint_id': JOINT_ID,
            'request_id': REQUEST_ID,
            'progress': 100,
            'status': 'Completed',
            'md5_hash': obj.get_data_hash('md5'),
            'sha1_hash': obj.get_data_hash('sha1'),
            'sha256_hash': obj.get_data_hash('sha256'),
            'download_path': obj.get_dest(),
            'download_time_length': obj.get_dl_time(human=True)
        }
        req = requests.post('http://localhost/JDS/req/req_handler.php', data=payload)
        print("||")
        print("||")
        if req:
            print("|-----> download took %s" % obj.get_dl_time(human=True))
        else:
            print("|-----> JDS WAS NOT UPDATED [100%]")
        print(req)
        print(req.text)
        print("||")
        print("||")
    else:
        print("There were some errors:")
        for e in obj.get_errors():
            print(str(e))
    # ------------------------------------------------------------------------->
    # [*] 0.23 Mb / 0.37 Mb @ 88.00Kb/s [##########——–] [60%, 2s left]

    # STORE DOWNLOADED FILE IN GIVEN DESTINATION
    path = obj.get_dest()
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>/\

    # disconnect from socket server
    sio.disconnect()


if __name__ == '__main__':
    # Get arguments from user
    URL = sys.argv[1]
    JOINT_ID = sys.argv[2]
    REQUEST_ID = sys.argv[3]
    NAMESPACE = sys.argv[4]
    DESTINATION = sys.argv[5]
    download(URL, JOINT_ID, REQUEST_ID, NAMESPACE, DESTINATION)
# SCRIPT BY OSUNRINDE STEPHEN ADEBAYO (SID 20010266)
