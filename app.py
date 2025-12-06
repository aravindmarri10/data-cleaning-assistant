import streamlit as st
from modules import (
    data_loader, preview, eda, duplicates, utils, nulls, outliers, type_converter, undo_reset, Sanitization
)



st.set_page_config(page_title="Cleaner", layout="wide", page_icon="🧹")
st.title("🧼 Cleaner - Your Data Cleaning Assistant")
st.markdown("A powerful app to clean, analyze, and transform your CSV datasets.")

# Initialize snapshots
if 'snapshots' not in st.session_state:
    st.session_state.snapshots = []

# Upload or load sample file
uploaded = st.file_uploader("📄 Upload CSV file", type=["csv"])
if uploaded:
    st.session_state.file = uploaded

with st.expander("📂 Use Sample Dataset"):
    sample_files = {
        "Books": "https://raw.githubusercontent.com/aravindmarri10/data-cleaning-assistant/main/sample_data/books.csv",
        "Youtube": "https://raw.githubusercontent.com/aravindmarri10/data-cleaning-assistant/main/sample_data/Youtube.csv",
        "Automobile": "https://raw.githubusercontent.com/aravindmarri10/data-cleaning-assistant/main/sample_data/automobile_data.csv",
        "AmesHousing": "https://raw.githubusercontent.com/aravindmarri10/data-cleaning-assistant/main/sample_data/AmesHousing.csv",
        "IMDB": "https://raw.githubusercontent.com/aravindmarri10/data-cleaning-assistant/main/sample_data/imdb_data.csv"
    }
    sample_choice = st.selectbox("Choose a sample dataset:", list(sample_files.keys()))
    if st.button("Load Selected Sample"):
        st.session_state.file = sample_files[sample_choice]
        st.success(f"Loaded sample: {sample_choice}")

# Load and display tabs if file is available
if "file" in st.session_state:
    df, original = data_loader.load_data(st.session_state.file)

    tab = st.sidebar.radio(
        "📌 Select Operation",
        ["Preview", "Data Sanitization", "Type Convertor", "Duplicate Handling", "Null Handling", "Outlier Detection", "Charts",  "Undo Last Change", "Reset Data"]
    )

    if tab == "Preview":
        preview.preview_data(df) 

    elif tab == "Data Sanitization":
        Sanitization.santize()


    elif tab == "Charts":
        eda.eda(df)

    elif tab == "Duplicate Handling":
        task = st.sidebar.radio("Select Task", ["Remove Duplicates", "Drop Columns"], key="dup_task")
        if task == "Remove Duplicates":
            duplicates.remove_duplicates()
        else:
            duplicates.drop_columns()

    elif tab == "Null Handling":
        nulls.null_handling()

    elif tab == "Outlier Detection":
        outliers.outlier_detection(df)

    elif tab == "Type Convertor":
        type_converter.type_convertor(df)

    elif tab == "Undo Last Change":
        undo_reset.undo_change(df)

    elif tab == "Reset Data":
        undo_reset.reset_data(original)

    st.markdown("---")
    utils.download_data(df)
