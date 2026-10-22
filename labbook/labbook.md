# Lab Book: ECG FIR Filtering

## 1. Spectrum Analysis

**Recording**
- ECG is in column 8 of the `.tsv`.
- fs = 250 Hz, so the Nyquist frequency is 125 Hz.

**Signal**
- The ECG itself sits roughly between 0.5 and 40 Hz.

**Noise identified**
- **Baseline wander:** below about 0.5 Hz.
- **50 Hz mains:** very strong, about 200× the median spectral level.
- **100 Hz harmonic:** weak, about 3× the median, but still worth mentioning.
- **Aliasing:** the 150 Hz harmonic aliases to 100 Hz, and 200 Hz aliases to 50 Hz.

**Bands to remove**
- 0 – 0.5 Hz => baseline wander, below the ECG range
- 45 – 55 Hz => 50 Hz mains (plus the 200 Hz alias)
- 95 – 105 Hz => 100 Hz harmonic (plus the 150 Hz alias)

## 2. Coefficient Design Function
Number of co-efficients (taps) is based on the smallest band to remove.

Smallest band is 0.5Hz, therefore if M is the no. of co-efficients

M = Fs / 0.5Hz = 250Hz / 0.5Hz = 500

The filter will delay the sample by (M-1) / 2, so let **M = 501**

We can add a hamming window too to smooth the edges from the filtering.

## 3. Realtime FIR Class

## 4. Adaptive LMS

## 5. Matched Filter and Heart Rate
