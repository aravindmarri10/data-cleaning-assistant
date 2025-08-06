import streamlit as st
from .undo_reset import save_snapshot

def remove_duplicates(df):
    st.subheader("🧭 Duplicate Detection")
    dup = df.duplicated().sum()
    if dup > 0:
        st.warning(f"🚨 Found {dup} duplicate rows.")
        if st.button("🗑️ Drop Duplicates"):
            save_snapshot(df)
            df = df.drop_duplicates(ignore_index=True)
            st.session_state.df = df
            st.success("✅ Duplicate rows removed.")
    else:
        st.info("✨ No duplicates found.")

def drop_columns(df):
    st.subheader("🧹 Drop Columns")
    cols = st.multiselect("Select columns to drop", df.columns.tolist())
    if not cols:
        st.warning("⚠️ No columns selected.")
    else:
        if st.button("🚫 Apply Drop"):
            save_snapshot(df)
            df = df.drop(columns=cols)
            st.session_state.df = df
            st.success(f"✅ Dropped: {', '.join(cols)}")