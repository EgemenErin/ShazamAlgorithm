import numpy as np
from scipy.ndimage import maximum_filter
from scipy.ndimage import generate_binary_structure, iterate_structure

def find_peaks(spectogram, neighborhood_size=10, treshold=0.5):
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, neighborhood_size)

    local_max = maximum_filter(spectogram, footprint=neighborhood) == spectogram
    background = (spectogram < treshold)
    peaks = local_max & ~background
    peak_coords = np.where(peaks)

    return list(zip(peak_coords[0], peak_coords[1]))

def generate_fingerprints(peaks, fan_value=15, min_time_delta=0, max_time_delta=200):
    fingerprints = []
    peaks.sort(key=lambda x: x[1])

    for i in range(len(peaks)):
        for j in range(1, min(fan_value, len(peaks) - i)):
            freq1, time1 = peaks[i]
            freq2, time2 = peaks[i + j]
            time_delta = time2 - time1

            if min_time_delta <= time_delta <= max_time_delta:
                hash_str = f"{freq1}|{freq2}|{time_delta}"
                hash_value = hash(hash_str)
                fingerprints.append((hash_value, time1))
    return fingerprints