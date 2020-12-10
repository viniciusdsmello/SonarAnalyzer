import logging
from enum import Enum
from io import BytesIO, StringIO
from typing import Union

import soundfile as sf
import streamlit as st
from scipy.io.wavfile import read, write

from src.utils import Page
from src.utils.files import file_selector

from src.preprocessing import LofarAnalysis

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

    def _run_lofar_analysis(self, **kwargs):
        lofar = LofarAnalysis()
        
    def _run_demon_analysis(self, **kwargs):
        demon = DemonAnalysis()

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
                            "rate": rate,
                            "data": data
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
                               
                self.classes.update(
                    {
                        f"class_{class_label}": {
                            "index": i,
                            "files": class_files
                        }
                    }
                )

        self.write_sidebar()

    def write_sidebar(self):
        st.sidebar.write("Options:")
        if st.sidebar.button('Lofar Analysis'):
            st.sidebar.write("Lofar Settings:")
            self.state.client_config["lofar_decimation_rate"] = st.sidebar.slider(
                label="Decimation Rate",
                min_value=0,
                value=self.state.client_config.get("lofar_decimation_rate", 3)
            )
            self.state.client_config["lofar_fft_points"] = st.sidebar.slider(
                label="FFT Points",
                min_value=1,
                value=self.state.client_config.get("lofar_fft_points", 400)
            )
            for c in self.classes:
                st.title(f"Lofar Analysis - {c}")
                for filename in self.classes[c].get('files'):
                    st.write(f"File: {filename}")
                    st.write(f"Decimation Rate: {decimation_rate}")
                    st.write(f"FFT Points: {fft_points}")
                    file_data = self.files_data[filename]
                    logging.info("Running Lofar Analysis...")

        if st.sidebar.button('Demon Analysis'):
            for c in classes:
                st.title(f"Demon Analysis - {c}")
                for filename in classes[c].get('files'): 
                    st.write(f"File: {filename}")
                    st.write(f"Decimation Rate: {decimation_rate}")
                    st.write(f"FFT Points: {fft_points}")
                    file_data = self.files_data[filename]                
                    logging.info("Running Lofar Analysis...")