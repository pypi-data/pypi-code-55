from rohan.global_imports import *
from rohan.dandage.io_dict import read_dict,to_dict

def get_audio_duration(filename):
    import subprocess
    args=("ffprobe","-show_entries", "format=duration","-i",filename)
    popen = subprocess.Popen(args, stdout = subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    return float(str(output).split('=')[1].split('\\n')[0])*1000

def get_spectrogram(audio_path,plot_mel_power_spectrogram=False):
    """https://github.com/librosa"""
    import librosa
    y, sr = librosa.load(audio_path)

    #Mel spectrogram
    #This first step will show how to compute a Mel spectrogram from an audio waveform.
    # Let's make and display a mel-scaled power (energy-squared) spectrogram
    # S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)

    # Convert to log scale (dB). We'll use the peak power (max) as reference.
    # log_S = librosa.power_to_db(S, ref=np.max)

    if plot_mel_power_spectrogram:
        # Make a new figure
        plt.figure(figsize=(12,4))
        # Display the spectrogram on a mel scale
        # sample rate and hop length parameters are used to render the time axis
        librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
        # Put a descriptive title on the plot
        plt.title('mel power spectrogram')
        # draw a color bar
        plt.colorbar(format='%+02.0f dB')
        # Make the figure layout compact
        plt.tight_layout()

    #Harmonic-percussive source separation
    #Before doing any signal analysis, let's pull apart the harmonic and percussive components of the audio. This is pretty easy to do with the effects module.
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    # What do the spectrograms look like?
    # Let's make and display a mel-scaled power (energy-squared) spectrogram
    # S_harmonic   = librosa.feature.melspectrogram(y_harmonic, sr=sr)
    S_percussive = librosa.feature.melspectrogram(y_percussive, sr=sr)

    # Convert to log scale (dB). We'll use the peak power as reference.
    # log_Sh = librosa.power_to_db(S_harmonic, ref=np.max)
    log_Sp = librosa.power_to_db(S_percussive, ref=np.max)
    if plot_mel_power_spectrogram:
        # Make a new figure
        plt.figure(figsize=(16,4))
        plt.subplot(2,1,1)
        # Display the spectrogram on a mel scale
        librosa.display.specshow(log_Sh, sr=sr, y_axis='mel')
        # Put a descriptive title on the plot
        plt.title('mel power spectrogram (Harmonic)')
        # draw a color bar
        plt.colorbar(format='%+02.0f dB')
        plt.subplot(2,1,2)
        librosa.display.specshow(log_Sp, sr=sr, x_axis='time', y_axis='mel')
        # Put a descriptive title on the plot
        plt.title('mel power spectrogram (Percussive)')
        # draw a color bar
        plt.colorbar(format='%+02.0f dB')
        # Make the figure layout compact
        plt.tight_layout()
    df1=pd.DataFrame(log_Sp,
                    columns=np.linspace(0,get_audio_duration(audio_path),log_Sp.shape[1]))
    df2=dmap2lin(df1,coln='time (ms)',colvalue_name='db (log-scale)',idxn='frequency')
    return df2

def get01_date2dspectrogramp(cfg,date2dspectrogramp):
    dn2dp=cfg['date2pathm4ap']
    dn2outp={}
    for k in dn2dp:
        dn2outp[k]=f"{dirname(date2dspectrogramp)}/{k}.pqt"
        if not exists(dn2outp[k]):
            df=get_spectrogram(dn2dp[k])
            to_table(df,dn2outp[k])
    to_dict(dn2outp,date2dspectrogramp)