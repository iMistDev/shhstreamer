import eel
import eel.browsers
import threading
import vtt_module
import tts_module
import speech_recognition as sr

eel.init('web')

app_config = {
    "mic": 0,
    "lang": "es-419",
    "voice": 0
}

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
        voices = tts_module.select_voice()
        print(f" -> Voices found!: {len(voices)}")
    
        return{
        "mics":mics,
        "voices":voices
        }
    
    except Exception as e:
        print(f"Critical Error on method get_lists(): {e}")
        return {"mics": [], "voices": []}
    
def audio_loop():
    global active_stream
    print("--- [THREAD] Starting audio Engine... ---")
    
    r = sr.Recognizer()
    r.pause_threshold = 1.5
    r.dynamic_energy_threshold = False
    
    try:
        mic_id = app_config["mic"]
        device = mic_id if mic_id is not None else None
        
        with sr.Microphone(device_index=device) as source:
            
            eel.js_log("--- [SYSTEM] Calibrating Noise... (please be quiet.) ---")
            print("--- [THREAD] Calibrating... ---")
            r.adjust_for_ambient_noise(source, duration=1)
            eel.js_log("--- [SYSTEM] System ready, listening... ---")
            
            while active_stream:
                try:
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
                            tts_module.speak(text, app_config["voice"])
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
                
# Deprecated / Refactorized
""" 
def audio_loop():
    global active_stream
    print("--- [THREAD] Entering Audio Loop. ---")
    try:
        print(f" [CHECK] Mic ID: {app_config['mic']}")
        print(f" [CHECK] Lang: {app_config['lang']}")
        print(f" [CHECK] Voice ID: {app_config['voice']}")
    except Exception as e:
        print(f"--- [THREAD ERROR] Error while reading config: {e} ---")
        eel.js_log(f"Error config: {e}")
        return
    
    while active_stream:
        try:
            print("--- [THREAD] Calling vtt function... ---")
            eel.js_log("Listening...")
            
            text = vtt_module.hear_function(app_config["mic"], app_config["lang"])
            
            if not active_stream:
                print("--- [THREAD Stop signal detected after listening. Aborting... ---]")
                eel.js_log("Forcibly Detained.")
                break
            
            print(f"--- [THREAD] vtt state: {text} ---")
            
            if text:
                eel.js_log(f"Your Microphone: {text}")
                eel.js_log(f"Voice selected: {text}")
                
                print("--- [THREAD] Calling TTS... ---")
                if active_stream:
                    tts_module.speak(text, app_config["voice"])
                
                
        except Exception as e:
            msg_error = f"--- THREAD CRASH: {e} ---"
            print(f" ERROR: {msg_error}")
            eel.js_log(msg_error)
            import traceback
            traceback.print_exc()
            active_stream = False
            break
    eel.js_log(">>>SHUTDOWN SYSTEM")
    print("--- [THREAD] Loop finished successfully. ---") 
"""             
chromium_browser = r"D:\Chromium\chrome-win\chrome.exe"

eel.browsers.set_path('chrome', chromium_browser)

eel.start('index.html', size=(680, 980), mode='chrome')
