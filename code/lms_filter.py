import numpy as np
import matplotlib.pyplot as plt
from fir_filter import FIRfilter
from ecg_plot import load_signal, time_to_freq, plot, plot_zoom, WILLIAM_ECG, PLOTS, FS

if __name__ == "__main__":
    time, ecg = load_signal(WILLIAM_ECG)
    
    r_noise = np.sin(2 * np.pi * 50 * time)
    
    lms = FIRfilter(np.zeros(31))
    
    learningRate = 0.01
    
    lms_cleaned = np.zeros_like(ecg)
    for i in range(len(ecg)):
        lms_cleaned[i] = lms.doFilterAdaptive(ecg[i], r_noise[i], learningRate)
    
    freqs_lms, db_lms = time_to_freq(lms_cleaned)
    plot(time, lms_cleaned, freqs_lms, db_lms, "lms_cleaned_ecg")
    plot_zoom(time, lms_cleaned, "lms_cleaned_ecg_zoom")
    plt.show()
    