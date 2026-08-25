from scipy.signal import stft
import numpy as np

def calculate_stft(audio, sample_rate, nperseg = 2048, noverlap=1024):
    f, t, Zxx = stft(
        audio, 
        fs=sample_rate, 
        nperseg=nperseg, 
        noverlap=noverlap
    )
    
    magnitude_db = 20 * np.log10(np.abs(Zxx) + 1e-10)
    
    return f, t, magnitude_db

def get_spectrogram_value(
    mouse_time,
    mouse_freq,
    t,
    f,
    magnitude_db
):
    time_index = np.argmin(np.abs(t - mouse_time))
    freq_index = np.argmin(np.abs(f - mouse_freq))

    magnitude = magnitude_db[freq_index, time_index]

    return magnitude