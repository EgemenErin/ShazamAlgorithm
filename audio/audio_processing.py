import numpy as np
import librosa
import matplotlib.pyplot as plt

def create_spectogram(audio_file, plot=False):
    y, sr = librosa.load(audio_file)
    S = np.abs(librosa.stft(y))
    log_S = librosa.amplitude_to_db(S, ref=np.max)

    if plot:
        plt.figure(figsize=(12, 8))
        librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='log')
        plt.title('Spectogram')
        plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()
        plt.show()
    return log_S, sr