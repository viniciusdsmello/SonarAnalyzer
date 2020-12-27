import logging
from enum import Enum
from io import BytesIO, StringIO
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from scipy.io.wavfile import read
from src.preprocessing.signal import LofarAnalysis, DemonAnalysis
from src.utils import Page

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

FILE_TYPES = ["wav"]


class FileType(Enum):
    """Used to distinguish between file types"""
    WAV = "Wav"


def get_file_type(file: Union[BytesIO, StringIO]) -> FileType:
    """The file uploader widget does not provide information on the type of file uploaded so we have
    to guess using rules or ML. See
    [Issue 896](https://github.com/streamlit/streamlit/issues/896)

    I've implemented rules for now :-)

    Arguments:
        file {Union[BytesIO, StringIO]} -- The file uploaded

    Returns:
        FileType -- A best guess of the file type
    """

    if isinstance(file, BytesIO):
        return FileType.WAV


class AudioAnalysis(Page):
    def __init__(self, state):
        self.state = state
        self.files_data = {}
        self.classes = {}
        self.number_of_classes = None

    def _read_wav(self, file: BytesIO):
        rate = None
        data = None
        file_type = get_file_type(file)
        if file_type == FileType.WAV:
            try:
                rate, data = read(file)
            except Exception as e:
                logging.error(f"Error while reading wav file - {str(e)}")
        else:
            st.error("Invalid extention, please upload a wav file!")
        return rate, data

    def _run_lofar_analysis(self, data: np.ndarray, fs: int, n_pts_fft: int, n_overlap: int, spectrum_bins_left: int,
                            plot_title: str):
        logging.info("Running Lofar Analysis...")

        lofar = LofarAnalysis()

        power, freq, time = lofar.transform(data, fs, n_pts_fft, n_overlap, spectrum_bins_left)

        plt.rcParams['font.weight'] = 'bold'
        plt.rcParams['font.size'] = 14
        plt.rcParams['xtick.labelsize'] = 15
        plt.rcParams['ytick.labelsize'] = 15

        fig, ax = plt.subplots(figsize=(10, 10))
        plt.imshow(power,
                   cmap="jet",
                   extent=[1, spectrum_bins_left, time.max(), 1],
                   aspect="auto")

        cbar = plt.colorbar()
        cbar.ax.set_ylabel('dB', fontweight='bold')

        if plot_title is None:
            plot_title = 'Lofargram'

        plt.title(plot_title, fontweight='bold')
        plt.xlabel('Frequency bins', fontweight='bold')
        plt.ylabel('Time (seconds)', fontweight='bold')

        st.pyplot(fig=fig)

    def _run_demon_analysis(self, **kwargs):
        DemonAnalysis()

    def write(self):
        st.title("Audio Analysis")
        st.markdown("""
        Please, select the .wav files above, then in the sidebar select the analysis that should be performed.
        """)
        files = st.file_uploader("Upload file", type=FILE_TYPES, accept_multiple_files=True)
        show_file = st.empty()
        if not files:
            show_file.info("Please upload a file of type: " + ", ".join(FILE_TYPES))
            return

        if not isinstance(files, list):
            files = [files]
        try:
            for file in files:
                rate, data = self._read_wav(file)
                self.files_data.update(
                    {
                        file.name: {
                            "sample_rate": rate,
                            "signal": data
                        }
                    }
                )
        except Exception as e:
            logging.error(f"Error while reading processing files - {str(e)}")

        self.number_of_classes = st.number_input("How many classes?", format='%d', value=0, step=1)

        self.classes = {}
        if self.number_of_classes:
            for i in range(self.number_of_classes):
                class_label = st.text_input(label=f"Insert a Label for the #{i+1} class", key=f"class_label_{i}")
                class_files = st.multiselect(label="Select files to add to this class",
                                             options=[file.name for file in files],
                                             key=f"class_files_{i}")

                class_dict = {}

                for class_file in class_files:
                    class_dict.update(
                        {
                            class_file: {
                                "sample_rate": self.files_data[class_file]["sample_rate"],
                                "signal": self.files_data[class_file]["signal"]
                            }
                        }
                    )

                self.classes.update({f"class_{class_label}": class_dict})

        self.write_sidebar()

    def write_sidebar(self):
        button = st.sidebar.selectbox(label='Options:',
                                      options=[
                                          'Choose one Analysis...',
                                          'Lofar Analysis',
                                          'Demon Analysis'
                                      ]
                                      )

        if button == "Lofar Analysis":
            self._lofar_analysis()
        if button == "Demon Analysis":
            self._demon_analysis()

    def _lofar_analysis(self):
        st.sidebar.write("Lofar Settings:")
        self.state.client_config["lofar_decimation_rate"] = st.sidebar.number_input(
            label="Decimation Rate",
            min_value=0,
            max_value=10,
            value=self.state.client_config.get("lofar_decimation_rate", 3)
        )
        self.state.client_config["lofar_fft_points"] = st.sidebar.number_input(
            label="FFT Points",
            min_value=1,
            max_value=4000,
            value=self.state.client_config.get("lofar_fft_points", 1024)
        )
        self.state.client_config["lofar_spectrum_bins_left"] = st.sidebar.number_input(
            label="Spectrum Bins Left",
            min_value=1,
            max_value=4000,
            value=self.state.client_config.get("lofar_spectrum_bins_left", 400)
        )
        self.state.client_config["lofar_n_overlap"] = st.sidebar.number_input(
            label="Overlap",
            min_value=0,
            max_value=4000,
            value=self.state.client_config.get("lofar_n_overlap", 0)
        )
        for class_label in self.classes:
            st.title(f"Lofar Analysis - {class_label}")
            for filename in self.classes[class_label]:
                file_data = self.classes[class_label][filename]
                st.write(f"File: {filename}")
                st.write(f"Decimation Rate: {self.state.client_config['lofar_decimation_rate']}")
                st.write(f"FFT Points: {self.state.client_config['lofar_fft_points']}")
                st.write(f"Spectrum Bins Left: {self.state.client_config['lofar_spectrum_bins_left']}")
                st.write(f"Signal Overlap: {self.state.client_config['lofar_n_overlap']}")

                sample_rate = file_data["sample_rate"]
                signal = file_data["signal"]

                self._run_lofar_analysis(data=signal,
                                         fs=sample_rate,
                                         n_pts_fft=self.state.client_config['lofar_fft_points'],
                                         n_overlap=self.state.client_config['lofar_n_overlap'],
                                         spectrum_bins_left=self.state.client_config['lofar_spectrum_bins_left'],
                                         plot_title=f"Lofargram {filename} - {class_label}"
                                         )

    def _demon_analysis(self):
        st.sidebar.write("Demon Settings:")
        for c in self.classes:
            st.title(f"Demon Analysis - {c}")
            for filename in self.classes[c].get('files'):
                st.write(f"File: {filename}")
                # file_data = self.files_data[filename]
                logging.info("Running Lofar Analysis...")
