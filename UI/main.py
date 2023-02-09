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
    def __init__(self)-> None:
        st.title("Speech to Text")
        st.write("This is the speech to text page")

        #create tabs for record or upload file
        tabs = ["Record your speech", "Upload an audio file"]
        record, upload= st.tabs(tabs)

        with record:
            audio_record = audio_recorder()
            if audio_record:
                st.session_state['stt_audio_bytes_input'] = audio_record
                st.success("Recording completed")

        with upload:  
            audio_file = st.file_uploader("Upload a file", type=["wav", "mp3"])
            if audio_file:
                st.session_state['stt_audio_bytes_input'] = audio_file.getvalue()
                st.success("File uploaded successfully")

        try :
            st.header("Preview your audio file")
            if st.session_state['audio_bytes']:
                st.audio(st.session_state['audio_bytes'], format="audio/wav")
                if st.button("Transcribe"):
                    st.session_state['stt_text_output'] = self.stt_api(st.session_state['audio_bytes'])
                if st.session_state['stt_text_output']:
                    st.success("Speech to text completed")
                    st.write(st.session_state['stt_text_output'])
        except KeyError:
            pass


    def stt_api(self, audio: bytes):
        url = "http://127.0.0.1:8000/stt"
        files = {'audio': audio, 'type': 'audio/wav'}
        response = requests.post(url, files=files)
        return response.json()

    def feedback(self, max_wer: int):
        st.title("Feedback Section")
        st.write("Please provide feedback on the model's performance")
        st.slider("Word Error Rate i.e the number of word spelled incorrectly", 0, max_wer, 0,  key="tts_feedback_wer")
        st.text_area("Enter your comment", key="tts_feedback_comment",  help="Please provide feedback on the model's performance")
        if st.button("Submit"):
            st.success("Thank you for your feedback")
            return st.session_state["tts_feedback_wer"], st.session_state["tts_feedback_comment"]


class tts:
    def __init__(self) -> None:
        st.title("Text to Speech")
        st.write("This is the text to speech page")

        text_file = st.file_uploader("Upload a file", type=["txt"])
        if text_file:
            st.session_state['tts_typed_text'] = str(text_file.getvalue(), 'UTF-8')
        
        st.text_area("Preview or edit the text to be converted into a speech", key='tts_typed_text')
        generate_with_text = st.button("Generate Speech! ")
        if generate_with_text:
            st.write("Converting text to speech")
            st.session_state["tts_audio_bytes_ouput"] = self.tts_api(st.session_state['tts_typed_text'])
        try:
            if st.session_state["tts_audio_bytes_ouput"]:
                st.header("Listen bellow to the generated audio file. :)")
                st.audio(st.session_state["tts_audio_bytes_ouput"], format="audio/wav")
                self.feedback(len(st.session_state['tts_typed_text'] .split(" ")))
        except KeyError:
            pass


    def tts_api(self, text: str):
        host = "http://127.0.0.1" #os.environ.get("API_HOST")
        port = 8000 #os.environ.get("API_PORT")
        response = requests.post(f"http://127.0.0.1:8000/tts", json={"text": text})
        with open("sound.wav", "wb") as f:
            f.write(response.content)
        return response.content

    def feedback(self, max_wer: int):
        st.title("Feedback Section")
        st.write("Please provide feedback on the model's performance")
        st.slider("Word Error Rate i.e the number of word spelled incorrectly", 0, max_wer, 0,  key="tts_feedback_wer")
        st.slider("Overall Score including accent", 0, 5, 3, key="tts_feedback_score", help="The score is a combination of the word error rate and the accent score" )
        st.text_area("Enter your comment", key="tts_feedback_comment",  help="Please provide feedback on the model's performance")
        if st.button("Submit"):
            st.success("Thank you for your feedback")
            return st.session_state["tts_feedback_wer"], st.session_state["tts_feedback_score"], st.session_state["tts_feedback_comment"]


def main():

    mode = sidebar()

    if mode == "Home":
        index()
    elif mode == "Speech to Text":
        stt()
    elif mode == "Text to Speech":
        tts()
    


if __name__ == "__main__":
    main()