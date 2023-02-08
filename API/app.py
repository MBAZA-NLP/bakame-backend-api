from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import os  # For system commands
from pydantic import BaseModel

class Text(BaseModel):
    text: str

app = FastAPI()

#Index path
@app.post("/")
async def index():
    return {"message": "This is the index page"}

#Text to speech path
@app.post("/stt")
async def stt(request: Request):
    return {"message": "This is the stt page"}

#Text to speech path
@app.post("/tts")
async def tts(request: Request, text : Text) -> str:
    text = text.dict()['text']
    file_id : int = len(os.listdir("TTS/sounds")) + 1
    #Infer the text
    os.system(f'tts --text "{text}" --model_path TTS/model.pth --encoder_path TTS/SE_checkpoint.pth.tar --encoder_config_path TTS/config_se.json --config_path TTS/config.json --speakers_file_path TTS/speakers.pth --speaker_wav TTS/conditioning_audio.wav --out_path TTS/sounds/sound-{file_id}.wav')
    
    return FileResponse(f"TTS/sounds/sound-{file_id}.wav", media_type="audio/wav")
