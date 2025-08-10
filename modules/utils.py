import streamlit as st
import io
#===Download function=========
def download_data(df):
    st.download_button(
        label="📥 Download Cleaned CSV",
        data=df.to_csv(index=False),
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

#=====  Null summary ======
def get_null_summary(df):
    null_per = (df.isnull().mean() * 100).reset_index()
    null_per.columns = ['Column', 'Null %']
    return null_per[null_per['Null %'] > 0]

#=====  IQR Method ======
def get_iqr_bounds(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    return Q1 - 1.5 * IQR, Q3 + 1.5 * IQR


#=====  Numerical Null Fill and Apply ======
def numeric_fill_ui(null_df, df):
    for col in null_df['Column']:
        method = st.radio(f"How to fill {col}?", ['Use constant', 'Use median'], key=f'n_{col}')
        if method == 'Use constant':
            val = st.number_input(f"Value for {col}", key=f'inp_{col}')
            st.session_state[f'{col}_value'] = val
        else:
            st.session_state[f'{col}_value'] = 'median'

def apply_numeric_fill(null_df, df):
    for col in null_df['Column']:
        value = st.session_state.get(f'{col}_value')
        if value == 'median':
            med = df[col].median()
            df[col] = df[col].fillna(med)
            st.success(f"{col} filled with median ({med})")
        else:
            df[col] = df[col].fillna(value)
            st.success(f"{col} filled with {value}")
    return df

#=====  Categorical Null Fill and Apply ======
def cat_fill_ui(null_df, df):
    for col in null_df['Column']:
        method = st.radio(f"How to fill {col}?", ['Most Frequent', 'User Input'], key=f'c_{col}')
        if method == 'User Input':
            val = st.text_input(f"Value for {col}", key=f'inp_{col}')
            st.session_state[f'{col}_value'] = val
        else:
            st.session_state[f'{col}_value'] = 'freq'

def apply_cat_fill(null_df, df):
    for col in null_df['Column']:
        value = st.session_state.get(f'{col}_value')
        if value == 'freq':
            freq = df[col].value_counts().idxmax()
            df[col] = df[col].fillna(freq)
            st.success(f"{col} filled with most frequent value: {freq}")
        else:
            df[col] = df[col].fillna(value)
            st.success(f"{col} filled with constant: {value}")
    return df


#=====  Plot ======
def plot_and_download(fig, file_name):
    with st.container():
        st.pyplot(fig)
        show_download = st.checkbox("📥 Show Download Button", value=True)

        if show_download:
            download_plot(fig, file_name)

#=====  Download Plot ======
def download_plot(fig, filename):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("📥 Download Plot", buf.getvalue(), file_name=filename, mime="image/png")