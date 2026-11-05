import numpy as np

class FIRfilter: 
    def __init__(self, _coefficients): 
        self.coefficients = np.array(_coefficients)
        self.N = len(_coefficients)
        self.buffer = np.zeros(self.N)
        self.index = 0
        
        #LMS filter parameters
        self.w = np.zeros(self.N)
        self.lms_buffer = np.zeros(self.N)
        self.lms_index = 0

    def doFilter(self,v):
        """Realtime ECG filtering"""
        self.buffer[self.index] = v

        # Array of indices showing order of most recently accessed sample
        indices = (self.index - np.arange(self.N)) % self.N

        # Apply reordering to match co-effs with sample, dot to multiply then sum
        filtered_value = np.dot(self.coefficients, self.buffer[indices])
        
        self.index = (self.index + 1) % self.N
        return filtered_value

    def doFilterAdaptive(self, signal, noise, learningRate):
        """Adaptive LMS filter rather than bandstop filters"""
        
        self.lms_buffer[self.lms_index] = noise
        indices = (self.lms_index - np.arange(self.N)) % self.N
        xvector = self.lms_buffer[indices]
        
        y = np.dot(self.w, xvector)
        e = signal - y
        self.w += 2 *learningRate * e * xvector
        
        self.lms_index = (self.lms_index + 1) % self.N  
        
        return e
