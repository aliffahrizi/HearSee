import matplotlib.pyplot as plt
import numpy as np
import time
from pathlib import Path
from analysis import calculate_stft, get_spectrogram_value
from audio import *
from visualization import plot_spectrogram, update_cursor


BASE_DIR = Path(__file__).resolve().parent.parent
audio_path = BASE_DIR / "audio" / "The xx - Intro.flac"

song_name = 'Intro'

audio, sampleRate = load_audio(audio_path)
song_duration = get_audio_duration(audio, sampleRate)

print(f'Audio shape: {audio.shape}')
print(f'Sample rate: {sampleRate}')
print(f'Song duration: {song_duration}')

analysis_duration = song_duration
n_samples = int(analysis_duration * sampleRate)

x = audio[:n_samples, :]
x_left = audio[:n_samples, 0]
x_right = audio[:n_samples, 1]

f, t, magnitude_db = calculate_stft(x_left, sampleRate)

fig, ax = plot_spectrogram(t, f, magnitude_db, song_name)
cursor = ax.axvline(0)


fig.subplots_adjust(bottom=0.22)
info_text = ax.text(
    -0.12, -0.075,
    "",
    transform=ax.transAxes,
    verticalalignment="top"
)

def mouse_move(event):
    if event.inaxes == ax:

        mouse_time = event.xdata
        mouse_freq = event.ydata

        magnitude = get_spectrogram_value(
            mouse_time,
            mouse_freq,
            t,
            f,
            magnitude_db
        )

        print(
            f"Time: {mouse_time:.2f} s |"
            f"Frequency: {mouse_freq:.1f} Hz |"
            f"Magnitude: {magnitude:.1f} dB"
        )

        fig.canvas.draw_idle()


fig.canvas.mpl_connect(
    "motion_notify_event",
    mouse_move
)

# plt.show()
plt.show(block=False)
plt.pause(1)

fig.canvas.draw()
background = fig.canvas.copy_from_bbox(ax.bbox)

sd.play(audio[:n_samples, :], sampleRate)
start_time = time.perf_counter()

while sd.get_stream().active:
    elapsed = time.perf_counter() - start_time

    fig.canvas.restore_region(background)

    update_cursor(cursor, elapsed)

    ax.draw_artist(cursor)

    fig.canvas.blit(ax.bbox)
    fig.canvas.flush_events()
 
#     print(
#     f"elapsed: {elapsed:.3f} | "
#     f"cursor: {elapsed:.3f}"
# )

sd.wait()
plt.close()