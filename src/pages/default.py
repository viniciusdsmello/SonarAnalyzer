import streamlit as st
from src.utils import Page, get_file_content_as_string


class Default(Page):
    def __init__(self, state):
        self.state = state

    def write(self):
        st.title("Ops! Page not Foud!")

        st.markdown(get_file_content_as_string('docs/instructions.md'))
