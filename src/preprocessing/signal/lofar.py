
import streamlit as st
import numpy as np
from poseidon.signal.lofar import lofar


class LofarAnalysis:
    def __init__(self):
        pass

    @st.cache
    def transform(
            self, data: np.ndarray, fs: int, n_pts_fft: int, n_overlap: int, spectrum_bins_left: int) -> (
            np.ndarray, np.ndarray, np.ndarray):
        power, freq, time = lofar(data, fs, n_pts_fft, n_overlap, spectrum_bins_left)

        # TODO: Convert to float
        power = power.astype(np.float32)
        freq = freq.astype(np.float32)
        time = time.astype(np.float32)

        return power, freq, time

    def plot_lofargram(self, power, freq, time, ax=None, figsize=(10, 10), savepath=None):
        raise NotImplementedError
