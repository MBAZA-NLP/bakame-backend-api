from fastapi import FastAPI


mbaza = FastAPI(title='Mbaza Chatbot API')


@mbaza.post('/')
def index():
    return "This is the landing page of the chatbot"


@mbaza.get('/stt') #path
def stt(auth: str = None, recording: str = None):
    print(auth)
    print(recording)
    return "This is the mbaza stt section of the chatbot"


@mbaza.get('/tts') #path
def tts(auth: str = None, text: str = None):
    return "This is the mbaza tts section of the chatbot"

