# 🧼 Cleaner – Interactive Data Cleaning App

Cleaner is a no-code Streamlit app that helps you clean messy CSV datasets with ease.  
It supports missing value handling, outlier detection, type conversions, basic EDA, and more — all through an intuitive UI.

<p align="left">
  <a href="https://data-cleaning-assistant-arfueufx59wrquriqkgk2e.streamlit.app/">
    <img src="https://img.shields.io/badge/Try%20Live%20App-Streamlit-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live App Badge">
  </a>
</p>

---


## 🧪 Try It Instantly

- 👉 [Launch the Live App](https://data-cleaning-assistant-arfueufx59wrquriqkgk2e.streamlit.app/)
- 🧠 Use built-in sample datasets (like AmesHousing) — no upload required
- ⚙️ Just click and start cleaning — no setup or coding needed

---

## Interface

![Cleaner Banner](demo/Screenshot.png)

## ✨ Features (v1.4)

- **👀 Preview & Summary**  
  - View first few rows, column types, and full `df.info()`  
  - Descriptive statistics and unique value previews  

- **🧼 Null Handling**  
  - Drop rows or columns with missing values  
  - Fill numeric nulls with median or custom constant  
  - Fill categorical nulls with most frequent or user input  

- **🧭 Duplicate & Column Handling**  
  - Detect and remove exact duplicates  
  - Drop unwanted columns with preview  

- **📊 EDA Tools**  
  - Histogram, Box Plot, Bar Plot, Category vs. Numeric Plot, Correlation Heatmap  
  - Downloadable plots with UI toggle  

- **🚨 Outlier Handling**  
  - Detect outliers using IQR  
  - Drop or cap outliers with preview of affected rows  

- **🔄 Type Conversion**  
  - Convert columns to int, float, string, or datetime  
  - Preview conversion impact before applying  

- **🛠️ Utilities**  
  - Undo last change with snapshot  
  - Reset to original uploaded file  
  - Download cleaned dataset as CSV  
  - Mobile and tablet friendly UI layout  

---

## 📁 Sample Dataset

Use this to test the app immediately:

- [AmesHousing.csv](https://raw.githubusercontent.com/aravindmarri10/data-cleaning-assistant/main/sample_data/AmesHousing.csv)  
(Hosted in the `sample_data/` folder)

---

## 🧵 Real Use Case: Ames Housing Cleaning

Using the Cleaner app, the [Ames Housing Dataset](https://www.kaggle.com/datasets/prevek18/ames-housing-dataset) was cleaned as follows:

### 🔍 Duplicate Check
- ✅ No duplicate rows found

### 🧼 Null Handling
- Dropped: `Mas Vnr Type` (60.58%), `Fireplace Qu` (48.53%)
- Filled categorical columns (most frequent):
  - `Bsmt Qual`, `Bsmt Cond`, `Bsmt Exposure`, `Garage Type`, etc.
- Filled numerical columns (median or 0):
  - `Lot Frontage`, `Mas Vnr Area`, `Garage Yr Blt`, `BsmtFin SF 1`, etc.

### 🚨 Outlier Handling
- Capped strong outliers:  
  `GrLivArea`, `SalePrice`, `TotalBsmtSF`, `GarageYrBlt`, etc.  
- Reason: Avoids row loss while reducing skew for regression models

---

## 🛠️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/aravindmarri10/data-cleaning-assistant.git
cd data-cleaning-assistant

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run cleaner_app.py
```
