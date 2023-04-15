from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import stt_sdk, tts_sdk, chatbot_sdk
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
@api.post('/type')
async def text_interaction():
    pass


#voice path
@api.post("/speak")
async def voice_interaction(request : Request, audio_file: bytes = File(...), user_id : str = Form(...)):

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


@api.post("/audio")
async def process_audio(audio: UploadFile = File(...), text: str = Form(...)):
    """
    Process audio file and text string
    """
    # Do some processing with the audio and text here
    # ...

    # Create a BytesIO object to store the response content
    output = io.BytesIO()
    
    # Write the audio file contents to the BytesIO object
    output.write(audio.file.read())
    output.seek(0)

    # Set the response headers
    headers = {
        "Content-Disposition": f"attachment; filename={audio.filename}",
        "text" :  text
    }

    # Return a StreamingResponse object with the audio file and text as the response content and JSON payload respectively
    return StreamingResponse(output, headers=headers, media_type="audio/mpeg")



