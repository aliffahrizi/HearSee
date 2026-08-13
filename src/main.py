import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from scipy.signal import stft, spectrogram

song_name = 'Daydreaming'

audio, sampleRate = sf.read(r"audio\Radiohead - Daydreaming.flac")
print(f'Audio shape: {audio.shape}')
print(f'Sample rate: {sampleRate}')

time = np.arange(len(audio)) / sampleRate

# plt.plot(time, audio[:, 0])
# plt.xlabel("Time")
# plt.ylabel("Amplitude")
# plt.show()


duration = 10
n_samples = int(duration * sampleRate)

x = audio[:n_samples, :]
x_left= audio[:n_samples, 0]
x_right = audio[:n_samples, 1]  

# X = np.fft.rfft(x)
# freq = np.fft.rfftfreq(len(x), 1 / sampleRate)

# magnitude = np.abs(X)

# plt.plot(freq, magnitude)

# plt.xlabel("Frequency (Hz)")
# plt.ylabel("Magnitude")
# plt.title("FFT of Daydreaming")
# plt.xscale("log")
# plt.xlim(20, 20000)

# plt.show()


sd.play(x)
# sd.wait()




freq, time, Zxx = stft(x_right, fs=sampleRate, nperseg=2048, noverlap=1024)

# magnitude = np.abs(Zxx)
magnitude_db = 20 * np.log10(np.abs(Zxx) + 1e-10)

plt.pcolormesh(time, freq, magnitude_db, shading='gouraud', cmap='inferno', vmin=-120, vmax=0)
plt.colorbar(label='Magnitude (dB)')
plt.xlabel('Time (s)')
plt.yscale('log')
plt.ylim(20, 20000)
plt.ylabel('Frequency (Hz)')
plt.title(song_name)
plt.show()
# freq, time, Sxx = stft(x, fs=sampleRate, nperseg=2048, noverlap=1024)

# # magnitude = np.abs(Zxx)
# magnitude_db = 20 * np.log10(np.abs(Zxx) + 1e-10)

# plt.pcolormesh(time, freq, magnitude_db, shading='gouraud', cmap='inferno', vmin=-160, vmax=0)
# plt.colorbar(label='Magnitude (dB)')
# plt.xlabel('Time (s)')
# plt.yscale('log')
# plt.ylim(20, 20000)
# plt.ylabel('Frequency (Hz)')
# plt.title(song_name)
# plt.show()