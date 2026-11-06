import os
import numpy as np
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLOTS = os.path.join(ROOT, "plots")
WILLIAM_ECG = os.path.join(ROOT, "ecg", "william_ecg_1.tsv")

SAVE = True

FS = 250 #Hz
BANDS = [
    (0, 0.5),
    (45, 55),
    (95, 105)
]
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

def plot(time, ecg, filename):
    """Full ECG in the time domain and its spectrum"""
    fig, (time_ax, spec_ax) = plt.subplots(2, 1, figsize=(6.3, 4))

    time_ax.plot(time, (ecg - ecg.mean()) * 1000, linewidth=0.5)
    time_ax.set_xlabel("Time (s)")
    time_ax.set_ylabel("Amplitude (mV)")
    time_ax.set_xlim(time[0], time[-1])
    time_ax.grid(alpha=0.3)

    spec_ax.plot(*time_to_freq(ecg), linewidth=0.5)
    spec_ax.set_xlabel("Frequency (Hz)")
    spec_ax.set_ylabel("Amplitude (dBV)")
    spec_ax.set_xlim(0, FS / 2)
    spec_ax.grid(alpha=0.3)

    fig.tight_layout()
    save_svg(fig, filename)

def plot_zoom(time, signals, filename):
    """Overlay a few heartbeats of each signal (dict of label: ecg)"""
    fig, zoom_ax = plt.subplots(figsize=(6.3, 2.5))
    zoom = (time >= ZOOM_START) & (time <= ZOOM_END)

    for label, ecg in signals.items():
        zoom_ax.plot(time[zoom], (ecg[zoom] - ecg[zoom].mean()) * 1000, linewidth=0.8, label=label)
    zoom_ax.set_xlabel("Time (s)")
    zoom_ax.set_ylabel("Amplitude (mV)")
    zoom_ax.set_xlim(ZOOM_START, ZOOM_END)
    zoom_ax.grid(alpha=0.3)
    if len(signals) > 1:
        zoom_ax.legend(fontsize=7)

    fig.tight_layout()
    save_svg(fig, filename)

def plot_spectra(signals, filename):
    """Overlay the spectrum of each signal (dict of label: ecg)"""
    fig, spec_ax = plt.subplots(figsize=(6.3, 2.5))

    for label, ecg in signals.items():
        # Raw in grey so the filtered signals keep the same colours as in plot_zoom
        color = "0.7" if label == "Raw" else None
        spec_ax.plot(*time_to_freq(ecg), linewidth=0.5, label=label, color=color)
    spec_ax.set_xlabel("Frequency (Hz)")
    spec_ax.set_ylabel("Amplitude (dBV)")
    spec_ax.set_xlim(0, FS / 2)
    spec_ax.grid(alpha=0.3)
    legend = spec_ax.legend(fontsize=7)
    for line in legend.get_lines():
        line.set_linewidth(2)

    fig.tight_layout()
    save_svg(fig, filename)

def save_svg(fig, filename):
    if SAVE:
        os.makedirs(PLOTS, exist_ok=True)
        fig.savefig(os.path.join(PLOTS, filename + ".svg"))

if __name__ == "__main__":
    time, ecg = load_signal(WILLIAM_ECG)
    plot(time, ecg, "full_ecg")
    plot_zoom(time, {"Raw": ecg}, "zoomed_ecg")
    
    plt.show()