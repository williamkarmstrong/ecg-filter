import numpy as np

class FIRfilter: 
    def __init__(self, _coefficients): 
        self.coefficients = np.array(_coefficients)
        self.N = len(self.coefficients)
        self.buffer = np.zeros(self.N)
        self.index = 0

    def doFilter(self,v):
        """Realtime ECG filtering"""
        self.buffer[self.index] = v
        
        indices = (self.index - np.arange(self.N)) % self.N
        filtered_value = np.dot(self.coefficients, self.buffer[indices])
        
        self.index = (self.index + 1) % self.N
        return filtered_value

    def doFilterAdaptive(self, signal, noise, learningRate):
        """Adaptive LMS filter rather than bandstop filters"""
        return
