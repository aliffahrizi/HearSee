import matplotlib.pyplot as plt


def plot_spectrogram(t, f, magnitude_db, song_name, figsize=(20,10)):

    fig, ax = plt.subplots(figsize=figsize)
    mesh = ax.pcolormesh(
        t,
        f,
        magnitude_db,
        shading="gouraud",
        cmap="inferno",
        vmin=-120,
        vmax=0
    )

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_yscale("log")
    ax.set_ylim(20, 20000)
    ax.set_title(song_name)

    fig.colorbar(
        mesh,
        ax=ax,
        label="Magnitude (dB)"
    )

    return fig, ax

def update_cursor(cursor, elapsed):
    cursor.set_xdata([elapsed, elapsed])