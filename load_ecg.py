import os
import numpy as np
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
PLOTS = os.path.join(HERE, "plots")
WILLIAM_ECG = os.path.join(HERE, "ecg/william_ecg_1.tsv")

SAVE = True

FS = 250 #Hz
ZOOM_START, ZOOM_END = 20, 23 #s

def load_signal(file):
    data = np.loadtxt(file)
    time = data[:, 0]
    ecg = data[:, 8]
    return time, ecg

def time_to_freq(ecg):
    n = len(ecg)
    spectrum = np.fft.fft(ecg)
    bins = np.arange(1, n // 2 + 1)
    freqs = bins * FS / n
    amp = 2 * np.abs(spectrum[bins]) / n
    return freqs, 20 * np.log10(amp)

def plot(time, ecg, freqs, db, filename):
    fig, (time_ax, spec_ax) = plt.subplots(2, 1, figsize=(6.3, 4))

    time_ax.plot(time, (ecg - ecg.mean()) * 1000, linewidth=0.5)
    time_ax.set_xlabel("Time (s)")
    time_ax.set_ylabel("Amplitude (mV)")
    time_ax.set_xlim(0, time[-1])
    time_ax.grid(alpha=0.3)

    spec_ax.semilogx(freqs, db, linewidth=0.5)
    spec_ax.set_xlabel("Frequency (Hz)")
    spec_ax.set_ylabel("Amplitude (dBV)")
    spec_ax.grid(which="both", alpha=0.3)

    fig.tight_layout()
    save_svg(fig, filename)

def plot_zoom(time, ecg, filename):
    fig, zoom_ax = plt.subplots(figsize=(6.3, 2.5))
    zoom = (time >= ZOOM_START) & (time <= ZOOM_END)

    zoom_ax.plot(time[zoom], (ecg[zoom] - ecg.mean()) * 1000, linewidth=0.8)
    zoom_ax.set_xlabel("Time (s)")
    zoom_ax.set_ylabel("Amplitude (mV)")
    zoom_ax.set_xlim(ZOOM_START, ZOOM_END)
    zoom_ax.grid(alpha=0.3)

    fig.tight_layout()
    save_svg(fig, filename)

def save_svg(fig, filename):
    if SAVE:
        os.makedirs(PLOTS, exist_ok=True)
        fig.savefig(os.path.join(PLOTS, filename + ".svg"))

if __name__ == "__main__":
    time, ecg = load_signal(WILLIAM_ECG)
    freqs, db = time_to_freq(ecg)
    plot(time, ecg, freqs, db, "full_ecg")
    plot_zoom(time, ecg, "zoomed_ecg")
    plt.show()