import os
import numpy as np
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
WILLIAM_ECG = os.path.join(HERE, "ecg/william_ecg_1.tsv")
FS = 250 #Hz

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

def plot(time, ecg, freqs, db):
    fig, (time_ax, spec_ax) = plt.subplots(2, 1, figsize=(6.3, 4))

    time_ax.plot(time, ecg, linewidth=0.5)
    time_ax.set_xlabel("Time (s)")
    time_ax.set_ylabel("Amplitude (V)")
    time_ax.set_xlim(0, time[-1])
    time_ax.grid(alpha=0.3)

    spec_ax.semilogx(freqs, db, linewidth=0.5)
    spec_ax.set_xlabel("Frequency (Hz)")
    spec_ax.set_ylabel("Amplitude (dB)")
    spec_ax.grid(which="both", alpha=0.3)

    fig.tight_layout()

if __name__ == "__main__":
    time, ecg = load_signal(WILLIAM_ECG)
    freqs, db = time_to_freq(ecg)
    plot(time, ecg, freqs, db)
    plt.show()