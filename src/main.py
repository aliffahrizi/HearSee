import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from scipy.signal import stft
import time
from pathlib import Path
from analysis import calculate_stft

BASE_DIR = Path(__file__).resolve().parent.parent
audio_path = BASE_DIR / "audio" / "The xx - Intro.flac"

song_name = 'Intro'

audio, sampleRate = sf.read(audio_path)

print(f'Audio shape: {audio.shape}')
print(f'Sample rate: {sampleRate}')

duration = 5
n_samples = int(duration * sampleRate)

# Audio separation for 10 secs
x = audio[:n_samples, :]
x_left = audio[:n_samples, 0]
x_right = audio[:n_samples, 1]

f, t, magnitude_db = calculate_stft(x_left, sampleRate)

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

fig.subplots_adjust(bottom=0.22)
info_text = ax.text(
    0.02, -0.15,
    "",
    transform=ax.transAxes,
    verticalalignment="top"
)

def mouse_move(event):
    if event.inaxes == ax:
        
        mouse_time = event.xdata
        mouse_freq = event.ydata

        time_index = np.argmin(np.abs(t - mouse_time))
        freq_index = np.argmin(np.abs(f - mouse_freq))

        magnitude = magnitude_db[freq_index, time_index]

        info_text.set_text(
            f"Time: {mouse_time:.2f} s\n"
            f"Frequency: {mouse_freq:.1f} Hz\n"
            f"Magnitude: {magnitude:.1f} dB"
        )
        fig.canvas.draw_idle()


fig.canvas.mpl_connect(
    "motion_notify_event",
    mouse_move
)

plt.show()
# plt.show(block=False)

# plt.pause(10)

# sd.play(audio[:n_samples, :], sampleRate)
# start_time = time.perf_counter()

# while sd.get_stream().active:
#     elapsed = time.perf_counter() - start_time

#     cursor.set_xdata([elapsed, elapsed])

#     plt.pause(0.01)

# sd.wait()
# plt.close()