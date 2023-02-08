import streamlit as st 
from audio_recorder_streamlit import audio_recorder
import requests
import os

#Set app configuration
st.set_page_config(page_title="RW Deep Speech UI", page_icon="🗣️",  initial_sidebar_state="expanded")

def project_info():
    st.sidebar.success("If you would like to contribute to the development of the models, please visit the [Github repository](github.com/agent87)")

def sidebar():
    options = st.sidebar.selectbox("Select a model", ["Home", "Speech to Text", "Text to Speech"])
    project_info()
    return options

def index():
    st.title("Kinyarwanda Deep Speech UI")
    st.write("This is a user interface for the Kinyarwanda speech to text and text to speech models. The aim of this setup is to collect feedback from the general non-technical public on the performance of the models.")

#Set of Global variables to be used in the stt
input_audio_bytes = None
output_audio_bytes = None


#Set of Global variables to be used in the tts
input_text : str = None
output_audio_bytes : bytes = None


class stt:
    def view()-> None:
        st.title("Speech to Text")
        st.write("This is the speech to text page")

        #create tabs for record or upload file
        tabs = ["Record your speech", "Upload an audio file"]
        record, upload= st.tabs(tabs)

        with record:
            audio_bytes = audio_recorder()
            if audio_bytes:
                st.audio(audio_bytes, format="audio/wav")
            stt.feedback(10)

        with upload:  
            st.file_uploader("Upload a file", type=["wav", "mp3"])


    def stt_api(audio):
        url = "http://127.0.0.1:8000/stt"
        files = {'file': open(audio.name, 'rb')}
        response = requests.post(url, files=files)
        return response.json()

    def feedback(max_wer: int):
        st.title("Feedback Section")
        st.write("Please provide feedback on the model's performance")
        wer = st.slider("Word Error Rate i.e: the number of words incorectly transcribed", 0, max_wer, 0)
        score = st.slider("Overall Score", 0, 5, 3)
        comment = st.text_area("Enter your comment")
        if st.button("Submit"):
            st.write("Submitting feedback")


class tts:
    def view() -> None:
        global audio_bytes
        st.title("Text to Speech")
        st.write("This is the text to speech page")
        tabs = ["Type your sentence", "Upload a text file"]
        type, upload= st.tabs(tabs)

        with type:
            text = st.text_area("Enter the text to be converted to speech")
            upload_type = st.button("Convert")
            if upload_type:
                st.write("Converting text to speech")
                audio_bytes = tts.tts_api(text)
                st.audio(audio_bytes, format="audio/wav")
                tts.feedback(len(text.split(" ")))

        with upload:
            text_file = st.file_uploader("Upload a file", type=["txt"])
            if text_file:
                text = text_file.read()
                upload_button =  st.button("Convert")
                if upload_button:
                    st.write("Converting text to speech")
                    audio_bytes = tts.tts_api(text)
                    st.audio(audio_bytes, format="audio/wav")
                    tts.feedback(len(text.split(" ")))


    def tts_api(text):
        host = "http://127.0.0.1" #os.environ.get("API_HOST")
        port = 8000 #os.environ.get("API_PORT")
        response = requests.post(f"http://127.0.0.1:8000/tts", json={"text": text})
        with open("sound.wav", "wb") as f:
            f.write(response.content)
        return response.content
    

    def feedback(max_wer: int):
        st.title("Feedback Section")
        st.write("Please provide feedback on the model's performance")
        global wer, score, comment
        wer = st.slider("Word Error Rate i.e the number of word spelled incorrectly", 0, max_wer, 0)
        score = st.slider("Overall Score including accent", 0, 5, 3)
        comment = st.text_area("Enter your comment")
        if st.button("Submit"):
            st.write("Submitting feedback")
            st.success("Thank you for your feedback")


def main():

    mode = sidebar()

    if mode == "Home":
        index()
    elif mode == "Speech to Text":
        #stt.view()
        pass
    elif mode == "Text to Speech":
        tts.view()
    


if __name__ == "__main__":
    main()