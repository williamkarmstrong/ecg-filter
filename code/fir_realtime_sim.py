import numpy as np
import matplotlib.pyplot as plt
from ecg_plot import load_signal, plot, plot_zoom, WILLIAM_ECG, FS, BANDS
from fir_design import design
from fir_filter import FIRfilter

if __name__ == "__main__":
    time, ecg = load_signal(WILLIAM_ECG)

    coefficients = design(FS, BANDS)
    fir_filter = FIRfilter(coefficients)

    filtered_ecg = np.zeros_like(ecg)
    for i in range(len(ecg)):
        filtered_ecg[i] = fir_filter.dofilter(ecg[i])

    # Skip the first M samples while the delay line fills
    M = len(coefficients)
    plot(time[M:], filtered_ecg[M:], "filtered_ecg")

    # Linear-phase FIR delays the output by (M - 1) / 2 samples, shift it back to line up with the raw ECG
    D = M // 2
    plot_zoom(time[:-D], {"Raw": ecg[:-D], "FIR filtered": filtered_ecg[D:]}, "filtered_ecg_zoom")
    plt.show()
