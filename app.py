from flask import Flask, request, jsonify
from encryptMessage import Encryptor
from flask_cors import CORS
from flask_restplus import Resource, Api

api = Api()
app = Flask(__name__)
CORS(app)
api.init_app(app)
enc = Encryptor()


@api.route('/ping')
class PingPong(Resource):
    def get(self):
        # easter egg/ test whether or not api is up
        return {'ping': 'pong'},200


@api.route("/encrypt")
class EncryptionPage(Resource):
    def get(self):
        msg = request.args.get("msg")
        print(msg)
        encrypted = enc.encrypt(msg)
        resp = {
            "encrypted": encrypted.decode()
        }
        return resp


@api.route("/decrypt")
class DecryptionPage(Resource):
    def get(self):
        td = request.args.get("dec").encode()
        des = request.args.get("destroy")
        flag = (des == "True")
        d = enc.decrypt(td, flag)
        print(td)
        if d == -1:
            resp = dict(code=300, err_msg="Your message does not exist")
        else:
            resp = dict(code=200, msg=str(d))
        return resp


if __name__ == "__main__":
    app.run(debug=True)
