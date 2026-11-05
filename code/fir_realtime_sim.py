import numpy as np
import matplotlib.pyplot as plt
from ecg_plot import load_signal, time_to_freq, plot, plot_zoom, WILLIAM_ECG, PLOTS, FS
from fir_design import design, BANDS
from fir_filter import FIRfilter

if __name__ == "__main__":
    time, ecg = load_signal(WILLIAM_ECG)
    
    coefficients = design(FS, BANDS)
    fir_filter = FIRfilter(coefficients)
    
    filtered_ecg = np.zeros_like(ecg)
    for i in range(len(ecg)):
        filtered_ecg[i] = fir_filter.doFilter(ecg[i])
        
    freqs_filt, db_filt = time_to_freq(filtered_ecg)
    plot(time, filtered_ecg, freqs_filt, db_filt, "filtered_ecg")
    plot_zoom(time, filtered_ecg, "filtered_ecg_zoom")
    plt.show()
    
    