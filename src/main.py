import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from scipy.signal import stft, spectrogram
from matplotlib.animation import FuncAnimation
import time

song_name = 'Intro'

audio, sampleRate = sf.read(r"audio\The xx - Intro.flac")
print(f'Audio shape: {audio.shape}')
print(f'Sample rate: {sampleRate}')

t = np.arange(len(audio)) / sampleRate

# duration = np.max(t) / 5
duration = 10
n_samples = int(duration * sampleRate)

# audio separation for 10 secs
x = audio[:n_samples, :]
x_left= audio[:n_samples, 0]
x_right = audio[:n_samples, 1]  
    
    
f, t, Zxx = stft(x_right, fs=sampleRate, nperseg=2048, noverlap=1024
)

magnitude_db = 20 * np.log10(np.abs(Zxx) + 1e-10)

fig, ax = plt.subplots()

mesh = ax.pcolormesh(
    t,
    f,
    magnitude_db,
    shading="gouraud",
    cmap="inferno",
    vmin=-120,
    vmax=0
)
cursor = ax.axvline(0)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Frequency (Hz)")
ax.set_yscale("log")
ax.set_ylim(20, 20000)
ax.set_title(song_name)



sd.play(audio[:n_samples, :], sampleRate)
start_time = time.perf_counter()
fig.colorbar(mesh, ax=ax, label="Magnitude (dB)")
plt.show(block=False)
while sd.get_stream().active:
    elapsed = time.perf_counter() - start_time
    cursor.set_xdata([elapsed, elapsed])
    plt.pause(0.01)

sd.wait()
plt.close()
