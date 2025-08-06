import pandas as pd
import numpy as np
import streamlit as st

def load_data(file):
    if "file_name" not in st.session_state or st.session_state.file_name != file.name:
        try:
            df = pd.read_csv(file)
            df = df.replace(['-', 'n/a', 'N/A', 'missing'], np.nan)
            st.session_state.df = df
            st.session_state.raw_data = df.copy()
            st.session_state.file_name = file.name
        except Exception as e:
            st.error(f"❌ Failed to load file: {e}")
    return st.session_state.df, st.session_state.raw_data
