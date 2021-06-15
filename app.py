from flask import Flask, render_template, request, jsonify, make_response
from messages import Message, random_string
import crypto
import redis
import os
import pickle

app = Flask(__name__)
server_id = random_string(10)
REDIS_URL = os.environ['REDIS_URL']
REDIS_CHAN = 'chat'
r = redis.from_url(REDIS_URL)
log = {
    '0000': list() # general 
}
r.set('log', pickle.dumps(log))

update_code = """
function update() {
    setInterval(async function() {
        let id = document.getElementById('convo_hash').value
        let r = await fetch('/get_info/' + id);
        if (r.ok && document.getElementById('checkbox').checked == true) {
            let data = await r.json();
            document.getElementById('txt-log').innerHTML = data.log;
        }
    }, 30000);
}"""

@app.route('/', methods=["GET", "POST"])
def index():
    log = pickle.loads(r.get('log'))
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
        r.set('log', pickle.dumps(log))
    if request.method == 'GET':
        message = Message.fmt('', log['0000'])
    return render_template("index.html").format(update_code, '', convo_hash, key_file, message, server_id)

@app.route('/info/')
def info():
    return render_template("info.html")

@app.route('/get_info/<id>/')
def get_info(id):
    log = pickle.loads(r.get('log'))
    response = make_response(
        jsonify(
            {'log': Message.fmt('', log[id])}
        ),
    )
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(debug=True)