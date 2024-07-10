import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image

# Function to fill missing times in a DataFrame
def fill_missing_times(df, n, unit='minutes', time_column='timestamp', data_value='data_value', object_tag='tag', label=str, interpolate_option=str, dimension=3):
    # df[time_column] = pd.to_datetime(df[time_column])
    
    df = df.copy()
    df.loc[:, time_column] = pd.to_datetime(df[time_column])
    
    time_units = {
        'minutes': 'min',
        'hours': 'H',
        'seconds': 'S'
    }
    
    if unit not in time_units:
        raise ValueError("Unit must be 'minutes', 'hours', or 'seconds'")
    
    df = df.set_index(time_column).resample(f'{n}{time_units[unit]}').asfreq().reset_index()
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
    # elif interpolate_option == "time":
        # df[data_value] = pd.DataFrame(df[object_tag], index=df[time_column]).interpolate(method="time")
        # print(df.set_index(time_column))
        # df[data_value] = df.set_index(time_column).interpolate(method="time")[data_value]
        # df[data_value] = df.set_index(time_column).infer_objects(copy=False).interpolate(method="time").reset_index()[data_value]
    else:
        df[data_value] = df[data_value].interpolate(method=interpolate_option, order=dimension)

    df[object_tag] = label
    
    return df

# Function to concatenate DataFrames based on a list of tags
def concat_df(df, list, object_tag):
    if len(list) == 0:
        st.markdown("No data selected.")
        return None
    concat =  df[df[object_tag] == list[-1]]
    np.delete(list, len(list)-1)
    if len(list) >= 1:
        for i in list:
            matching_rows = df[df[object_tag] == i]
            concat = pd.concat([concat, matching_rows])
            
    return concat

def main():
    
    st.title('miniEDA')
    image = Image.open('./assets/pandas.png')
    st.image(image)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        read_csv_header = 0 if st.checkbox("csv header") else None
    with col2:
        transpose_data = st.checkbox("transpose?")

    # File uploader
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, header=read_csv_header, low_memory=False)
        if transpose_data:
            df = df.transpose()
        st.subheader('DataFrame Preview')
        st.write(df.head())
        
        # Option to rename columns
        # st.subheader('Modify Column Names')
        # new_columns = {}
        # for col in df.columns:
        #     new_name = st.text_input(f'New name for column "{col}"', value=col)
        #     new_columns[col] = new_name
        
        # if st.button('Rename Columns'):
        #     df.rename(columns=new_columns, inplace=True)
        #     st.write('Updated DataFrame with new column names:')
        #     st.write(df.head())

        # Option to filter data based on a column value
        st.subheader('Filtering based on Column')
        filter_column = st.selectbox('Select column to filter', df.columns)
        filter_value = st.text_input(f'Enter value to filter in column "{filter_column}"')
        
        if st.button('Filter Data'):
            filtered_df = df[df[filter_column] == filter_value]
            st.write('This data is not used. Download if necessary using the button on the top right.')
            st.write(f'Filtered data for column "{filter_column}" where value is "{filter_value}":')
            st.write(filtered_df)

        st.subheader('Setting Data Target (Time Series)')
        time_column = st.selectbox("Select Time Column", df.columns)
        data_value = st.selectbox("Select Data Value Column", df.columns)
        object_tag = st.selectbox("Select Object Tag Column", df.columns)

        # Pivot DataFrame
        pivot_button = st.button('Pivot')
        if pivot_button:
            pdf = df.pivot(index=time_column, columns=object_tag, values=data_value)
            st.subheader('Pivot DataFrame')
            st.write('This data is not used. Download if necessary using the button on the top right.')
            st.dataframe(pdf)
            
        # Data selection for visualization
        st.subheader("Select Data for Visualization")
        unique_df = pd.DataFrame(
            {
                "data": df[object_tag].unique(),
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
            width=1000,
        )
        
        favorite_command = edited_df.loc[edited_df["marged"]==True]
        marged_df = concat_df(df, favorite_command["data"].unique(), object_tag)
        
        try:
            st.write("Merged Data")
            st.dataframe(marged_df, width=1000)
            fig = px.line(marged_df, 
                x=time_column, 
                y=data_value, 
                title='Time Series Plot', 
                color=object_tag,
                labels={time_column: 'Datetime'})
            st.plotly_chart(fig)
        except:
            st.write(marged_df)
        
        # Fill missing times and interpolate
        unit = st.selectbox("Select Unit", ["minutes", "hours", "seconds"])
        n = st.text_input(label='Interval', value='15')
        
        is_interpolate = st.checkbox("Interpolate?")
        if is_interpolate:
            interpolate_option = st.selectbox(
                "Interpolation Option",
                ["linear", "polynomial", "cubic", "mvAvg", "fFill", "bFill"]
            )
            if interpolate_option in ["polynomial", "cubic"]:
                dimension = st.slider("control dimension", 2, 100)
            elif interpolate_option in ["mvAvg"]:
                dimension = st.slider("window size", 3, 1000)
        else:
            interpolate_option = "None"
        
        if st.button("Search for Missing Data"):
            eda_df = pd.DataFrame()
            for i in marged_df[object_tag].unique():
                try:
                    df_filled = fill_missing_times(df=df[df[object_tag] == i], n=n, unit=unit, time_column=time_column, data_value=data_value, object_tag=object_tag, label=i, interpolate_option=interpolate_option, dimension=dimension)
                except:
                    df_filled = fill_missing_times(df=df[df[object_tag] == i], n=n, unit=unit, time_column=time_column, data_value=data_value, object_tag=object_tag, label=i, interpolate_option=interpolate_option)
                st.write(i)
                st.dataframe(df_filled)
                st.write("Missing Data")
                st.write(df_filled.isna().sum())
                eda_df = pd.concat([eda_df, df_filled])
            
            fig = px.line(eda_df, 
                x=time_column, 
                y=data_value, 
                title='Time Series Plot', 
                color=object_tag,
                labels={time_column: 'Datetime'})
            st.plotly_chart(fig)
        
        
if __name__ == "__main__":
    main()
