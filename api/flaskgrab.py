# SCRIPT BY OSUNRINDE STEPHEN ADEBAYO (SID 20010266)
import os
import sys
import time

import requests
import socketio

from pySmartDL import SmartDL

# from zipfile_infolist import print_info
import zipfile


class jdsDownloader():
    def __init__(self, channel, joint_id):
        super().__init__()
        self.channel = channel
        self.namespace = str("/py_"+channel)
        self.jid = joint_id
        self.rid = 0


    def connecsocket(self):
        self.socket = socketio.Client()

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


    def download(self, URL, REQUEST_ID, DESTINATION, CHUNK):
        print("[*] =================================================================================>")
        self.connecsocket() # Connect web socket

        obj = SmartDL(URL, DESTINATION)
        obj.start(blocking=False)
        nsp = self.namespace
        self.rid = REQUEST_ID

        while not obj.isFinished():
            print("[*] \t")
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
            print("[*] \t")

            time.sleep(0.4)

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
                'optimal_chunk': ((obj.get_final_filesize(human=False) * 20) / 100),
                'download_time_length': obj.get_dl_time(human=True),
                'file_real_size': obj.get_final_filesize(human=True),
                'file_byte_size': obj.get_final_filesize(human=False)
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

        path = obj.get_dest();

        # COMPRESS FILE
        try:
            self.compress(path, DESTINATION, obj.get_final_filesize(human=False))
        finally:
            print('[+] Compression is done');
            self.socket.sleep(0.4)
            self.socket.disconnect(); # disconnect WebSocket

        print("[*] =================================================================================>")


    def compress(self, path, dest, fileSize):
        # ===================================================================== #
        # |            ZIP AND SPLIT CHUNK USING PYTHON LIBRARIES             | #
        # ===================================================================== #

        # https://askubuntu.com/questions/1106903/split-zip-into-smaller-zip-files
        # https://pymotw.com/2/zipfile/
        # https://www.geeksforgeeks.org/working-zip-files-python/
        # https://stackoverflow.com/questions/26063311/importerror-no-module-named-zipfile

        optimal_chunk = (fileSize * 20.0) / 100.0
        real_optimal_chunk = optimal_chunk / 1024.0;

        print("[!] Optimal chunk size: ", optimal_chunk)
        print("[!] Optimal chunk real size: ", real_optimal_chunk, "KB")

        print("[!] FILE_PATH: ",path)
        print("[!] FILE_ROOT_DIR: ", dest)

        # C:/xampp/htdocs/JDS/storage/13RWS2/12/arch_13RWS2_12.zip
        # dest+'arch_'+JOINT_ID+'_'+REQUEST_ID+'.zip'
        file_name = 'Arch_'+self.jid+'_'+self.rid+'.zip'
        file_zip_path = dest + file_name

        # fileZIP = zipfile.ZipFile('test.zip', mode='w')
        fileZIP = zipfile.ZipFile(file_zip_path, mode='w')

        # INITIALIZE COMPRESSION STAGE ----------------------------------------\/
        try:
            print('[+] Compressing file');
            fileZIP.write(path)

            self.socket.emit('event', {
                'namespace': self.namespace,
                'joint_id': self.jid,
                'request_id': self.rid,
                'file_data': {'status': 'compressing'}
            }, self.namespace)

            payload = {
                'jdsArch': 'QtWuiJ7JrlcWbIV8GzYS8243Jb7pZKPs',
                'joint_id': self.jid,
                'request_id': self.rid,
                'status': 'compressing'
            }
            req = requests.post('http://localhost/JDS/req/req_handler.php', data=payload)

        finally:
            print('[+] Compression completed');

            if os.path.exists(path):
                os.remove(path)
                print('[+] Cleaned up unused file: ', path);
            else:
                print('[-] Could not find file: ',path);

            fileZIP.close()

            self.socket.emit('event', {
                'namespace': self.namespace,
                'joint_id': self.jid,
                'request_id': self.rid,
                'archive': file_name,
                'file_data': {'status': 'splitting'}
            }, self.namespace)

            # INITIALIZE ARCHIVE SPLITTING STAGE ------------------------------\/
            payload = {
                'jdsArch': 'QtWuiJ7JrlcWbIV8GzYS8243Jb7pZKPs',
                'joint_id': self.jid,
                'request_id': self.rid,
                'archive': file_name,
                'status': 'splitting'
            }
            req = requests.post('http://localhost/JDS/req/req_handler.php', data=payload)
            print(req.text)
        # ===================================================================== #



if __name__ == '__main__':
    # TERMINAL ALTERNATIVE ->
    # python flaskgrab.py "https://i.pinimg.com/originals/bf/82/f6/bf82f6956a32819af48c2572243e8286.jpg" 13RWS2 12 1234531 "C:/JDS/storage/13RWS2/12/" 20
    # python flaskgrab.py "https://i.pinimg.com/originals/bf/82/f6/bf82f6956a32819af48c2572243e8286.jpg" 13RWS2 12 1234531 "C:/xampp/htdocs/JDS/storage/13RWS2/12/" 20
    URL = sys.argv[1]
    JOINT_ID = sys.argv[2]
    REQUEST_ID = sys.argv[3]
    NAMESPACE = sys.argv[4]
    DESTINATION = sys.argv[5]
    CHUNK = sys.argv[6]

    downloader = jdsDownloader(NAMESPACE, JOINT_ID)
    downloader.download(URL, REQUEST_ID, DESTINATION, CHUNK)
# SCRIPT BY OSUNRINDE STEPHEN ADEBAYO (SID 20010266)
