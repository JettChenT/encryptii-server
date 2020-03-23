"""
    The web version of encrypto
"""
from flask import Flask,render_template,request
from encryptMessage import Encryptor
app = Flask(__name__)
enc = Encryptor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encrypt',methods=["POST"])
def encrypt():
    msg = request.form['message']
    encrypted_message = enc.encrypt(msg)
    return encrypted_message

@app.route('/decrypt',methods=["POST"])
def decrypt():
    msg = request.form['message'].encode()
    decrypted_message = enc.decrypt(msg)
    return decrypted_message

if __name__ == '__main__':
    app.run(debug = True)