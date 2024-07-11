import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image
from st_pages import Page, Section, show_pages, add_page_title, hide_pages
from utils.util import *
import dask.dataframe as dd


page_title()

# check cache folder
if not os.path.exists("cache"):
    os.makedirs("cache")

image = Image.open('./assets/pandas.png')
st.image(image)

col1, col2 = st.columns([1, 1])
with col1:
    read_csv_header = 0 if st.checkbox("csv header") else None
with col2:
    transpose_data = st.checkbox("transpose?")


if st.checkbox("Read Large Scale CSV"):
    st.session_state["LCSV"] = True
    uploaded_file = st.text_input("Write file path", "test.csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, header=read_csv_header)
            st.write(df.head())
            save_df(df, "df", st.session_state["LCSV"])
        except FileNotFoundError:
            st.error('FileNotFoundError: Specified file not found') 
        
else:
    st.session_state["LCSV"] = False
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, header=read_csv_header, low_memory=False)
        if transpose_data:
            df = df.transpose()
        st.subheader('DataFrame Header')
        st.dataframe(df.head())

        save_df(df, "df", st.session_state["LCSV"])
        