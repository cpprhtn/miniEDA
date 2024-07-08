import streamlit as st
import pandas as pd
from lstm_outlier import *

st.title('miniFEMS')

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # 데이터 프레임으로 읽기
    df = pd.read_csv(uploaded_file)

    # 데이터 프레임 일부 출력
    st.subheader('DataFrame')
    st.write(df.head())
    data_target = st.selectbox(
    "종류",
    df.columns)
    st.write("You selected:", data_target)
    st.write(df[data_target].unique())
    print(df[data_target].unique(), len(df[data_target].unique()))
    data_time = st.selectbox(
    "시간",
    df.columns)
    st.write("You selected:", data_time)
    data_val = st.selectbox(
    "값",
    df.columns)
    st.write("You selected:", data_val)

    # Transpose 버튼
    if st.button('Transpose DataFrame'):
        df = df.transpose()
        st.subheader('Transposed DataFrame')
        st.write(df.head())
        
    if st.button("이상치 탐색"):
        st.write("Training")
        find_outlier(data=df, sequence_length=10, load=False, epochs=10, data_target=data_target, data_time=data_time, data_val=data_val)
        