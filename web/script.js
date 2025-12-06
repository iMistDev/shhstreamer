window.onload = async function() {
    console.log("Loading System...");

    let datos = await eel.get_lists()();

    if (datos) {

        fillSelect("micSelect", datos.mics);
        fillSelect("voiceSelect", datos.voices);

        let langSelect = document.getElementById("langSelect");
        langSelect.innerHTML = "";

        datos.languages.forEach(langItem => {
            let option = document.createElement("option");

            option.text = langItem.name;
            option.value = langItem.code;

            langSelect.appendChild(option);
        });

        if (datos.config) {

            document.getElementById("micSelect").value = datos.config.mic;
            document.getElementById("voiceSelect").value = datos.config.voice;
            document.getElementById("langSelect").value = datos.config.lang;
            
            let volReal = datos.config.volume;

            let threshReal = datos.config.sensitivity || 20;

            let sSlider = document.getElementById("sensInput");
            let sLabel = document.getElementById("sensLabel");

            let slider = document.getElementById('volInput');
            let label = document.getElementById('volLabel');

            if (sSlider) sSlider.value = threshReal;
            if (sLabel) sLabel.innerText = threshReal + "%";

            if (slider) slider.value = volReal;
            if (label) label.innerText = volReal + "%";
        }

        js_log("--- System Loaded (Devices & Config) ---")
    }
};

function fillSelect(elementId, listaItems) {
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
    eel.update_config(key, value);
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

function updateVolume(val) {
    document.getElementById('volLabel').innerText = val + "%";
    eel.update_config('volume', val); 
}

function updateSens(val) {
    document.getElementById('sensLabel').innerText = val + "%";
    eel.update_config('sensitivity', val); 
}

eel.expose(js_log);
function js_log(text) {
    let box = document.getElementById('console');
    let p = document.createElement('p');
    p.innerText = text;
    
    if(text.includes("You:")) p.style.color = "#00ffff";
    if(text.includes("Bot:")) p.style.color = "#00ff88";
    if(text.includes("Error")) p.style.color = "red";
    
    box.appendChild(p);
    box.scrollTop = box.scrollHeight;
}
