# SCRIPT BY OSUNRINDE STEPHEN ADEBAYO (SID 20010266)
import threading
from threading import Thread

import flask
from flask import request, jsonify, make_response

from flaskgrab import jdsDownloader

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['GET'])
def main():
    # Data needed URL, REQUEST_ID, SOCKET NAMESPACE, DOWNLOAD DESTINATION
    # [TEST URL] ------------------------------------------------------------------------------------------------------>
    # 127.0.0.1:5000/?url=https://i.pinimg.com/originals/bf/82/f6/bf82f6956a32819af48c2572243e8286.jpg&rid=12&jid=13RWS2&nsp=1234531&dest=C:\JDS\storage
    # ----------------------------------------------------------------------------------------------------------------->

    if 'url' in request.args and 'jid' in request.args and 'rid' in request.args and 'nsp' in request.args and 'dest' in request.args:
        url = str(request.args['url'])
        jid = str(request.args['jid'])
        rid = str(request.args['rid'])
        nsp = str(request.args['nsp'])
        dest = str(request.args['dest'])


        # Add the download request to a thread
        thread = Thread(target=jdsDownloader(nsp, jid).download, args=[url, rid, dest])
        thread.setDaemon(True)
        thread.start()

        for thread in threading.enumerate():
            print("Thread name => ",thread.name)

            # return make_response(jsonify({'thread_name': str(thread.name), 'started': True}), 200)
            return jsonify({'thread_name': str(thread.name), 'started': True})
    else:
        return jsonify({'response': 'Invalid parameter'})

app.run()
# SCRIPT BY OSUNRINDE STEPHEN ADEBAYO (SID 20010266)
