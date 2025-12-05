import asyncio
import edge_tts
import io
import pygame

VOICE_MAPPING = {
    0: "es-CL-LorenzoNeural",
    1: "es-ES-ElviraNeural",
    2: "es-MX-DaliaNeural",
    3: "en-US-JennyNeural"
}

def list_voices():
    voice_options = []
    for i, name in VOICE_MAPPING.items():
        voice_options.append({
            "id": i,
            "name": name
        })
    return voice_options

async def speak(text: str, voice_id: int, volume: int = 100):
    if voice_id not in VOICE_MAPPING:
        print(f"Error: Voice ID {voice_id} not found. Using 0. (default)")
        voice_id = 0
        
    VOICE = VOICE_MAPPING[voice_id]
    
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        
        audio_buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
                
        audio_buffer.seek(0)
        
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        
        vol_float = volume / 100.0
        pygame.mixer.music.set_volume(vol_float)
        
        pygame.mixer.music.load(audio_buffer)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
        
    except Exception as e:
        print(f"EdgeTTS Error: {e}")