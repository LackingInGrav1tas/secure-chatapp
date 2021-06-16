function update() {
    setInterval(async function() {
        let id = document.getElementById('convo_hash').value
        let r = await fetch('/get_info/', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(
                {
                    key: getKey(),
                    convo_id: document.getElementById('convo_hash').value,
                }
            )
        });
        if (r.ok && document.getElementById('checkbox').checked == true) {
            let data = await r.json();
            document.getElementById('txt-log').innerHTML = data.log;
        }
    }, 1000);
}

function getKey() {
    let contents = '';
    if (document.getElementById('key_file').files.length > 0) {
        let reader = new FileReader();
        reader.onload = (e) => {
            contents = e.target.result;
        };
        reader.readAsText(document.getElementById('key_file').files[0]);
    }
    console.log(document.getElementById('key_file').files.length);
    return contents;
}

async function handleForm(event) {
    event.preventDefault();    

    await fetch('/send_msg', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(
            {
                key: getKey(),
                convo_id: document.getElementById('convo_hash').value,
                msg: document.getElementById('text_msg').value
            }
        )
    });
}

function init_form() {
    document.getElementById('msg-form').addEventListener('submit', handleForm);
}