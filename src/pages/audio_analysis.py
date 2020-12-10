from enum import Enum
from io import BytesIO, StringIO
from typing import Union

import streamlit as st
from scipy.io.wavfile import read, write
from src.utils import Page
from src.utils.files import file_selector

import soundfile as sf

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
    
    def _read_wav(self, file: BytesIO):
        rate = None
        data = None
        file_type = get_file_type(file)
        if file_type == FileType.WAV:
            try:
                rate, data = read(file)
                file.close()
            except:
                pass
        else:
            st.error("Invalid extention, please upload a wav file!")
        return rate, data

    def write(self):
        st.title("Audio Analysis")

        files = st.file_uploader("Upload file", type=FILE_TYPES, accept_multiple_files=True)
        show_file = st.empty()
        if not files:
            show_file.info("Please upload a file of type: " + ", ".join(FILE_TYPES))
            return
        
        if not isinstance(files, list):
            files = [files]
        try:
            for file in files:
                rate, date = self._read_wav(file)
                st.write(f"File: {file.name}")
                st.write(f"Rate: {rate}")
                st.write(f"------")
        except Exception:
            for file in files:
                file.close()

        st.title("Lofar Analysis")

        # self.state.client_config["audio_filename"] = filename
