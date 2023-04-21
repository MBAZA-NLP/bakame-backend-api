from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import stt_sdk, tts_sdk, chatbot_sdk, va_sdk
import io



api = FastAPI()  #instance
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#text path
@api.post('/')
async def index():
    return "Welcome to the Health Assistant API"

#text path
@api.post('/type')
async def text_interaction(request : Request, text : str):
    
    #get response from chabot
    chat_response = chatbot_sdk.chatbot_api(chat=text['message'])
    tts_chat = chatbot_sdk.process_tts_response(chat_response)
    

    # return chat response and voice response as JSON
    headers = {
        "Content-Disposition": f"attachment; filename=audio.wav",
        "text" : f'{chatbot_sdk.process_chat_response(chat_response)}'
    }


    return chat_response

#text path
@api.post('/va_cmu/type')
async def text_interaction_va(request : Request, text : str):
    
    #get response from chabot
    chat_response = va_sdk.chatbot_api(question=text['message'])
    

    # return chat response and voice response as JSON
    headers = {
        "Content-Disposition": f"attachment; filename=audio.wav",
        "text" : f'{chat_response}'
    }


    return chat_response


#voice path
@api.post("/speak")
async def voice_interaction_bakame(request : Request, audio_file: bytes = File(...), user_id : str = Form(...)):

    #process the voice
    text = stt_sdk.stt_api(audio_bytes=audio_file)
    print(text)
    
    #get response from chabot
    chat_response = chatbot_sdk.chatbot_api(chat=text['message'], user_id=user_id)
    tts_chat = chatbot_sdk.process_tts_response(chat_response)
    print(tts_chat)

    #tts response
    voice_response = tts_sdk.tts_api(text=tts_chat)
    voice_response_bytes = io.BytesIO()
    voice_response_bytes.write(voice_response)
    voice_response_bytes.seek(0)


    # return chat response and voice response as JSON
    headers = {
        "Content-Disposition": f"attachment; filename=audio.wav",
        "text" : f'{chatbot_sdk.process_chat_response(chat_response)}'
    }


    return StreamingResponse(voice_response_bytes, headers=headers, media_type="audio/mpeg")



#voice path
@api.post("/va_cmu/speak")
async def voice_assistant(request : Request, audio_file: bytes = File(...), user_id : str = Form(...)):

    #process the voice
    text = stt_sdk.stt_api(audio_bytes=audio_file)
    
    #get response from chabot
    chat_response = va_sdk.chatbot_api(question=text['message'])


    #tts response
    voice_response = tts_sdk.tts_api(text=chat_response)
    voice_response_bytes = io.BytesIO()
    voice_response_bytes.write(voice_response)
    voice_response_bytes.seek(0)


    # return chat response and voice response as JSON
    headers = {
        "Content-Disposition": f"attachment; filename=audio.wav",
        "text" : f'{chat_response}'
    }


    return StreamingResponse(voice_response_bytes, headers=headers, media_type="audio/mpeg")



