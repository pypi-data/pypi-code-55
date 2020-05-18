from IPython.display import Audio, Latex

def audio_play(s, fs, txt="", autoplay=False):
    if txt:
      display(Latex(txt))
    display(Audio(s, rate=fs, autoplay=autoplay))