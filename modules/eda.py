import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from .utils import plot_and_download,download_data


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