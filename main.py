import streamlit as st

from src.utils import Page, provide_state, get_file_content_as_string
from src.pages import Page1, Page2, AudioAnalysis, Default

from typing import Dict, Type


PAGE_MAP: Dict[str, Type[Page]] = {
    "Audio Analysis": AudioAnalysis,
    "Page 1": Page1,
    "Page 2": Page2
}

@provide_state()
def main(state=None):
    st.set_page_config(page_title="Sonar Analyzer", layout="centered")
    readme_text = st.markdown(get_file_content_as_string("docs/instructions.md"))

    st.sidebar.header("Sonar Analyzer")
    current_page = st.sidebar.selectbox("Menu",
        ["Home"] + list(PAGE_MAP))
    
    if current_page == "Home":
        st.sidebar.success('To continue select an option aboce.')
    else:
        readme_text.empty()
        PAGE_MAP.get(current_page, Default)(state=state).write()

if __name__ == "__main__":
    main()