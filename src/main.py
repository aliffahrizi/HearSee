import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from scipy.signal import stft
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
audio_path = BASE_DIR / "audio" / "The xx - Intro.flac"

song_name = 'Intro'

audio, sampleRate = sf.read(audio_path)

print(f'Audio shape: {audio.shape}')
print(f'Sample rate: {sampleRate}')

duration = 10
n_samples = int(duration * sampleRate)

# Audio separation for 10 secs
x = audio[:n_samples, :]
x_left = audio[:n_samples, 0]
x_right = audio[:n_samples, 1]

f, t, Zxx = stft(
    x_right,
    fs=sampleRate,
    nperseg=2048,
    noverlap=1024
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

fig.colorbar(mesh, ax=ax, label="Magnitude (dB)")


def mouse_move(event):
    if event.inaxes == ax:
        print(
            f"Time: {event.xdata:.2f} s | "
            f"Frequency: {event.ydata:.1f} Hz"
        )


fig.canvas.mpl_connect(
    "motion_notify_event",
    mouse_move
)

plt.show(block=False)

# Give Matplotlib time to render
plt.pause(1)

sd.play(audio[:n_samples, :], sampleRate)
start_time = time.perf_counter()

while sd.get_stream().active:
    elapsed = time.perf_counter() - start_time

    cursor.set_xdata([elapsed, elapsed])

    plt.pause(0.01)

sd.wait()
plt.close()