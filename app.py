from flask import Flask, request
from encryptMessage import Encryptor
from flask_cors import CORS
from flask_restx import Resource, Api

api = Api()
app = Flask(__name__)
CORS(app)
api.init_app(app)
enc = Encryptor()


@api.route('/ping')
class PingPong(Resource):
    def get(self):
        # easter egg/ test whether or not api is up
        return {'ping': 'pong'}, 200


@api.route("/encrypt")
@api.doc(params={'msg': 'message to encrypt'})
class EncryptionPage(Resource):
    def get(self):
        msg = request.args.get("msg")
        print(msg)
        encrypted = enc.encrypt(msg)
        resp = {
            "encrypted": encrypted.decode()
        }
        return resp, 200


@api.route("/decrypt")
@api.doc(params={'dec': 'encrypted message to decrypt', 'destroy': "destroys the message if this parameter is True"})
class DecryptionPage(Resource):
    @api.doc(responses={404: 'Message does not exist or was destroyed',
                        200: 'Success'
                        })
    def get(self):
        td = request.args.get("dec").encode()
        des = request.args.get("destroy")
        flag = (des == "True")
        d = enc.decrypt(td, flag)
        print(td)
        if d == -1:
            return dict(msg="Message does not exist or was destroyed"), 404
        else:
            return dict(msg=str(d)), 200


if __name__ == "__main__":
    app.run(debug=True)
