import numpy as np
import matplotlib.pyplot as plt
from ecg_plot import save_svg, FS, BANDS

def design(fs, bands):
    """
    Design of the function to create the desired FIR co-efficients
    M: number of taps (co-efficients)
    H: desired frequency response
    h: time domain of H
    k: frequency bin index
    """
    M = int(fs / min(high - low for low, high in bands))
    M += M % 2 == 0
    
    H = np.ones(M)                    
    
    for low, high in bands:
        k_low, k_high = int(low * M / fs), int(high * M / fs)
        for k in range(k_low, k_high + 1):
            H[k] = 0
            if k > 0:
                H[M - k] = 0
        
    h = np.real(np.fft.ifft(H))
    h = np.roll(h, M // 2)
    
    return h * np.hamming(M)

if __name__ == "__main__":
    h = design(FS, BANDS)
    print("Number of taps:", len(h))

    # Zero-pad the FFT so the response between the M design bins is visible
    n_fft = 8192
    H = np.abs(np.fft.fft(h, n_fft)[:n_fft // 2])
    f = np.arange(n_fft // 2) * FS / n_fft

    fig, ax = plt.subplots(figsize=(6.3, 2.5))
    ax.plot(f, 20 * np.log10(H + 1e-12), linewidth=0.8)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Gain (dB)")
    ax.set_xlim(0, FS / 2)
    ax.set_ylim(-80, 5)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    save_svg(fig, "fir_frequency_response")
    plt.show()
