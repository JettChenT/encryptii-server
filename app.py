"""
    The web version of encrypto (auto-redirect)
"""
from flask import redirect,Flask
app = Flask(__name__)

@app.route('/')
def home():
    return redirect("https://encryptii.now.sh")

@app.route('/encrypt')
def encrypt():
    return redirect("https://encryptii.now.sh/encrypt")       

@app.route('/decrypt')
def decrypt():
    return redirect("https://encryptii.now.sh/encrypt")

if __name__ == '__main__':
    app.run()