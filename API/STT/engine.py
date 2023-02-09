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
    file_name = f"STT/sounds/sound-{file_id}.wav"
    pac.convert_wav_to_16bit_mono(file_name,file_name)


def transcribe(file_id: str):#):
    # audio = audio_microphone if audio_microphone else audio
    #if convert(audio) == False:
    #    return "The format must be mp3,wav and ogg"
    #file_path = os.path.abspath(file_id)[0]
    #print(file_path)
    result= hf_model.transcribe([f"STT/sounds/sound-{file_id}.wav"])
    return result

