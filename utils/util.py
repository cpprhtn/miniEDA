import pandas as pd
import numpy as np
import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title, hide_pages

def page_title():
    add_page_title()

    show_pages(
        [   
            Page("main.py", "miniEDA", "⭐"),

            Section("DataFrame", "💻"),
            Page("utils/dataframe/preview.py", "Data Preview", "📚", in_section=True),
            Page("utils/dataframe/modifycolumn.py", "Modify Column Names", "📚", in_section=True),
            Page("utils/dataframe/filterbycolumn.py", "Filter by Column", "📚", in_section=True),
            Page("utils/dataframe/pivotmelt.py", "Pivot and Melt", "📚", in_section=True),
            
            Section("Visualization", "💻"),
            Page("utils/visualization/timeseries.py", "Time Series", "📚", in_section=True),
            Page("utils/visualization/timesync.py", "Time Synchronization", "📚", in_section=True),
            Page("utils/visualization/bar.py", "Bar Plot", "📚", in_section=True),            
            Page("utils/visualization/line.py", "Line Plot", "📚", in_section=True),
            Page("utils/visualization/scatter.py", "Scatter Plot", "📚", in_section=True),
            Page("utils/visualization/heatmaps.py", "Heatmaps", "📚", in_section=True),
            
            Section("Custom", "💻"),
            Page("utils/custom.py", "Custom", "📚", in_section=True),

        ]
    )
    st.markdown(footer_html, unsafe_allow_html=True)


# Function to fill missing times in a DataFrame
def fill_missing_times(df, n, unit='minutes', data_index='timestamp', data_value='data_value', data_colum='tag', label=str, interpolate_option=str, dimension=3):
    # df[data_index] = pd.to_datetime(df[data_index])
    
    df = df.copy()
    df.loc[:, data_index] = pd.to_datetime(df[data_index])
    
    time_units = {
        'minutes': 'min',
        'hours': 'H',
        'seconds': 'S'
    }
    
    if unit not in time_units:
        raise ValueError("Unit must be 'minutes', 'hours', or 'seconds'")
    
    df = df.set_index(data_index).resample(f'{n}{time_units[unit]}').asfreq().reset_index()
    if interpolate_option == "linear":
        df[data_value] = df[data_value].interpolate(method=interpolate_option)
    elif interpolate_option == "None":
        pass
    elif interpolate_option == "mvAvg":
        df[data_value] = df[data_value].fillna(df[data_value].rolling(window=dimension, min_periods=1).mean())
    elif interpolate_option == "fFill":
        df[data_value] = df[data_value].ffill()
    elif interpolate_option == "bFill":
        df[data_value] = df[data_value].bfill()
    else:
        df[data_value] = df[data_value].interpolate(method=interpolate_option, order=dimension)

    df[data_colum] = label
    
    return df

# Function to concatenate DataFrames based on a list of tags
def concat_df(df, list, data_colum):
    if len(list) == 0:
        st.markdown("No data selected.")
        return None
    concat =  df[df[data_colum] == list[-1]]
    np.delete(list, len(list)-1)
    if len(list) >= 1:
        for i in list:
            matching_rows = df[df[data_colum] == i]
            concat = pd.concat([concat, matching_rows])
            
    return concat

def save_df(df, label="df"):
    st.session_state[label] = df
    
def load_df(label="df"):
    if label in st.session_state:
        return st.session_state[label]
    
    
footer_html = """
<style>
footer {
    visibility: hidden;
}
.main-footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 26px;
    text-align: center;
    color: black;
    background-color: #808080;
    padding: 1px 0;
    z-index: 1000;
}
.main-footer a {
    color: #000;
    text-decoration: none;
}
</style>
<div class="main-footer">
  <p>Developed by <a href="https://github.com/cpprhtn">cpprhtn</a></p>
</div>
"""