import os
import requests


tts_api_host = os.getenv('STT_HOST')


def stt_api(audio_bytes : bytes):

    #compile the form data
    form_data = {
        "user_id": "1234",
        "file": ("audio.wav", audio_bytes, "audio/mp3")
                }
    
    response = requests.post(url=tts_api_host, files=form_data).json()

    return response
