import pandas as pd
import numpy as np
import streamlit as st

def load_data(file):
    try:
        if isinstance(file, str):  # Local sample path
            df = pd.read_csv(file)
            st.session_state.file_name = file
        else:
            if "file_name" not in st.session_state or st.session_state.file_name != file.name:
                df = pd.read_csv(file)
                st.session_state.file_name = file.name
            else:
                df = st.session_state.df.copy()

        df = df.replace(['-', 'n/a', 'N/A', 'missing'], np.nan)
        st.session_state.df = df
        st.session_state.raw_data = df.copy()

    except Exception as e:
        st.error(f"❌ Failed to load file: {e}")
        raise e

    return st.session_state.df, st.session_state.raw_data
