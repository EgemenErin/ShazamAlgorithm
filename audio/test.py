import matplotlib.pyplot as plt
from audio_processing import create_spectogram
import sys


def test_audio_processing():
    if len(sys.argv) < 2:
        print("Usage: python test_audio_processing.py <path_to_audio_file>")
        return

    audio_file = sys.argv[1]
    print(f"Processing audio file: {audio_file}")

    try:
        spectrogram, sr = create_spectogram(audio_file, plot=True)
        print(f"Sample rate: {sr} Hz")
        print(f"Spectrogram shape: {spectrogram.shape}")
        print("Spectrogram generated successfully!")
        plt.show()

    except Exception as e:
        print(f"Error processing audio file: {e}")


test_audio_processing()