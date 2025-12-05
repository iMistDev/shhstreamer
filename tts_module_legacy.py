import pyttsx3


def select_voice():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    voice_options = []
    
    for i, v in enumerate(voices):
        voice_options.append({
            "id": i,
            "name": v.name
        })
        
    return voice_options

def speak(text, voice_index=0):
    if not text: return
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
        
    engine.setProperty('rate', 150)
    
    print(f"\n[BOT]: {text}")
    engine.say(text)
    engine.runAndWait()