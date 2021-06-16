function update() {
    setInterval(async function() {
        let id = document.getElementById('convo_hash').value
        let r = await fetch('/get_info/' + id);
        if (r.ok && document.getElementById('checkbox').checked == true) {
            let data = await r.json();
            document.getElementById('txt-log').innerHTML = data.log;
        }
    }, 1000);
}

async function handleForm(event) {
    event.preventDefault();

    let reader = new FileReader();
    let contents = '';
    reader.onload = (e) => {
        contents = e.target.result;
    };
    reader.readAsText(document.getElementById('key_file').files[0]);

    await fetch('/send_msg', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(
            {
                key: contents,
                convo_id: document.getElementById('convo_hash').value,
                msg: document.getElementById('text_msg').value
            }
        )
    });
}

function init_form() {
    document.getElementById('msg-form').addEventListener('submit', handleForm);
}