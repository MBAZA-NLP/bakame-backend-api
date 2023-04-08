import os
import requests
import json


def process_chat_response(chat : str):
    chat = json.loads(chat)
    chat = chat[0]['text']

    return chat

def process_tts_response(chat : str):
    chat = json.loads(chat)
    tts_chat = chat[0]['text'].split('http')[0]

    return tts_chat + '.'

def chatbot_api(chat : str, user_id : str):
    #compile the headers
    headers = {"Content-Type": "application/json"}

    #compile the form data
    payload = json.dumps({
        "sender": f"{user_id}",
        "message": f"{chat}"
        })
    
    #get response
    response = requests.post(url=os.getenv('CHATBOT_HOST'), headers=headers,data=payload)

    return response.text


