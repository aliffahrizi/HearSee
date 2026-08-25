import soundfile as sf
import sounddevice as sd

def load_audio(path):
    audio, sample_rate = sf.read(path)
    return audio, sample_rate

def play_audio(audio, sample_rate):
    sd.play(audio, sample_rate)
    
def wait_audio():
    sd.wait()
    
    