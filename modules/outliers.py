import streamlit as st
import pandas as pd
import numpy as np
from .utils import get_iqr_bounds
from .undo_reset import save_snapshot

def outlier_detection(df):
    st.subheader("🚨 Outlier Handler")
    mode = st.sidebar.radio("Outlier Mode", ['Show Outliers', 'Drop Outliers', 'Cap Outliers'],  key = "outlier_mode")

    num_cols = df.select_dtypes(include='number').columns
    summary = []

    for col in num_cols:
        low, high = get_iqr_bounds(df[col])
        count = df[(df[col] < low) | (df[col] > high)].shape[0]
        summary.append({'Column': col, 'Outlier Count': count})

    outlier_df = pd.DataFrame(summary)

    if mode == 'Show Outliers':
        if outlier_df['Outlier Count'].sum() == 0:
            st.info("🎉 No outliers found.")
        else:
            st.dataframe(outlier_df)

    elif mode == 'Drop Outliers':
        if outlier_df['Outlier Count'].sum() == 0:
            st.info("✅ No outliers to drop.")
        else:
            st.warning("⚠️ Dropping outliers may reduce data size significantly and somtimes form new outliers.")
            cols = st.multiselect("Select columns", outlier_df[outlier_df['Outlier Count'] > 0]['Column'])
            if cols:
                temp = df.copy()
                before = temp.shape[0]
                for col in cols:
                    low, high = get_iqr_bounds(df[col])
                    temp = temp[(temp[col] >= low) & (temp[col] <= high)]
                after = temp.shape[0]
                dropped = before - after
                pct = round((dropped / before) * 100, 2)
                st.info(f"Rows dropped: {dropped} ({pct}%)")
                if st.checkbox("🔍 Preview dropped rows"):
                    st.dataframe(df[~df.index.isin(temp.index)])
                if st.button("Confirm Drop"):
                    save_snapshot(df)
                    st.session_state.df = temp
                    st.success("✅ Outliers removed.")

    elif mode == 'Cap Outliers':
        if outlier_df['Outlier Count'].sum() == 0:
            st.info("✅ No outliers to cap.")
        else:
            cols = st.multiselect("Select columns", outlier_df[outlier_df['Outlier Count'] > 0]['Column'])
            if cols:
                temp = df.copy()
                for col in cols:
                    low, high = get_iqr_bounds(df[col])
                    temp[col] = np.where(temp[col] < low, low, temp[col])
                    temp[col] = np.where(temp[col] > high, high, temp[col])
                if st.checkbox("🔍 Show capped rows"):
                    diff = df[cols] != temp[cols]
                    affected = df[diff.any(axis=1)]
                    st.write(f"{affected.shape[0]} rows capped.")
                    st.dataframe(affected)
                if st.button("Confirm Capping"):
                    save_snapshot(df)
                    st.session_state.df = temp
                    st.success("✅ Outliers capped.")