import soundfile as sf
import sounddevice as sd

def load_audio(path):
    audio, sample_rate = sf.read(path)
    return audio, sample_rate

def play_audio(audio, sample_rate):
    sd.play(audio, sample_rate)
    
def wait_audio():
    sd.wait()
    
def get_audio_duration(audio, sample_rate):
    duration = len(audio) / sample_rate
    return duration