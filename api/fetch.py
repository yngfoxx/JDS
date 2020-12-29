import flask
from flask import request, jsonify, make_response

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

fileData = {
    'uid'       : "1203AD",
    'src'       : "https://www.exodusleague.com/user/profile/156_d2eeb9e18f6c_profile.png",
    'timestamp' : "2020-11-02T04:43:03+00:00",
    'ip'        : "192.168.0.1"
}

@app.route('/', methods=['GET'])
def main():
    # Data needed URL and USER/SESSION ID
    # return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
    # http://127.0.0.1:5000/?url="https://download-cf.jetbrains.com/python/pycharm-community-2020.3.exe"&rid="13RWS2"&nsp='1234531'&dest='C:/JDS/storage'
    if 'url' in request.args:
        url = str(request.args['url'])
        if 'rid' in request.args:
            rid = str(request.args['rid'])
            if 'nsp' in request.args:
                nsp = str(request.args['nsp'])
                if 'dest' in request.args:
                    dest = str(request.args['dest'])
                    return "True"
                else:
                    return "Error: no destination specified"
            else:
                return "Error: no namespace specified"
        else:
            return "Error: no request ID specified"
    else:
        return "Error: no url specified"


app.run()
