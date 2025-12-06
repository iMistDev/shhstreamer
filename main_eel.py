import eel
import threading
import vtt_module
import tts_module
import speech_recognition as sr
import asyncio
import utils
import json
import os

eel.init('web')

CONFIG_FILE = "user_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r')as f:
                return json.load(f)
        except Exception as e:
            print(f"Error while loading config: {e}")
    return None

def save_config():
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(app_config, f, indent=4)
        print("--- [SYS] Saved Config. ---")
    except Exception as e:
        print(f"--- Error saving config: {e} ---")

default_config = {
    "mic": 0,
    "lang": "es-419",
    "voice": 0,
    "volume": 50,
    "sensitivity": 20
}

saved_config = load_config()

if saved_config:
    app_config = saved_config
    print(f"--- [SYS] Config. Loaded: {app_config} ---")
else:
    app_config = default_config
    print("--- [SYS] Defatult configuration selected. ---")

active_stream = False

@eel.expose
def stop_stream():
    global active_stream
    print("--- [PY] STOP signal Recived. ---")
    active_stream = False

@eel.expose
def update_config(key, value):
    print(f"[UI] Changin {key} to {value}")
    if str(value).isdigit():
        app_config[key] = int(value)
    else:
        app_config[key] = value
    save_config()

@eel.expose
def start_stream():
    global active_stream
    
    if active_stream:
        return
    print("--- [PY] Start button pressed, Attempting Thread... ---")
    eel.js_log(">>> STARTING UP...")
    
    active_stream = True
    t = threading.Thread(target=audio_loop, daemon=True)
    t.start()
    print("--- [PY] Thread started succesfully. ---")
    
@eel.expose
def get_lists():
    print("Sending devices lists...")
    try:
        
        print(" -> Searching Microphones...")
        mics = vtt_module.select_mic()
        print(f" -> Microphones found!: {len(mics)}")
        print(" -> Searching Voices...")
        voices = tts_module.list_voices()
        print(f" -> Voices found!: {len(voices)}")
        
        input_langs = utils.INPUT_LANGUAGES
    
        return{
        "mics":mics,
        "voices":voices,
        "languages": input_langs,
        "config": app_config
        }
    
    except Exception as e:
        print(f"Critical Error on method get_lists(): {e}")
        return {"mics": [], "voices": []}

def calculate_tresh(percent):
    MIN_AUDIO = 300
    MAX_AUDIO = 4000
    
    return MIN_AUDIO + (percent * (MAX_AUDIO - MIN_AUDIO) / 100)
    
def audio_loop():
    global active_stream
    print("--- [THREAD] Starting audio Engine... ---")
    
    r = sr.Recognizer()
    r.pause_threshold = 0.6
    r.non_speaking_duration = 0.4
    r.dynamic_energy_threshold = False
    
    try:
        mic_id = app_config["mic"]
        device = mic_id if mic_id is not None else None
        
        with sr.Microphone(device_index=device) as source:
            
            eel.js_log("--- [SYS] Sistem Ready. ---")
            eel.js_log("--- [SYS] Remember to check your Mic Sensitivity ---")
            eel.js_log("--- [SYS] Now start Speaking... ---")
            
            while active_stream:
                try:
                    
                    user_percent = app_config.get("sensitivity", 20)
                    real_threshold = calculate_tresh(user_percent)
                    
                    r.energy_threshold = real_threshold
                    
                    try:
                        audio = r.listen(source, timeout=1, phrase_time_limit=6)
                    except sr.WaitTimeoutError:
                        continue
                
                    if not active_stream:
                        print("--- [THREAD] Stop detected after listening. ---")
                        break
                 
                    eel.js_log("--- [SYSTEM] Processing... ---")
                
                    text = vtt_module.audio_processing(r, audio, app_config["lang"])
                
                    if text:
                        eel.js_log(f" >Your Microphone: {text}")
                        if active_stream:
                            eel.js_log(f" >Your voice: {text}")
                            asyncio.run(tts_module.speak(text, app_config["voice"], app_config["volume"]))
                            #Deprecated on ver. 2.0
                            #tts_module.speak(text, app_config["voice"])
                            eel.js_log("Listening...")
                except Exception as e:
                    print(f"Error while looping: {e}")
                    if active_stream:
                        eel.js_log(f"Error: {e}")
    except Exception as e:
        eel.js_log(f" --- [ERROR] Critical error while opening mic: {e}")
        print(f"--- [SYSTEM] CRITICAL ERROR: {e} ---")
        active_stream = False
        
    eel.js_log("--- [SYSTEM] SHUTDOWN SYSTEM ---")
    print("--- [THREAD] Thread finished. ---")
                
import sys
if sys.platform in ['win32', 'cygwin']:
    browser = 'edge'
else:
    browser = 'chrome'
    
print(f"--- [SYS] Initializing in mode: {browser} ---")

try:
    eel.start('index.html', size=(680, 980), mode=browser)
except EnvironmentError:
    print("--- [WARN/SYS] Browser not found, using users default. ---")
    eel.start('index.html', size=(680, 980), mode='default')
