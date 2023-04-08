import os
import requests
import json


tts_api_host = os.getenv('TTS_HOST')


def tts_api(text : str):

    #compile the headers
    headers = {"Content-Type": "application/json"}

    #compile the form data
    payload = json.dumps({
        "text": f"{text}"
        })
    
    #get response
    response = requests.post(url=os.getenv('TTS_HOST'), headers=headers,data=payload)

    return response
