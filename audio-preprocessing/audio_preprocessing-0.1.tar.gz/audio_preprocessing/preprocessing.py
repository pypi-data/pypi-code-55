#Mounting google drive
from google.colab import drive
drive.mount('/content/drive', force_remount=True)

#In case I want to load data into colab itself
#!cp -r '../content/drive/My Drive/FSDKaggle2018.audio_train/' /content

#Importing libraries
import numpy as np 
import pandas as pd

import librosa 
import librosa.display

import matplotlib
import matplotlib.pyplot as plt
import IPython.display as ipd
%matplotlib inline
matplotlib.style.use('ggplot')

from python_speech_features import mfcc, logfbank
from scipy.io import wavfile

import os
import shutil
import warnings
warnings.filterwarnings('ignore')

#Reading meta data file
train = pd.read_csv('../content/drive/My Drive/esc50.csv')

#train = train.drop(['esc10', 'src_file', 'take', 'fold'], axis =1)

#train = train[['filename', 'category', 'target']]

train.head()

print("Number of training examples=", train.shape[0], "  Number of classes=", 
      len(train['category'].unique()))

#train.category.value_counts()

import struct

class WavFileHelper():
    
    def read_file_properties(self, filename):

        wave_file = open(filename,"rb")
        
        riff = wave_file.read(12)
        fmt = wave_file.read(36)
        
        num_channels_string = fmt[10:12]
        num_channels = struct.unpack('<H', num_channels_string)[0]

        sample_rate_string = fmt[12:16]
        sample_rate = struct.unpack("<I",sample_rate_string)[0]
        
        bit_depth_string = fmt[22:24]
        bit_depth = struct.unpack("<H",bit_depth_string)[0]

        return (num_channels, sample_rate, bit_depth)

#from helpers.wavfilehelper import WavFileHelper
wavfilehelper = WavFileHelper()

audiodata = []
for index, row in train.iterrows():
    
    file_name = os.path.join(os.path.abspath('/content/drive/My Drive/audio/'+wav_file))
    data = wavfilehelper.read_file_properties(file_name)
    audiodata.append(data)

# Convert into a Panda dataframe
audiodf = pd.DataFrame(audiodata, columns=['num_channels','sample_rate','bit_depth'])

#num of channels 
print(audiodf.num_channels.value_counts(normalize=True))

#sample rates 
print(audiodf.sample_rate.value_counts(normalize=True))

#bit depth
print(audiodf.bit_depth.value_counts(normalize=True))

def plot_signals(signals):
    fig, axes = plt.subplots(nrows=3, ncols=5, sharex=False,
                             sharey=True, figsize=(20,5))
    fig.suptitle('Time Series', size=16)
    i = 0
    for x in range(3):
        for y in range(5):
            axes[x,y].set_title(list(signals.keys())[i])
            axes[x,y].plot(list(signals.values())[i])
            axes[x,y].get_xaxis().set_visible(False)
            axes[x,y].get_yaxis().set_visible(False)
            i += 1

def plot_fft(fft):
    fig, axes = plt.subplots(nrows=3, ncols=5, sharex=False,
                             sharey=True, figsize=(20,5))
    fig.suptitle('Fourier Transforms', size=16)
    i = 0
    for x in range(3):
        for y in range(5):
            data = list(fft.values())[i]
            Y, freq = data[0], data[1]
            axes[x,y].set_title(list(fft.keys())[i])
            axes[x,y].plot(freq, Y)
            axes[x,y].get_xaxis().set_visible(False)
            axes[x,y].get_yaxis().set_visible(False)
            i += 1

def plot_fbank(fbank):
    fig, axes = plt.subplots(nrows=3, ncols=5, sharex=False,
                             sharey=True, figsize=(20,5))
    fig.suptitle('Filter Bank Coefficients', size=16)
    i = 0
    for x in range(3):
        for y in range(5):
            axes[x,y].set_title(list(fbank.keys())[i])
            axes[x,y].imshow(list(fbank.values())[i],
                    cmap='hot', interpolation='nearest')
            axes[x,y].get_xaxis().set_visible(False)
            axes[x,y].get_yaxis().set_visible(False)
            i += 1

def plot_mfccs(mfccs):
    fig, axes = plt.subplots(nrows=2, ncols=5, sharex=False,
                             sharey=True, figsize=(20,5))
    fig.suptitle('Mel Frequency Cepstrum Coefficients', size=16)
    i = 0
    for x in range(2):
        for y in range(5):
            axes[x,y].set_title(list(mfccs.keys())[i])
            axes[x,y].imshow(list(mfccs.values())[i],
                    cmap='hot', interpolation='nearest')
            axes[x,y].get_xaxis().set_visible(False)
            axes[x,y].get_yaxis().set_visible(False)
            i += 1

classes = list(np.unique(train.category))

def calc_fft(y, rate):
  n = len(y)
  freq = np.fft.rfftfreq(n, d = 1/rate)
  Y = abs(np.fft.rfft(y)/n)
  return(Y, freq)

signals = {}
fft = {}
fbank = {}
mfccs = {}

for c in classes: 
  wav_file = train[train.category == c].iloc[0,0]
  signal, rate = librosa.load('/content/drive/My Drive/audio/' +wav_file, sr = 44100)
  
  signals[c] = signal
  fft[c] = calc_fft(signal, rate)
  

  bank = logfbank(signal[:rate], rate, nfilt=26, nfft=1103).T
  fbank[c] = bank
  #mel = mfcc(signal[:rate], rate, numcep = 13, nfilt = 26, nfft= 1103).T
  #mfccs[c] = mel

plot_signals(signals)
plt.show();

#plot_mfcc(mfccs)
#plt.show()

plot_fft(fft)
plt.show();

plot_fbank(fbank)
plt.show;

# Using IPython.display.Audio to play the audio files so we can inspect aurally
ipd.Audio('../content/drive/My Drive/audio/1-7057-A-12.wav')

filename = '/content/drive/My Drive/audio/1-137-A-32.wav'

#Sample rate conversion
librosa_audio, librosa_sample_rate = librosa.load(filename) 
scipy_sample_rate, scipy_audio = wav.read(filename) 

print('Original sample rate:', scipy_sample_rate) 
print('Librosa sample rate:', librosa_sample_rate)

#Bit depth conversion
print('Original audio file min~max range:', np.min(scipy_audio), 'to', np.max(scipy_audio))
print('Librosa audio file min~max range:', np.min(librosa_audio), 'to', np.max(librosa_audio))










