import numpy as np

BANDS = [
    (0, 0.5),
    (45, 55),
    (95, 105)
]

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
        k_low, k_high = round(low * M / fs), round(high * M / fs)
        H[k_low:k_high + 1] = 0
        H[M - k_high:M - k_low + 1] = 0
        
    h = np.real(np.fft.ifft(H))
    h = np.roll(h, M // 2)
    
    return h * np.hamming(M)

if __name__ == "__main__":
    pass