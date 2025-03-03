import os
import pickle
from collections import defaultdict
from audio.audio_processing import create_spectogram
from audio.fingerprinting import find_peaks, generate_fingerprints


class FingerprintDatabase:
    def __init__(self):
        """Initialize the fingerprint database"""
        # Store fingerprints as {hash_value: [(song_id, time_offset), ...]}
        self.fingerprints = defaultdict(list)
        self.songs = {}
        self.next_id = 0

    def add_song(self, song_path):
        """
        Add a song to the database

        Args:
            song_path (str): Path to the song file

        Returns:
            int: ID of the added song
        """
        # Generate a song ID
        song_id = self.next_id
        self.next_id += 1

        # Store song info
        song_name = os.path.basename(song_path)
        self.songs[song_id] = song_name

        # Create spectrogram
        spectrogram, sr = create_spectogram(song_path)

        # Find peaks
        peaks = find_peaks(spectrogram)

        # Generate fingerprints
        fingerprints = generate_fingerprints(peaks)

        # Add fingerprints to database
        for hash_value, time_offset in fingerprints:
            self.fingerprints[hash_value].append((song_id, time_offset))

        print(f"Added song {song_name} with {len(fingerprints)} fingerprints")
        return song_id

    def save(self, filename):
        """
        Save the database to a file

        Args:
            filename (str): Path to save the database
        """
        with open(filename, 'wb') as f:
            pickle.dump((self.fingerprints, self.songs, self.next_id), f)

    def load(self, filename):
        """
        Load the database from a file

        Args:
            filename (str): Path to the database file
        """
        with open(filename, 'rb') as f:
            self.fingerprints, self.songs, self.next_id = pickle.load(f)