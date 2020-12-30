import threading
from threading import Thread

import flask
from flask import request, jsonify, make_response

from flaskgrab import download

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['GET'])
def main():
    # Data needed URL, REQUEST_ID, SOCKET NAMESPACE, DOWNLOAD DESTINATION
    # [TEST URL] ------------------------------------------------------------------------------------------------------>
    # http://127.0.0.1:5000/?url="https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe"&rid="13RWS2"&nsp='1234531'&dest='C:/JDS/storage/'
    # ----------------------------------------------------------------------------------------------------------------->
    url = str(request.args['url'])
    rid = str(request.args['rid'])
    nsp = str(request.args['nsp'])
    dest = str(request.args['dest'])


    # BREAKTHROUGH
    # thread = Thread(target=flaskgrab.download, args={'URL': url, 'REQUEST_ID': rid, 'NAMESPACE': nsp, 'DESTINATION': dest}) # Failed attempt
    # flaskgrab.download(URL=url, REQUEST_ID=rid, NAMESPACE=nsp, DESTINATION=dest)
    thread = Thread(target=download, args=[url, rid, nsp, dest])
    thread.setDaemon(True)
    thread.start()

    for thread in threading.enumerate():
        print(thread.name)

    return make_response(jsonify({'thread_name': str(thread.name), 'started': True}), 200)

    # if 'url' in request.args:
    #     url = str(request.args['url'])
    #     if 'rid' in request.args:
    #         rid = str(request.args['rid'])
    #         if 'nsp' in request.args:
    #             nsp = str(request.args['nsp'])
    #             if 'dest' in request.args:
    #                 dest = str(request.args['dest'])
    #
    #                 # return json.dumps(request.args)
    #             else:
    #                 return "Error: no destination specified"
    #         else:
    #             return "Error: no namespace specified"
    #     else:
    #         return "Error: no request ID specified"
    # else:
    #     return "Error: no url specified"


app.run()
