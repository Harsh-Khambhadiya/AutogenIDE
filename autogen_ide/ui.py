"""Simple Streamlit-based UI for the Offline IDE."""

from __future__ import annotations

import streamlit as st
from .ide import OfflineIDE


st.set_page_config(layout="wide")

if "ide" not in st.session_state:
    st.session_state.ide = OfflineIDE(".")

ide: OfflineIDE = st.session_state.ide

left, center, right = st.columns([1, 2, 1])

with left:
    st.header("Project Files")
    files = ide.analyze()
    st.write("\n".join(files))

with center:
    st.header("Code Editor")
    path = st.text_input("File Path", "result.txt")
    content = st.text_area("Content", height=300)
    if st.button("Save"):
        ide.coder.apply_patch(path, content)

with right:
    st.header("Chat")
    prompt = st.text_input("Prompt", "")
    if st.button("Send") and prompt:
        response = ide.chat(prompt)
        st.write(response)
