import streamlit as st
import pandas as pd
from lstm_outlier import *
import plotly.express as px
import re

def fill_missing_times(df, n, unit='minutes', data_time='timestamp', data_val='power_consumption'):
    df[data_time] = pd.to_datetime(df[data_time])
    
    # 시간 단위 설정
    time_units = {
        'minutes': 'T',
        'hours': 'H',
        'seconds': 'S'
    }
    
    if unit not in time_units:
        raise ValueError("Unit must be 'minutes', 'hours', or 'seconds'")
    
    # 모든 시간 간격을 채울 수 있도록 리샘플링
    df = df.set_index(data_time).resample(f'{n}{time_units[unit]}').asfreq().reset_index()
    # df[data_val] = df[data_val].interpolate(method="values")  # method = (values/time/spline)

    return df

def concat_df(df, list, data_target):
    # print(len(list))
    if len(list) == 0:
        st.markdown("선택된 데이터가 없습니다.")
        return None
    concat =  df[df[data_target] == list[-1]]
    # print(list)
    np.delete(list, len(list)-1)
    # print(list)
    if len(list) >= 1:
        for i in list:
            # print(i)
            matching_rows = df[df[data_target] == i]
            # print(matching_rows)
            concat = pd.concat([concat, matching_rows])
            
    return concat


st.title('miniFEMS')

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # 데이터 프레임으로 읽기
    df = pd.read_csv(uploaded_file)
    st.subheader('DataFrame')
    st.write(df.head())
    
    # Transpose 버튼
    if st.button('Transpose DataFrame'):
        df = df.transpose()
        st.subheader('Transposed DataFrame')
        st.write(df.head())
        
    data_time = st.selectbox(
    "시간",
    df.columns)
    # time_query = st.text_input(label='datetime format (연:%Y 월:%m 일:%d 시:%H 분:%M 초%S)', value='ex) 연-월-일 시:분:초는 다음과 같이 작성 %Y-%m-%d %H:%M:%S')
    # if st.button("datetime format 적용"):
    #     df[data_time] = pd.to_datetime(df[data_time], format=time_query)
    #     st.write(df.head())
    
        # time_gap = df[data_time][1] - df[data_time][0]
        # st.write("time_gap:", time_gap)
        
    # st.checkbox
    data_val = st.selectbox(
    "값",
    df.columns)   
        
    data_target = st.selectbox(
    "종류",
    df.columns)
   
    # # data_query = st.selectbox(
    # "특정 대상 선택",
    # df[data_target].unique())
    # matching_rows = df[df[data_target] == data_query]
 
    
    # if st.button("특정 대상 dataframe 재생성"):
    #     # matching_rows = df[df[data_target].astype(str).str.contains(data_query, case=False, regex=True)]
    #     print(matching_rows)
    #     st.dataframe(matching_rows)
    # unique_df = df[data_target].unique().insert(1, "marge", False)
    
    unique_df = pd.DataFrame(
        {
            "data": df[data_target].unique(),
            "marged": False,
        }
    )
    edited_df = st.data_editor(
        unique_df,
        column_config={
            "marged": st.column_config.CheckboxColumn(
                default=False,
            )
        },
        disabled=["data"],
        hide_index=True,
    )
    favorite_command = edited_df.loc[edited_df["marged"]==True]
    # print(favorite_command)
    marged_df = concat_df(df, favorite_command["data"].unique(), data_target)
    try:
        st.dataframe(marged_df)
        fig = px.line(marged_df, 
            x=data_time, 
            y=data_val, 
            title='Time Series Plot', 
            color=data_target,
            labels={data_time: 'Datetime'})
        st.plotly_chart(fig)
        
    except:
        st.write(marged_df)

    unit = st.selectbox( "단위", ["minutes", "hours", "seconds"])
    n = st.text_input(label='간격', value='15')

    if st.button("데이터 결측치 탐색"):
        for i in marged_df[data_target].unique():
            st.write(i)
            df_filled = fill_missing_times(df=df[df[data_target] == i], n=n, unit=unit, data_time=data_time, data_val=data_val)
            st.dataframe(df_filled)
            st.write("결측치")
            st.write(df_filled.isna().sum())
        # #all dataset 작동코드
        # for i in df[data_target].unique():
        #     print(i)
        #     df_filled = fill_missing_times(df=df[df[data_target] == i], n=15, unit="minutes", data_time=data_time, data_val=data_val)
        #     st.dataframe(df_filled)
        #     st.write(df_filled.isna().sum())
        
    # if st.button("데이터 시각화"):
    #     fig = px.line(marged_df, 
    #         x=data_time, 
    #         y=data_val, 
    #         title='Time Series Plot', 
    #         color=data_target,
    #         labels={data_time: 'Datetime'})
    #     st.plotly_chart(fig)

    
    
    if st.button("이상치 탐색"):
        st.write("Training")
        find_outlier(data=marged_df, sequence_length=100, load=False, epochs=1, data_target=data_target, data_time=data_time, data_val=data_val)
        
