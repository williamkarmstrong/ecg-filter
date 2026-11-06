import numpy as np

class FIRfilter: 
    def __init__(self, _coefficients): 
        self.coefficients = np.array(_coefficients)
        self.N = len(_coefficients)
        self.buffer = np.zeros(self.N)
        self.index = 0
        
    def dofilter(self,v):
        """Realtime ECG filtering"""
        self.buffer[self.index] = v

        # Array of indices showing order of most recently accessed sample
        indices = (self.index - np.arange(self.N)) % self.N

        # Apply reordering to match co-effs with sample, dot to multiply then sum
        filtered_value = np.dot(self.coefficients, self.buffer[indices])
        
        self.index = (self.index + 1) % self.N
        return filtered_value

    def doFilterAdaptive(self, signal, noise, learning_rate):
        """Adaptive LMS filter rather than bandstop filters"""

        # Run LMS Filter on the noise
        canceller = self.dofilter(noise)

        # Re-order buffer based on the previous index
        indices = (self.index - 1 - np.arange(self.N)) % self.N
        xvector = self.buffer[indices]

        # Calculate error signal and update co-efficients
        e = signal - canceller
        self.coefficients += learning_rate * e * xvector
        
        return e
