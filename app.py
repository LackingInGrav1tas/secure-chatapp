from flask import Flask, render_template, request
from messages import Message, random_string
import crypto

app = Flask(__name__)
log = {
    '0000': list() # general 
}

@app.route('/', methods=["GET", "POST"])
def index():
    message = ''
    convo_hash = '0000'
    key_file = ''
    if request.method == "POST":
        if not request.form["convo_hash"] in log:
            log[request.form["convo_hash"]] = list()

        f = request.files['key_file']
        f.seek(0)
        key = f.read()

        if len(request.form["text_msg"]) > 0:
            log[request.form["convo_hash"]].insert(0, 
                Message(
                    str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr)),
                    crypto.encrypt(key, (request.form["text_msg"] + '.').encode('utf-8')) if len(key) != 0 else request.form["text_msg"],
                    len(key)!=0
                )
            )
        convo_hash = request.form['convo_hash']
        message = Message.fmt(key, log[request.form["convo_hash"]])
    return render_template("index.html").format(convo_hash, key_file, message)

@app.route('/info/')
def info():
    return render_template("info.html")

if __name__ == '__main__':
    app.run(debug=True)