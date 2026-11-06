import numpy as np
import matplotlib.pyplot as plt
from ecg_plot import WILLIAM_ECG, SHREYAS_ECG, BANDS, FS, load_signal, save_svg
from fir_design import design
from fir_filter import FIRfilter

# One QRS complex in Shreyas's raw ECG (s), used as the template
BEAT_START, BEAT_END = 22.38, 22.51
MAX_BPM = 200

def fir_filter(x, coefficients):
    fir = FIRfilter(coefficients)
    return np.array([fir.dofilter(v) for v in x])

def matched_filter(signal, template):
    return fir_filter(signal, template[::-1]) ** 2

def find_peaks(signal, threshold):
    min_gap = FS * 60 / MAX_BPM  # samples between beats at MAX_BPM
    peaks = []
    for i in range(len(signal)):
        if signal[i] >= threshold and (len(peaks) == 0 or i - peaks[-1] > min_gap):
            peaks.append(i)
    return np.array(peaks)

def calculate_bpm(time, ecg, template_ecg):
    # Remove DC and mains from both ECGs with the bandstop FIR
    h = design(FS, BANDS)
    ecg = fir_filter(ecg, h)
    template_ecg = fir_filter(template_ecg, h)
    
    # The linear-phase FIR delays by (M - 1) / 2 samples, so shift the template window by that
    M = len(h)
    delay = (M - 1) // 2
    template = template_ecg[int(BEAT_START * FS) + delay : int(BEAT_END * FS) + delay]
    
    # Skip the first M samples while the delay line fills
    matched = matched_filter(ecg, template)[M:]
    time = time[M:]
    
    # Smallest peaks reach approx. 55% of the largest
    peaks = find_peaks(matched, 0.4 * matched.max())
    peak_times = time[peaks]
    bpm = 60 / np.diff(peak_times)

    return matched, bpm, peaks, peak_times

def plot_heartrate(matched, bpm, peaks, peak_times):
    fig, (match_ax, bpm_ax) = plt.subplots(2, 1, figsize=(6.3, 4))
    
    match_ax.plot(time, matched / matched.max(), linewidth=0.5)
    match_ax.plot(peak_times, matched[peaks] / matched.max(), "x", markersize=4)
    match_ax.set_xlabel("Time (s)")
    match_ax.set_ylabel("Matched output")
    match_ax.set_xlim(time[0], time[-1])
    match_ax.grid(alpha=0.3)
    
    bpm_ax.step(peak_times[1:], bpm, where="post", linewidth=0.8)
    bpm_ax.set_xlabel("Time (s)")
    bpm_ax.set_ylabel("Heart rate (BPM)")
    bpm_ax.set_xlim(time[0], time[-1])
    bpm_ax.grid(alpha=0.3)
    
    fig.tight_layout()
    save_svg(fig, "heart_rate")
    plt.show()

if __name__ == "__main__":
    time, ecg = load_signal(WILLIAM_ECG)
    _, template_ecg = load_signal(SHREYAS_ECG)

    matched, bpm, peaks, peak_times = calculate_bpm(time, ecg, template_ecg)
    plot_heartrate(matched, bpm, peaks, peak_times)
