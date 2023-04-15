import os
import requests
import json
import hashlib


tts_api_host = os.getenv('TTS_HOST')

text_responses = set()


def hash_text(text: str):
    return hashlib.sha256(text.encode()).hexdigest()
    

def tts_search_sdk(text: str, hash : str):
    cache_dir = "cache/tts/"
    audio_cache = os.listdir(cache_dir)
    if hash + ".wav" in audio_cache:
        with open(cache_dir + hash + ".wav", "rb+") as audio_file:
            audio_bytes = audio_file.read()
        return audio_bytes
    else:
        return False
    
def tts_save_sdk(text: str, audio_bytes : bytes):
    cache_dir = "cache/tts/"
    text_hash = hash_text(text=text)
    with open(cache_dir + text_hash + ".wav", "wb+") as audio_file:
            audio_file.write(audio_bytes)
    return True


def tts_api(text : str):

    cache =  tts_search_sdk(text=text, hash=hash_text(text=text))
    if cache:
        return cache

    #compile the headers
    headers = {"Content-Type": "application/json"}

    #compile the form data
    payload = json.dumps({
        "text": f"{text}"
        })
    
    #get response
    response = requests.post(url=os.getenv('TTS_HOST'), headers=headers,data=payload)

    if response.status_code == 200:
        tts_save_sdk(text, response.content)
    

    return response.content



