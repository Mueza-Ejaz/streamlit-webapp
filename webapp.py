import streamlit as st
import pandas as pd
import numpy as np
import os
from io import BytesIO

st.set_page_config(page_title="Growth-mindset", page_icon=":material/upload:", layout="wide")

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

        /* Instructions text green */
        div[data-testid="stFileUploader"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stRadio"] label,
        div[data-testid="stMultiselect"] label {
            color: green !important; 
        }
        
        /* Download Button Default Text */
        .stDownloadButton > button {
            position: relative;
        }

        .stDownloadButton > button::before {
            content: ' Download'; /* Default text */
            font-weight:bold;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 20px;
            color: green;
            opacity: 1;
            transition: opacity 0.3s ease-in-out;
        }

        .stDownloadButton > button:hover::before {
            opacity: 0; /* Hide text on hover */
        } ! important

        </style>
        """,
        unsafe_allow_html=True,
    )

custom_css()

# Title with styling
st.markdown("<h2 class='title-text'>Datasweeper Convertor By Mueza Ejaz!</h2>", unsafe_allow_html=True)

st.write("<p class='hover-text'>Transform your files between CSV and Excel formats with built-in data cleaning and visualization.</p>", unsafe_allow_html=True)

# File uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Load file based on extension
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine="openpyxl")
            else:
                st.error(f"Unsupported file format: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error reading file {file.name}: {str(e)}")
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
            file_name = file.name.replace(file_ext, f".{'csv' if conversion_type == 'CSV' else 'xlsx'}")
            mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            try:
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                else:  # Excel conversion fix
                    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False, sheet_name="Sheet1")
                
                buffer.seek(0)
                st.download_button(f"Download {file_name}", buffer, file_name, mime=mime_type)
                st.success(f"{file.name} converted successfully to {conversion_type}!")
            
            except Exception as e:
                st.error(f"Error converting {file.name}: {str(e)}")

st.success("Files have been processed successfully!")
