import asyncio
import edge_tts
import io
import pygame
import utils

try:
    pygame.mixer.init()
    print("--- [TTS] Audio Engine Pre-Loaded ---")
except pygame.error:
    print("--- [TTS] Can't pre-load the audio engine. ---")

def list_voices():
    voice_options = []
    for i, data in utils.TTS_VOICES.items():
        voice_options.append({
            "id": i,
            "name": data["name"]
        })
    return voice_options

async def speak(text: str, voice_id: int, volume: int = 100):
    if voice_id not in utils.TTS_VOICES:
        print(f"Error: Voice ID {voice_id} not found. Using 0. (default)")
        voice_id = 0
        
    if not text or not text.strip():
        return
     
    VOICE = utils.TTS_VOICES[voice_id]["code"]
    
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        
        audio_buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
                
        audio_buffer.seek(0)
        
        vol_float = volume / 100.0
        pygame.mixer.music.set_volume(vol_float)
        
        pygame.mixer.music.load(audio_buffer)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.05)
        
    except Exception as e:
        print(f"EdgeTTS Error: {e}")