import streamlit as st
import pandas as pd
from .undo_reset import save_snapshot

# ====== Type Converter ======
def type_convertor(df):
    st.subheader("🔄 Type Converter")

    cols = df.columns.tolist()
    selected = st.selectbox("Select column to convert", cols)
    curr_type = df[selected].dtype
    st.write(f"Current dtype: **{curr_type}**")

    new_type = st.selectbox("Convert to type", ["int", "float", "str", "datetime"])

    if st.button("Preview Conversion"):
        try:
            if new_type == "int":
                converted = pd.to_numeric(df[selected], errors='coerce').astype("Int64")
            elif new_type == "float":
                converted = pd.to_numeric(df[selected], errors='coerce').astype(float)
            elif new_type == "str":
                converted = df[selected].astype(str)
            elif new_type == "datetime":
                converted = pd.to_datetime(df[selected], errors='coerce')

            nulls = converted.isna().sum()
            total = len(converted)
            pct = round((nulls / total) * 100, 2)

            if pct > 0:
                st.warning(f"{nulls} values ({pct}%) will become NaN.")
                failed_rows = df[converted.isna()]
                if not failed_rows.empty:
                    st.write(f"❌ {failed_rows.shape[0]} rows failed to convert:")
                    st.dataframe(failed_rows)
            else:
                st.success("✅ Safe conversion. No nulls introduced.")

            st.session_state.converted_col = converted
            st.session_state.converted_col_name = selected
            st.session_state.new_dtype = new_type

        except Exception as e:
            st.error(f"⚠️ Conversion error: {e}")

    if st.button("Apply Conversion"):
        if (
            "converted_col" in st.session_state and 
            st.session_state.get("converted_col_name") == selected
        ):
            save_snapshot(df)
            df[selected] = st.session_state.converted_col
            st.session_state.df = df
            st.success(f"✅ Column '{selected}' converted to {st.session_state.new_dtype}.")
        else:
            st.warning("⚠️ Please preview before applying.")