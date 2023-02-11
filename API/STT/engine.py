import nemo.collections.asr as nemo_asr
from pydub import AudioSegment
import pyaudioconvert as pac
import os

#import the model using hugging face 
hf_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(model_name="mbazaNLP/Kinyarwanda_nemo_stt_conformer_model")


def convert(file_id: int):
    # if file_name.endswith("mp3"):
    #     sound = AudioSegment.from_mp3(audio.name)
    #     sound.export(audio.name, format="wav")
    # elif file_name.endswith("ogg"):
    #     sound = AudioSegment.from_ogg(audio.name)
    #     sound.export(audio.name, format="wav")
    # elif filename.endswith("wav"):
    #     pass
    # else:
    #     return False  
    # pac.convert_wav_to_16bit_mono(audio.name,audio.name)
    # return True
    pass

class transcriber:
    workdir = f"STT/sounds/"
    def __init__(self, audio_bytes : bytes) -> None:
        #Save the audio bytes file
        self.file_id : int = len(os.listdir("STT/sounds")) + 1
        with open(f"STT/sounds/sound-{self.file_id}.wav", "wb") as audio_file:
            audio_file.write(audio_bytes)

        #convert the audio file
        if self.convert_wav_to_16bit_mono():
            print("Done!")
        else:
            print('unnable to')


        #transcribe and store to text var in class
        #self.text = self.transcribe()


    def convert_wav_to_16bit_mono(self):
        try:
            file_path = self.workdir + f"sound-{self.file_id}.wav"
            pac.convert_wav_to_16bit_mono(file_path,file_path)
            return True
        except FileNotFoundError:
            return False
        
    def transcribe(self):
        try:
            file_path = self.workdir + f"sound-{self.file_id}.wav"
            result= hf_model.transcribe([file_path])
            return result[0]
        except FileNotFoundError:
            return "Unable to transcribe audio!"


        

