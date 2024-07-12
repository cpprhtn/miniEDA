from utils.util import *
import plotly.express as px

page_title()

try:
    df = load_df(type=st.session_state["LCSV"])
    marged_df = load_df("df1", st.session_state["LCSV"])
    data_index = load_df("data_index", False)
    data_colum = load_df("data_colum", False)
    data_value = load_df("data_value", False)
except FileNotFoundError:
    st.error("Visit the 'Time Series' page first to generate data")

if df is None:
    st.warning("Visit the 'Time Series' page first to generate data")
else:  
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
        missing_cnt = {}
        
        # use_selector is True
        if st.session_state["use_selector"]:
            for i in marged_df[data_colum].unique():
                try:
                    df_filled = fill_missing_times(df=df[df[data_colum] == i], n=n, unit=unit, data_index=data_index, data_value=data_value, data_colum=data_colum, label=i, interpolate_option=interpolate_option, dimension=dimension)
                except:
                    df_filled = fill_missing_times(df=df[df[data_colum] == i], n=n, unit=unit, data_index=data_index, data_value=data_value, data_colum=data_colum, label=i, interpolate_option=interpolate_option)
                st.write(i)
                if st.session_state["LCSV"]:
                    st.dataframe(df_filled.head())
                    st.write(f"row: {df_filled.shape[0]}, col: {df_filled.shape[1]}")
                else:
                    st.dataframe(df_filled)
                missing_cnt[i] = df_filled.isna().sum()[data_value]
                eda_df = pd.concat([eda_df, df_filled])
                
            fig = px.line(eda_df, 
                x=data_index, 
                y=data_value, 
                title='Time Series Plot', 
                color=data_colum,
                labels={data_index: 'Datetime'})
            st.plotly_chart(fig)
            missing_plot = pd.DataFrame(missing_cnt, index=[0])
            st.dataframe(missing_plot)
        else:
            try:
                df = interpolate_data(marged_df, n=n, unit=unit, data_index=data_index, data_value=data_value, interpolate_option= interpolate_option, dimension = dimension)
            except:
                df = interpolate_data(marged_df, n=n, unit=unit, data_index=data_index, data_value=data_value, interpolate_option= interpolate_option)
                
            if st.session_state["LCSV"]:
                st.dataframe(df.head())
                st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")
            else:
                st.dataframe(df)
            fig = px.line(df, 
                x=data_index, 
                y=data_value, 
                title='Time Series Plot', 
                labels={data_index: 'Datetime'})
            st.plotly_chart(fig)
            missing_cnt = df.isna().sum()
            st.write("Missing Values")
            st.dataframe(missing_cnt)