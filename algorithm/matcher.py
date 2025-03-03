import numpy as np
from collections import defaultdict
from audio.audio_processing import create_spectogram
from audio.fingerprinting import find_peaks, generate_fingerprints


def identify_song(sample_path, database, plot=False):
    # Create spectrogram for sample
    spectrogram, sr = create_spectogram(sample_path, plot)

    # Find peaks in the sample
    peaks = find_peaks(spectrogram)

    # Generate fingerprints
    sample_fingerprints = generate_fingerprints(peaks)

    # Count matches for each song
    matches = defaultdict(list)

    for hash_value, sample_time in sample_fingerprints:
        # Look up the hash in the database
        if hash_value in database.fingerprints:
            # Get all songs that have this fingerprint
            for song_id, song_time in database.fingerprints[hash_value]:
                # Calculate time offset
                time_delta = sample_time - song_time

                # Add to matches
                matches[song_id].append(time_delta)

    # Find the song with the most matches
    best_match = None
    best_count = 0

    for song_id, time_deltas in matches.items():
        # Histogram of time deltas should show a spike at the correct offset
        hist = np.histogram(time_deltas, bins=100)
        count = np.max(hist[0])

        if count > best_count:
            best_count = count
            best_match = song_id

    # Return the result
    if best_match is not None and best_count > 5:  # Minimum threshold
        return database.songs[best_match], best_count
    else:
        return "No match found", 0