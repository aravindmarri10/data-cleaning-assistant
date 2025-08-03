
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io


# ======snapshots for undo functionality ====
if 'snapshots' not in st.session_state:
    st.session_state.snapshots = []

# ====== Page Configuration ======
st.set_page_config(page_title="Cleaner", layout="wide", page_icon="🧹")
st.title("🧼 Cleaner - Your Data Cleaning Assistant")
st.markdown("A powerful app to clean, analyze, and transform your CSV datasets.")

# ====== Upload File ======
# ====== Load Data (from upload or local sample) ======
def load_data(file):
    try:
        if isinstance(file, str):  # Local sample path
            df = pd.read_csv(file)
            st.session_state.file_name = file  # store path as identifier
        else:  # Uploaded file
            if "file_name" not in st.session_state or st.session_state.file_name != file.name:
                df = pd.read_csv(file)
                st.session_state.file_name = file.name
            else:
                df = st.session_state.df.copy()  # already loaded

        df = df.replace(['-', 'n/a', 'N/A', 'missing'], np.nan)
        st.session_state.df = df
        st.session_state.raw_data = df.copy()

    except Exception as e:
        st.error(f"❌ Failed to load file: {e}")
        raise e

    return st.session_state.df, st.session_state.raw_data



# ====== Preview Section ======
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

# ====== Exploratory Data Analysis ======
def eda(df):
    st.subheader("📊 Exploratory Data Analysis")
    plot = st.sidebar.radio("Choose EDA Plot", ['Histogram', 'Box Plot', 'Bar Plot', 'Category vs. Numeric Bar', 'Heat Map'], key = "eda_plot_choice")

    if plot == 'Histogram':
        st.subheader("📉 Histogram")
        num_cols = df.select_dtypes(include='number').columns.tolist()
        col = st.selectbox("Select numeric columns", num_cols)
        fig, ax = plt.subplots(figsize=(16, 4))
        sns.histplot(df[col], kde=True, ax=ax, color="steelblue", edgecolor='black')
        ax.set_title(f"Distribution of {col}", fontsize=14, pad=10)
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")
        ax.grid(True, linestyle='--', alpha=0.5)
        plot_and_download(fig, f"{col}_hist.png")

            


    elif plot == 'Box Plot':
        st.subheader("📦 Box Plot")
        col = st.selectbox("Select a numeric column", df.select_dtypes(include='number').columns)
        fig, ax = plt.subplots(figsize=(16, 4))
        sns.boxplot(x=df[col], ax=ax, palette="Set3")
        ax.set_title(f"Boxplot of {col}", fontsize=14)
        ax.set_xlabel(col)
        file_name=f"{col}_boxplot.png"
        plot_and_download(fig, file_name )

    elif plot == 'Bar Plot':
        st.subheader("📊 Bar Plot")
        cat_col = st.selectbox("Select a categorical column", df.select_dtypes(include='object').columns)
        order = df[cat_col].value_counts().index
        fig, ax = plt.subplots(figsize=(16, 4))
        sns.countplot(x=cat_col, data=df, order=order, ax=ax, palette="Set2")
        ax.set_title(f"Count Plot of {cat_col}", fontsize=14)
        ax.set_xlabel(cat_col)
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)
        file_name=f"{cat_col}_bar_plot.png"
        plot_and_download(fig, file_name )

        
        
    elif plot == 'Category vs. Numeric Bar':
            st.subheader("📊 Category vs. Numeric Bar Plot")
            cat_col = st.selectbox("Select categorical column", df.select_dtypes(include='object').columns)
            num_col = st.selectbox("Select numeric column", df.select_dtypes(include='number').columns)
            order = df.groupby(cat_col)[num_col].mean().sort_values(ascending=False).index
            fig, ax = plt.subplots(figsize=(16, 4))
            sns.barplot(x=cat_col, y=num_col, data=df, order=order, ax=ax, palette="Set2")
            ax.set_title(f"Average {num_col} per {cat_col}", fontsize=14)
            plt.xticks(rotation=45)
            file_name=f"{cat_col}_vs_{num_col}_bar.png"
            plot_and_download(fig, file_name )
            

    elif plot == 'Heat Map':
        st.subheader("🌡️ Heatmap of Correlations")
        num_df = df.select_dtypes(include='number')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(num_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax, linewidths=0.5)
        ax.set_title("Correlation Matrix", fontsize=14)
        file_name= "correlation_heatmap.png"
        plot_and_download(fig, file_name )
        
# ====== Duplicate Detection and Column Dropping ======

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

# ====== Missing Values Handling ======
def null_handling(df):
    st.subheader("🔍 Null Value Handler")
    sub = st.sidebar.radio("Select Null Handling Method", 
        ['Null Summary', 'Drop Rows with Nulls', 'Drop Columns with Nulls',
         'Fill Numeric Nulls', 'Fill Categorical Nulls'], key = "null_handling_method")

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
            if st.button("🗑️ Drop Columns"):
                save_snapshot(df)
                df = df.drop(columns=to_drop)
                st.session_state.df = df
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
                df = apply_numeric_fill(numeric_nulls, df)
                st.session_state.df = df


    elif sub == 'Fill Categorical Nulls':
        cat_cols = df.select_dtypes(include='object').columns
        cat_nulls = null_per[null_per['Column'].isin(cat_cols)]
        if cat_nulls.empty:
            st.info("✅ No categorical nulls.")
        else:
            for col in cat_nulls['Column']:
                method = st.radio(f"How to fill {col}?", ['Most Frequent', 'User Input'], key=f'c_{col}')
                if method == 'User Input':
                    val = st.text_input(f"Value for {col}", key=f'inp_{col}')
                    st.session_state[f'{col}_value'] = val
                else:
                    st.session_state[f'{col}_value'] = 'freq'
            if st.button("💾 Apply Fills"):
                save_snapshot(df)
                for col in cat_nulls['Column']:
                    value = st.session_state.get(f'{col}_value')
                    if value == 'freq':
                        freq = df[col].value_counts().idxmax()
                        df[col] = df[col].fillna(freq)
                        st.success(f"{col} filled with most frequent value: {freq}")
                    else:
                        df[col] = df[col].fillna(value)
                        st.success(f"{col} filled with constant: {value}")
                st.session_state.df = df

# ====== Outlier Detection ======
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

# ====== Undo Change ======
def undo_change(df):
    st.subheader("🔁 Undo Change")
    st.warning("⚠️ This will revert the last change. This action cannot be undone.")
    if st.button("↩️ Confirm Undo"):
        if st.session_state.snapshots:
            st.session_state.df = st.session_state.snapshots.pop()
            st.success("✅ Reverted to last saved state.")
        else:
            st.warning("⚠️ No previous state to undo.")


def save_snapshot(df):
    """Save a copy of the current DataFrame for undo functionality."""
    st.session_state.snapshots.append(df.copy())


# ====== Reset to Original ======
def reset_data(original):
    st.subheader("🔁 Reset to Original")
    st.warning("⚠️ This will reset to raw data Frame. This action cannot be undone.")
    if st.button("Reset"):
        save_snapshot(st.session_state.df)
        st.session_state.df = original.copy()
        st.success("✅ Data reset to original uploaded file.")

#=====  Download Plot ======
def download_plot(fig, filename):
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("📥 Download Plot", buf.getvalue(), file_name=filename, mime="image/png")

#=====  Helper Function ======
#=====  Plot ======
def plot_and_download(fig, file_name):
    with st.container():
        st.pyplot(fig)
        show_download = st.checkbox("📥 Show Download Button", value=True)

        if show_download:
            download_plot(fig, file_name)

#=====  IQR Method ======
def get_iqr_bounds(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    return Q1 - 1.5 * IQR, Q3 + 1.5 * IQR

#=====  Null summary ======
def get_null_summary(df):
    null_per = (df.isnull().mean() * 100).reset_index()
    null_per.columns = ['Column', 'Null %']
    return null_per[null_per['Null %'] > 0]

#=====  Null Fill and Apply ======
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


# ====== Download Cleaned Data ======
def download_data(df):
    st.download_button(
        label="📥 Download Cleaned CSV",
        data=df.to_csv(index=False),
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

# ====== Cleaner Layout ======
def main_app():
    file = st.file_uploader("📤 Upload CSV file", type=["csv"])

    with st.expander("📂 Use Sample Dataset"):
        sample_files = {
    "IMDB": "https://raw.githubusercontent.com/aravindmarri10/data-cleaning-assistant/main/sample_data/imdb_data.csv",
    "Books": "https://raw.githubusercontent.com/aravindmarri10/data-cleaning-assistant/main/sample_data/books.csv",
    "Youtube": "https://raw.githubusercontent.com/aravindmarri10/data-cleaning-assistant/main/sample_data/Youtube.csv",
    "Automobile": "https://raw.githubusercontent.com/aravindmarri10/data-cleaning-assistant/main/sample_data/automobile_data.csv",
    "AmesHousing": "https://raw.githubusercontent.com/aravindmarri10/data-cleaning-assistant/main/sample_data/AmesHousing.csv"
}



        sample_choice = st.selectbox("Choose a sample dataset:", list(sample_files.keys()))
        if st.button("Load Selected Sample"):
            file = sample_files[sample_choice]
          
            df, original = load_data(file)
            st.success(f"Loaded sample: {sample_choice}")
        
    if file:
        df, original = load_data(file)

        tab = st.sidebar.radio(
            "📌 Select Operation",
            ["Preview", "EDA", "Duplicate Handling", "Null Handling", "Outlier Detection", "Type Convertor", "Undo Last Change", "Reset Data"]
        )

        # Add your existing feature logic calls here
        # e.g., if tab == "Preview": preview_data(df)
        if tab == "Preview":
            preview_data(df)
        elif tab == "EDA":
            eda(df)
        elif tab == "Duplicate Handling":
            task = st.sidebar.radio("Select Task", ["Remove Duplicates", "Drop Columns"], key = "dup_task")
            if task == "Remove Duplicates":
                remove_duplicates(df)
            else:
                drop_columns(df)
        elif tab == "Null Handling":
            null_handling(df)
        elif tab == "Outlier Detection":
            outlier_detection(df)
        elif tab == "Type Convertor":
            type_convertor(df)
        elif tab == "Undo Last Change":
            undo_change(df)
        elif tab == "Reset Data":
            reset_data(original)

        st.markdown("---")
        st.download_button("📥 Download Cleaned CSV", df.to_csv(index=False), "cleaned_data.csv", mime="text/csv")

      

main_app()
