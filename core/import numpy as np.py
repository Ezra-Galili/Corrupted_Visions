import numpy as np

def window_curve(feature, feature_times, start, end, n_samples):
    sample_times = np.linspace(start, end, n_samples) # picks n_samples evenly spaced between start and end
    return np.interp(sample_times, feature_times, feature) # reads the feature curve at the moments and interpolates between points

