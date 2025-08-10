# modules/auto_clean.py
import streamlit as st
import pandas as pd
import numpy as np


def auto(df):
    st.subheader("🤖 Auto Cleaning in Progress...")

    try:

        # Step 1: Drop duplicates
        before = df.shape[0]
        df = df.drop_duplicates().reset_index(drop=True)
        st.success(f"✅ Removed {before - df.shape[0]} duplicate rows")

        # Step 2: Drop columns with >50% nulls
        null_percent = df.isnull().mean() * 100
        to_drop = null_percent[null_percent > 50].index.tolist()
        df.drop(columns=to_drop, inplace=True)
        if to_drop:
            st.success(f"✅ Dropped columns with >50% nulls: {', '.join(to_drop)}")
        else:
            st.info("✨ No columns with >50% nulls")

        # Step 3: Fill numeric nulls with median
        num_cols = df.select_dtypes(include='number').columns
        for col in num_cols:
            if df[col].isnull().sum() > 0:
                med = df[col].median()
                df[col].fillna(med, inplace=True)
                st.success(f"✅ Filled nulls in '{col}' with median ({med})")

        # Step 4: Fill categorical nulls with mode
        cat_cols = df.select_dtypes(include='object').columns
        for col in cat_cols:
            if df[col].isnull().sum() > 0:
                mode = df[col].mode().iloc[0]
                df[col].fillna(mode, inplace=True)
                st.success(f"✅ Filled nulls in '{col}' with mode ('{mode}')")

        # Final update
        st.session_state.df = df
        st.success("🎉 Auto cleaning complete!")

    except Exception as e:
        st.error(f"❌ Auto cleaning failed: {e}")
