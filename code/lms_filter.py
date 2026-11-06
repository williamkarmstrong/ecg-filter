import numpy as np
import matplotlib.pyplot as plt
from fir_filter import FIRfilter
from fir_design import design
from ecg_plot import load_signal, plot, plot_zoom, plot_spectra, WILLIAM_ECG, FS, BANDS

LEARNING_RATE = 0.05

if __name__ == "__main__":
    time, ecg = load_signal(WILLIAM_ECG)

    n = np.arange(len(ecg))
    ref_noise = np.sin(2 * np.pi * 50 / FS * n)

    # Remove DC with a high pass filter
    high_pass = FIRfilter(design(FS, [(0, 0.5)]))
    lms = FIRfilter(np.zeros(2))

    # Bandstop FIR for comparison
    fir = FIRfilter(design(FS, BANDS))

    lms_cleaned = np.zeros(len(ecg))
    fir_filtered = np.zeros(len(ecg))
    for i in range(len(ecg)):
        x = high_pass.dofilter(ecg[i])
        lms_cleaned[i] = lms.doFilterAdaptive(x, ref_noise[i], LEARNING_RATE)
        fir_filtered[i] = fir.dofilter(ecg[i])

    # Skip the first M samples while the delay lines fill
    M = high_pass.N
    time, ecg, lms_cleaned, fir_filtered = time[M:], ecg[M:], lms_cleaned[M:], fir_filtered[M:]

    plot(time, lms_cleaned, "lms_cleaned_ecg")
    plot_zoom(time, {"FIR bandstop": fir_filtered, "High-pass + LMS": lms_cleaned}, "fir_vs_lms_zoom")
    plot_spectra({"Raw": ecg, "FIR bandstop": fir_filtered, "High-pass + LMS": lms_cleaned}, "fir_vs_lms_spectrum")
    plt.show()
