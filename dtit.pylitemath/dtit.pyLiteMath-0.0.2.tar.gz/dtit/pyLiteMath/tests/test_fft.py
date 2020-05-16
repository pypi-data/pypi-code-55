import dtit.pyLiteMath as lmath
import numpy as np

def signal_xHz(A, fi, time_s, sample):
    return A * np.sin(np.linspace(0, fi * time_s * 2 * np.pi, sample * time_s))

    
print("-------------------------------")
print("Testing Fixed Point FFT 1024")
samples = signal_xHz(12288, 0.1, 100, 16000)
fr = samples.astype(np.int16)
fi = fr
result = lmath.pyFFT1024(fr, fi)
print("pyFFT1024 returned {:d}".format(result))
print(samples[0:50])
print(fr[0:50])
print("-------------------------------")