from fastapi import FastAPI, Request, File
from fastapi.responses import FileResponse
import os  # For system commands
from pydantic import BaseModel

class Text(BaseModel):
    text: str

class AudioBytes(BaseModel):
    audio: bytes

app = FastAPI()

#Index path
@app.post("/")
async def index():
    return {"message": "This is the index page"}

#Text to speech path
@app.post("/stt")
async def stt(request: Request, audio: bytes = File()):
    file_id : int = len(os.listdir("STT/sounds")) + 1
    with open(f"STT/sounds/sound-{file_id}.wav", "wb") as f:
        f.write(audio)
    
    return "Success"

#Text to speech path
@app.post("/tts")
async def tts(request: Request, text : Text) -> str:
    text = text.dict()['text']
    file_id : int = len(os.listdir("TTS/sounds")) + 1
    #Infer the text
    os.system(f'tts --text "{text}" --model_path TTS/model.pth --encoder_path TTS/SE_checkpoint.pth.tar --encoder_config_path TTS/config_se.json --config_path TTS/config.json --speakers_file_path TTS/speakers.pth --speaker_wav TTS/conditioning_audio.wav --out_path TTS/sounds/sound-{file_id}.wav')
    
    return FileResponse(f"TTS/sounds/sound-{file_id}.wav", media_type="audio/wav")