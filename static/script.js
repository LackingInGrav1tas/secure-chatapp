async function getKey() {
    let contents = '';
    if (document.getElementById('key_file').files.length > 0) {
        let reader = new FileReader();
        contents = await new Promise((resolve) => {
            reader.onload = (e) => {
                resolve(e.target.result);
            };
            reader.readAsText(document.getElementById('key_file').files[0]);
        });
    }
    return contents;
}

var notif = 0;

async function update() {
    window.addEventListener("mousedown", ()=> {
        notif = 0;
        document.title = "ChatApp";
        document.getElementById('icon').href = 'static/favicon.ico';
    });

    setInterval(async function() {
        let id = document.getElementById('convo_hash').value
        let prev_msgs = document.getElementById('txt-log').innerHTML.split('<p>').length - 1;
        let r = await fetch('/get_info/', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(
                {
                    key: await getKey(),
                    convo_id: document.getElementById('convo_hash').value,
                }
            )
        });
        if (r.ok && document.getElementById('checkbox').checked == true) {
            let data = await r.json();
            document.getElementById('txt-log').innerHTML = data.log;
            let current_msgs = (data.log.split('<p>').length-1);
            notif += current_msgs - prev_msgs;
            if (current_msgs !== prev_msgs) {
                let sound = new Audio("static/notification.mp3");
                sound.play();
            }
        }
        if (notif > 0) {
            document.title = '(' + notif.toString() + ') ChatApp';
            document.getElementById('icon').href = 'static/notif_icon.ico';
        }
    }, 1000);
}

async function handleForm(event) {
    event.preventDefault();    
    key = await getKey();
    console.log('key: ' + key)
    let resp = await fetch('/send_msg', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(
            {
                key: key,
                convo_id: document.getElementById('convo_hash').value,
                msg: document.getElementById('text_msg').value
            }
        )
    });
    console.log(resp)
}

function init_form() {
    document.getElementById('msg-form').addEventListener('submit', handleForm);
}