import streamlit as st 
from audio_recorder_streamlit import audio_recorder
import requests
import json

#Set app configuration
st.set_page_config(page_title="RW Deep Speech UI",  initial_sidebar_state="expanded")


def sidebar():
    options = st.sidebar.selectbox("Select a model", ["Translation", "Speech to Text", "Text to Speech"])
    st.sidebar.success("If you would like to contribute to the development of the models, please visit the [Github repository](github.com/agent87)")
    return options

# class index:
#     host = "http://127.0.0.1"
#     port = 8000
#     domain = host + ':' + str(port)
#     def __init__(self):
#         st.title("Kinyarwanda Deep Speech UI")
#         st.write("This is a user interface for the Kinyarwanda speech to text and text to speech models. The aim of this setup is to collect feedback from the general non-technical public on the performance of the models.")
#         ### STT DOCUMENTATION ###
#         self.stt_docs()

#         ### TTS DOCUMENTATION ###
#         self.tts_docs()
    
#     def stt_docs(self):
#         st.header("Speech to text documentation")
#         st.write(f"To transcribe using this endpoint use the following commands")
#         python, curl , javascript , Go= st.tabs(["Python", "Curl", "Javascript", "Go"])

#         with python:
#             st.code("import requests \n ")

#     def tts_docs(self):
#         st.header("Text to speech endpoint documentation")
#         st.write(f"To generate a voice audio using this endpoint use the following commands")
#         python, curl , javascript , Go= st.tabs(["Python", "Curl", "Javascript", "Go"])

#         with python:
#             with open("examples/tts/python.py", 'r') as f:
#                 py_code = f.read()
#             st.code(py_code)
        
#         with curl:
#             st.code("""curl -X POST -H "Content-Type: application/json" -d '{"text":"Mukomeze mugire ibihe byiza!"}' "https://domain.com:8000/tts" -o audio.wav""")
        
#         with javascript:
#             with open("examples/tts/javascript.js", 'r') as f:
#                 js_code = f.read()
#             st.code(js_code)

#         with Go:
#             with open("examples/tts/golang.go", 'r') as f:
#                 go_code = f.read()
#             st.code(go_code)


class translation:
    def __init__(self) -> None:
        st.title("Machine Translation")
        st.write("Kinyarwanda to English Translation Engine")
        translation_mode = st.sidebar.selectbox("Select a model", ["Kinyarwanda to English", "English to Kinyarwanda"])

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
        response = requests.post(f"http://127.0.0.1:8000/tts", json={"text": text})
        return response.content

    def feedback(self, max_wer: int, feedback_token: str = None):
        with st.form("Feedback Form"):
            st.title("Feedback Section")
            st.write("Please provide feedback on the model's performance")
            st.slider("Overall Score including accent", 0, 5, 3, key="tts_feedback_score", help="The score is a combination of the word error rate and the accent score" )
            st.slider("Word Pronounced in the wrong way i.e the number of word spelled incorrectly", 0, max_wer, 0,  key="tts_feedback_wer")
            st.text_area("Enter your comment", key="tts_feedback_comment",  help="Please provide feedback on the model's performance")
            if st.form_submit_button("Submit Feedback"):
                st.success("Thank you for your feedback")
                return st.session_state["tts_feedback_wer"], st.session_state["tts_feedback_score"], st.session_state["tts_feedback_comment"]



class stt:
    def __init__(self)-> None:
        st.title("Speech to Text")
        st.write("This is the speech to text page")

        #create tabs for record or upload file
        tabs = ["Record your speech", "Upload an audio file"]
        record, upload= st.tabs(tabs)

        with record:
            with st.form("Record Voice"):
                audio_record = audio_recorder()
                if st.form_submit_button("Listen to recording.") and audio_record:
                    st.session_state['stt_audio_bytes_input'] = audio_record
                    st.success("Recording completed")

        with upload:  
            audio_file = st.file_uploader("Upload a file", type=["wav", "mp3"])
            if audio_file:
                st.session_state['stt_audio_bytes_input'] = audio_file.getvalue()
                st.success("File uploaded successfully")

        try :
            if st.session_state['stt_audio_bytes_input']:
                st.header("Preview your audio file")
                st.audio(st.session_state['stt_audio_bytes_input'], format="audio/wav")
                transcribe =  st.button("Transcribe")
                if transcribe:
                    st.session_state['stt_text_output'] = self.stt_api(audio=st.session_state['stt_audio_bytes_input'])
                if st.session_state['stt_text_output']:
                    st.success("Speech to text completed")
                    st.write(st.session_state['stt_text_output'])
        except KeyError:
            pass


    def stt_api(self, audio: bytes):
        form_data = {"audio_bytes": audio }
        response = requests.post(f"http://34.69.164.74:15672/transcribe/", data=form_data)
        return response.text

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
        response = requests.post(f"http://127.0.0.1:8000/tts", json={"text": text})
        return response.content

    def feedback(self, max_wer: int, feedback_token: str = None):
        with st.form("Feedback Form"):
            st.title("Feedback Section")
            st.write("Please provide feedback on the model's performance")
            st.slider("Overall Score including accent", 0, 5, 3, key="tts_feedback_score", help="The score is a combination of the word error rate and the accent score" )
            st.slider("Word Pronounced in the wrong way i.e the number of word spelled incorrectly", 0, max_wer, 0,  key="tts_feedback_wer")
            st.text_area("Enter your comment", key="tts_feedback_comment",  help="Please provide feedback on the model's performance")
            if st.form_submit_button("Submit Feedback"):
                st.success("Thank you for your feedback")
                return st.session_state["tts_feedback_wer"], st.session_state["tts_feedback_score"], st.session_state["tts_feedback_comment"]


def main():

    mode = sidebar()

    if mode == "Translation":
        translation()
    elif mode == "Speech to Text":
        stt()
    elif mode == "Text to Speech":
        tts()
    
#

if __name__ == "__main__":
    main()