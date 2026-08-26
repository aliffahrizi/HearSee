class AudioPlayer:
    def __init__(self, audio, sample_rate):
        self.audio = audio
        self.sample_rate = sample_rate
        self.duration = len(audio) / sample_rate