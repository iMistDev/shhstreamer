#VTT (Voice to Text) Module Develop
import speech_recognition as sr
import time
import pyaudio
import utils

def select_language():
    #utils.cleaning()
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
    #utils.cleaning()
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