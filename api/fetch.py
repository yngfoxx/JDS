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
    return "True"

app.run()
