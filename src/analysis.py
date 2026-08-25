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