import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image
from utils.util import *
import dask.dataframe as dd
import pyarrow


page_title()

# check cache folder
if not os.path.exists("cache"):
    os.makedirs("cache")

image = Image.open('./assets/pandas.png')
st.image(image)

col1, col2 = st.columns([1, 1])
with col1:
    read_csv_header = 0 if st.checkbox("csv header") else None
    large_csv = st.checkbox("Read Large Scale CSV")
with col2:
    read_csv_index = 0 if st.checkbox("csv index") else None
    transpose_data = st.checkbox("transpose?")


if large_csv:
    st.session_state["LCSV"] = True
    uploaded_file = st.text_input("Write file path", "")
    if st.button("load latest csv"):
        df = pd.read_parquet("./cache/df.parquet")
        if read_csv_header == 0:
            df.columns = df.iloc[0]
            df.drop([0], inplace=True)
        if read_csv_index == 0:
            df.index = df.iloc[:, 0]
            df.drop([df.columns[0]], axis=1, inplace=True)
        st.write(df.head())
        st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")
    
   
    
    else:
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file, header=read_csv_header, index_col=read_csv_index, low_memory=False)
                st.write(df.head())
                st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")
                save_df(df, "df", st.session_state["LCSV"])
            except FileNotFoundError:
                st.error('FileNotFoundError: Specified file not found') 
            except pyarrow.lib.ArrowTypeError:
                st.error('''Try to check "csv header"
                        
                        ArrowTypeError: ("Expected bytes, got a 'float' object", 'Conversion failed for column 2 with type object')
                        ''')
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, header=read_csv_header, index_col=read_csv_index, encoding="CP949", low_memory=False)
                st.write(df.head())
                st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")
                save_df(df, "df", st.session_state["LCSV"])
            
else:
    st.session_state["LCSV"] = False
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, header=read_csv_header, index_col=read_csv_index, low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, header=read_csv_header, index_col=read_csv_index, low_memory=False, encoding="CP949")
        if transpose_data:
            df = df.transpose()
        st.subheader('DataFrame Header')
        st.dataframe(df.head())
        st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")

        save_df(df, "df", st.session_state["LCSV"])