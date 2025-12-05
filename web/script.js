window.onload = async function() {
    let datos = await eel.get_lists()(); 
    
    llenarSelect("micSelect", datos.mics);
    llenarSelect("voiceSelect", datos.voices);
    
    js_log("--- Loaded Devices ---");
};

function llenarSelect(elementId, listaItems) {
    let select = document.getElementById(elementId);
    select.innerHTML = ""; 
    
    listaItems.forEach(item => {
        let option = document.createElement("option");
        option.value = item.id;
        option.text = item.name; 
        select.appendChild(option);
    });
}

function setConfig(key, value) {
    eel.actualizar_config(key, value);
}

function start() {
    document.getElementById('btnStart').disabled = true;
    document.getElementById('btnStart').innerText = "WORKING...";

    document.getElementById('btnStop').disabled = false;
    document.getElementById('btnStop').innerText = "STOP STREAM";
    eel.start_stream();
}

function stop() {
    document.getElementById('btnStop').disabled = true;
    document.getElementById('btnStop').innerText = "STOP STREAM";

    eel.stop_stream();

    document.getElementById('btnStart').disabled = false;
    document.getElementById('btnStart').innerText = "STRAT STREAMING";

    js_log("Stopping... (Waiting for actual phase...)");
}

eel.expose(js_log);
function js_log(text) {
    let box = document.getElementById('console');
    let p = document.createElement('p');
    p.innerText = text;
    
    if(text.includes("Tú:")) p.style.color = "#00ffff";
    if(text.includes("Bot:")) p.style.color = "#00ff88";
    if(text.includes("Error")) p.style.color = "red";
    
    box.appendChild(p);
    box.scrollTop = box.scrollHeight;
}