import streamlit as st
from .undo_reset import save_snapshot

def santize():
    st.subheader("Data Sanity")
    df = st.session_state.df  
    col = st.selectbox("Select a column", df.columns.tolist())
    if not col:
        st.warning("⚠️ No column selected.")
    else:
        if st.checkbox("Preview unique values"):
            st.dataframe(df[col].unique())

        char = st.text_input("Enter a character/text to remove:")

        if st.button("🚫 Apply Cleaning"):
            if not char.strip():
                st.warning("⚠️ Enter something to remove.")
                return

            save_snapshot(df)

            df[col] = df[col].str.replace(char, "", regex=False)

            st.session_state.df = df
            st.success(f"Removed '{char}' successfully!")


