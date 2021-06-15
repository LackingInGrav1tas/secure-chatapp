function update() {
    setInterval(async function() {
        let id = document.getElementById('convo_hash').value
        let r = await fetch('e2ee-chat-app.herokuapp.com/get_info/' + id);
        if (r.ok) {
            let data = await r.text();
            document.getElementById('txt-log').innerHTML = data;
        }
    }, 30000)
}