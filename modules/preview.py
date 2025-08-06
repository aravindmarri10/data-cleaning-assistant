import streamlit as st
import io

def preview_data(df):
    st.subheader("👀 Dataset Preview")
    st.markdown(f"- **Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("📊 Column Types & Info")
    buf = io.StringIO()
    df.info(buf=buf)
    st.code(buf.getvalue(), language='text')

    st.subheader("📈 Descriptive Statistics")
    st.dataframe(df.describe(include='all').T, use_container_width=True)
