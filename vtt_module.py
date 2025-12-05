#VTT (Voice to Text) Module Develop
import speech_recognition as sr
import time
import pyaudio
import utils

def select_language():
    utils.cleaning()
    print("\n--- Languages Supported ---")
    print("\nMore available languages incoming")
    for key, info in utils.AVAILABLE_LANGUAGES.items():
        print(f"[{key}] {info['name']}")

    while True:
        option = input("Select your language (number): ").strip()
        
        if option in utils.AVAILABLE_LANGUAGES:
            selection = utils.AVAILABLE_LANGUAGES[option]
            print(f"-> Selected: {selection['name']}")
            time.sleep(1)
            return selection['code']
        else:
            print("Invalid Option. Try Again.")

def select_mic():
    utils.cleaning()
    p = pyaudio.PyAudio()
    info_devices = []
    
    seen_core_names = set()
    
    print("\n----- [ Scanning Audio Devices ] -----")
    
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        name = dev.get('name')
        input_channels = dev.get('maxInputChannels')
        
        ignore_words = ["Microphone", "Micrófono", "Input", "Entrada"]
        
        clean_name = name
        for word in ignore_words:
            clean_name = clean_name.replace(word, "").strip()
        
        if (input_channels > 0 and
            clean_name not in seen_core_names and
            "Asignador" not in name and
            "Controlador primario" not in name):
            
            seen_core_names.add(clean_name)
            info_devices.append({"id": i, "name": name})
            
    p.terminate()
    return info_devices
    
def audio_processing(recognizer, audio_data, lang_code):
    try:
        return recognizer.recognize_google(audio_data, language=lang_code)
    except sr.UnknownValueError:
        return None
    except Exception as e:
        print(f"Error on STT: {e}")
        return None
    
    # Legacy, CMD UI
    
    #print("\n--- [ Select Your Microphone ] ---")
    #for index_list, (real_id, name) in enumerate(info_devices):
    #    print(f"[{index_list}] {name}")
        
    #while True:
    #    try:
    #        option = int(input("\nSelect your microphone: "))
    #        if 0 <= option < len(info_devices):
    #            real_id = info_devices[option][0]
    #            real_name = info_devices[option][1]
    #            print(f"-> Selected: {real_name} (ID: {real_id})")
    #            time.sleep(1)
    #            return real_id
                
    #        print("Invalid Selection, Try again.")
    #    except ValueError:
    #        print("Please, enter a number.")

#OLD, deprecated.

"""
def hear_function(mic_id, lang_code):

    r = sr.Recognizer()
    r.pause_threshold = 2.5
    r.dynamic_energy_threshold = True
    
    print(f"\nInitializing microphone ID {mic_id}...")
    try:
        
        device = mic_id if mic_id is not None else None
        
        with sr.Microphone(device_index=mic_id) as source:
            print("Calibrating background noise (silence please)...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            
            print(f"Calibration Done. Speak Now... ({r.pause_threshold}s allowed pause time.)")
            
            audio = r.listen(source, timeout=10, phrase_time_limit=None)
            
            print("Processing audio...")
            text = r.recognize_google(audio, language=lang_code)
            print(f"\nYour Result: {text}")
            
            time.sleep(1.5)
            #Check if this continues or not
            #input("\nPress Enter to Return to Menu")
            return text
        
    except sr.WaitTimeoutError:
        print("Time out. No Speech Detected.")
        input("Press enter...")    
    except sr.UnknownValueError:
        print("Can't understand audio, try again.")
    except sr.RequestError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        
    return None
"""
