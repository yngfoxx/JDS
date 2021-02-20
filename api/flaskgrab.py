# SCRIPT BY OSUNRINDE STEPHEN ADEBAYO (SID 20010266)
import sys
import time
import requests
import socketio
from pySmartDL import SmartDL


class jdsDownloader():
    def __init__(self, channel, joint_id):
        super().__init__()
        self.channel = channel
        self.namespace = "/py_"+channel
        self.jid = joint_id


    def connecsocket(self):
        self.socket = socketio.Client(  )

        # self.socket.connect('https://localhost:8000'+self.namespace, headers={'room':self.namespace})
        self.socket.connect('https://ws-jds-eu.herokuapp.com', headers={'room':self.namespace}, namespaces=[self.namespace])


        @self.socket.on('connect', namespace=self.namespace)
        def connect():
            print("[socket connected successfully]")

        @self.socket.on('connect_error', namespace=self.namespace)
        def connect_error():
            print("[socket connection failed]")

        @self.socket.on('disconnect', namespace=self.namespace)
        def disconnect():
            print("[socket is now disconnected]")


    def download(self, URL, REQUEST_ID, DESTINATION):
        print("[*] =================================================================================>")
        self.connecsocket() # Connect web socket

        obj = SmartDL(URL, DESTINATION)
        obj.start(blocking=False)
        nsp = self.namespace

        while not obj.isFinished():
            print("[*]")
            try:
                self.socket.emit('event', {
                    'namespace': self.namespace,
                    'request_id': REQUEST_ID,
                    'joint_id': self.jid,
                    'file_data': {
                        'speed': obj.get_speed(human=True),
                        'downloaded': obj.get_dl_size(human=True),
                        'ETA': obj.get_eta(human=True),
                        'progress': (obj.get_progress() * 100),
                        'bar': obj.get_progress_bar(),
                        'status': obj.get_status()
                    }
                }, self.namespace)

                # Update PHP of file status
                payload = {
                    'jdsUpd': 'QtWuiJ7JrlcWbIV8GzYS8243Jb7pZKPs',
                    'joint_id': self.jid,
                    'request_id': REQUEST_ID,
                    'progress': (obj.get_progress() * 100),
                    'status': obj.get_status()
                }
                req = requests.post('http://localhost/JDS/req/req_handler.php', data=payload)
                if req:
                    print("[+] JDS UPDATED BY SOCKET AND POST REQUEST")
            except:
                print("Failed to connect to socket")
                # Update PHP of file status
                payload = {
                    'jdsUpd': 'QtWuiJ7JrlcWbIV8GzYS8243Jb7pZKPs',
                    'joint_id': self.jid,
                    'request_id': REQUEST_ID,
                    'progress': 0,
                    'status': "internal_error",
                    'error_msg': "Failed to send socket data."
                }
                req = requests.post('http://localhost/JDS/req/req_handler.php', data=payload)
                if req:
                    print("[+] WEB REQUEST SENT")
                else:
                    print("[-] WEB REQUEST FAILED")
                obj.stop()
            print("[*]")

            time.sleep(0.2)

        if obj.isSuccessful():
            print("[*]")
            self.socket.emit('event', {
                'namespace': self.namespace,
                'request_id': REQUEST_ID,
                'joint_id': self.jid,
                'file_data': {
                    'download_path': obj.get_dest(),
                    'download_time_length': obj.get_dl_time(human=True),
                    'MD5': obj.get_data_hash('md5'),
                    'SHA1': obj.get_data_hash('sha1'),
                    'SHA256': obj.get_data_hash('sha256')
                }
            }, self.namespace)
            # Update PHP of file status
            payload = {
                'jdsUpd': 'QtWuiJ7JrlcWbIV8GzYS8243Jb7pZKPs',
                'joint_id': self.jid,
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
            if req:
                print("[+] download took %s" % obj.get_dl_time(human=True))
            else:
                print("[-] JDS WAS NOT UPDATED [100%]")
                print(req)

        else:
            print("An unexpected error occured")
            for e in obj.get_errors():
                print(str(e))

        path = obj.get_dest()
        self.socket.disconnect(); # disconnect WebSocket
        print("[*] =================================================================================>")


if __name__ == '__main__':
    # TERMINAL ALTERNATIVE ->
    # python flaskgrab.py "https://i.pinimg.com/originals/bf/82/f6/bf82f6956a32819af48c2572243e8286.jpg" 13RWS2 12 1234531 "C:\JDS\storage"
    URL = sys.argv[1]
    JOINT_ID = sys.argv[2]
    REQUEST_ID = sys.argv[3]
    NAMESPACE = sys.argv[4]
    DESTINATION = sys.argv[5]

    downloader = jdsDownloader(JOINT_ID)
    downloader.download(URL, REQUEST_ID, DESTINATION)
# SCRIPT BY OSUNRINDE STEPHEN ADEBAYO (SID 20010266)
