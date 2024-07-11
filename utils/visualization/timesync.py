from utils.util import *
import plotly.express as px

page_title()


df = load_df()
marged_df = load_df("df1")
data_index = load_df("data_index")
data_colum = load_df("data_colum")
data_value = load_df("data_value")
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
        for i in marged_df[data_colum].unique():
            try:
                df_filled = fill_missing_times(df=df[df[data_colum] == i], n=n, unit=unit, data_index=data_index, data_value=data_value, data_colum=data_colum, label=i, interpolate_option=interpolate_option, dimension=dimension)
            except:
                df_filled = fill_missing_times(df=df[df[data_colum] == i], n=n, unit=unit, data_index=data_index, data_value=data_value, data_colum=data_colum, label=i, interpolate_option=interpolate_option)
            st.write(i)
            if st.session_state["LCSV"]:
                st.dataframe(df_filled.head())
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
