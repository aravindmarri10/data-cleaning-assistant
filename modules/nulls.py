import streamlit as st
from .utils import get_null_summary, numeric_fill_ui, apply_numeric_fill, cat_fill_ui, apply_cat_fill
from .undo_reset import save_snapshot

def null_handling():
    st.subheader("🔍 Null Value Handler")
    df = st.session_state.df  # ✅ always start here

    sub = st.sidebar.radio("Select Null Handling Method", 
        ['Null Summary', 'Drop Rows with Nulls', 'Drop Columns with Nulls',
         'Fill Numeric Nulls', 'Fill Categorical Nulls'], key="null_handling_method")

    null_per = get_null_summary(df)

    if sub == 'Null Summary':
        if null_per.empty:
            st.success("🎉 No missing values!")
        else:
            st.dataframe(null_per)

    elif sub == 'Drop Rows with Nulls':
        dropped_df = df.dropna()
        loss = df.shape[0] - dropped_df.shape[0]
        percent_loss = round((loss / df.shape[0]) * 100, 2)
        st.warning(f"⚠️ {loss} rows ({percent_loss}%) will be removed.")
        if st.checkbox("Preview rows to be dropped"):
            st.dataframe(df[~df.index.isin(dropped_df.index)])
        if st.button("🧹 Drop Null Rows"):
            save_snapshot(df)
            st.session_state.df = dropped_df
            st.success("✅ Null rows removed.")

    elif sub == 'Drop Columns with Nulls':
        threshold = st.slider("Threshold (%)", 0, 100, 80)
        to_drop = null_per[null_per['Null %'] > threshold]['Column'].tolist()
        if to_drop:
            st.warning(f"⚠️ Will drop columns: {', '.join(to_drop)}")
            if st.checkbox("Preview columns to be dropped"):
                st.dataframe(df[to_drop].head())
            if st.button("🗑️ Drop Columns"):
                save_snapshot(df)
                st.session_state.df = df.drop(columns=to_drop)
                st.success("✅ Columns dropped.")
        else:
            st.info("No columns exceed threshold.")

    elif sub == 'Fill Numeric Nulls':
        numeric_cols = df.select_dtypes(include='number').columns
        numeric_nulls = null_per[null_per['Column'].isin(numeric_cols)]

        if numeric_nulls.empty:
            st.info("✅ No numeric nulls.")
        else:
            numeric_fill_ui(numeric_nulls, df)
            if st.button("💾 Apply Fills"):
                save_snapshot(df)
                st.session_state.df = apply_numeric_fill(numeric_nulls, df)
                st.success("✅ Numeric nulls filled.")

    elif sub == 'Fill Categorical Nulls':
        cat_cols = df.select_dtypes(include='object').columns
        cat_nulls = null_per[null_per['Column'].isin(cat_cols)]

        if cat_nulls.empty:
            st.info("✅ No categorical nulls.")
        else:
            cat_fill_ui(cat_nulls, df)
            if st.button("💾 Apply Fills"):
                save_snapshot(df)
                st.session_state.df = apply_cat_fill(cat_nulls, df)
                st.success("✅ Categorical nulls filled.")
