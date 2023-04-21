import os
import requests
import json


def process_chat_response(chat : str):
    #chat = json.loads(chat)
    #chat = chat[0]['text']

    return chat

def process_tts_response(chat : str):
    #chat = json.loads(chat)
    #tts_chat = chat[0]['text'].split('http')[0]

    return chat#tts_chat + '.'

def chatbot_api(question : str):
    #compile the headers
    headers = {"Content-Type": "application/json"}

    #compile the form data
    payload = json.dumps({
        "question": f"{question}"
        })
    
    #get response
    response = requests.post(url=os.getenv('VA_CHATBOT_HOST'), headers=headers,data=payload)

    return response.text


