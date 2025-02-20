
import streamlit as st
import pandas as pd
import numpy as np
import os
from io import BytesIO

st.set_page_config(page_title="Datasweeper", page_icon=":material/upload:", layout="wide")

# Custom CSS for styling
def custom_css():
    st.markdown(
        """
        <style>
        .title-text {
        font-size: 32px;
        color: #FFD700; /* Gold color */
        text-shadow: 3px 3px 6px rgba(255, 215, 0, 0.7); 
        font-weight: bold;
        text-align: center;
        }

        .stApp {
            background-color: black;
            color: white;
            text-align: center;
        }
        
        .block-container {
            max-width: 900px;
            margin: auto;
            padding: 20px;
        }
        
        .stButton > button {
            background: linear-gradient(45deg, #ff4b4b, #ffad4b);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 16px;
            transition: 0.3s;
        }
        
        .stButton > button:hover {
            color: black;
            transform: scale(1.1);
            box-shadow: 0px 0px 10px #ffad4b;
        }

        .stDataFrame { border-radius: 10px; }
        
        .hover-text:hover {
            color: #ffad4b;
            transition: color 0.3s;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

custom_css()

# Title with styling
st.markdown("<h2 class='title-text'>Datasweeper Sterling Integrator By Mueza Ejaz!</h2>", unsafe_allow_html=True)

st.write("<p class='hover-text'>Transform your files between CSV and Excel formats with built-in data cleaning and visualization.</p>", unsafe_allow_html=True)

# File uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue

        # File preview
        st.write(f"### Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            if st.button(f"Remove duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("Duplicates removed!")
            if st.button(f"Fill missing values for {file.name}"):
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("Missing values filled!")

        # Column selection
        st.subheader("Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            file_name = file.name.replace(file_ext, f".{conversion_type.lower()}")
            mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            df.to_csv(buffer, index=False) if conversion_type == "CSV" else df.to_excel(buffer, index=False)
            buffer.seek(0)
            st.download_button(f"Download {file_name}", buffer, file_name, mime=mime_type)

st.success("Files have been processed successfully!")



