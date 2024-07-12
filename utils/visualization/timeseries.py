from utils.util import *
import plotly.express as px

page_title()

df = load_df(type=st.session_state["LCSV"])

if st.session_state["LCSV"]:
    st.dataframe(df.head())
    st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")
else:
    st.dataframe(df)

st.subheader('Select Data Target')
data_index = st.selectbox("Select a column with time", df.columns)

if st.checkbox("use selector"):
    data_colum = st.selectbox("Select a Column with labels", df.columns)
    data_value = st.selectbox("Select a Column with value", df.columns)

    # Data selection for visualization
    st.subheader("Select Data for Visualization")
    unique_df = pd.DataFrame(
        {
            "data": df[data_colum].unique(),
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
    marged_df = concat_df(df, favorite_command["data"].unique(), data_colum)

    try:
        st.write("Merged Data")
        if st.session_state["LCSV"]:
            st.dataframe(marged_df.head())
        else:
            st.dataframe(marged_df)
        fig = px.line(marged_df, 
            x=data_index, 
            y=data_value, 
            title='Time Series Plot', 
            color=data_colum,
            labels={data_index: 'Datetime'})
        fig.update_traces(connectgaps=False)
        st.plotly_chart(fig)
        save_df(marged_df, "df1", st.session_state["LCSV"])
        save_df(data_index, "data_index", st.session_state["LCSV"])
        save_df(data_colum, "data_colum", st.session_state["LCSV"])
        save_df(data_value, "data_value", st.session_state["LCSV"])
    except:
        st.write("No data selected. too.")

else:
    data_y = st.multiselect(
    "Select data to use",
    df.columns,
    [])
    
    if st.button("Draw"):
        fig = px.line(df, 
                x=data_index, 
                y=data_y, 
                title='Time Series Plot', 
                labels={data_index: 'Datetime'})
        fig.update_traces(connectgaps=False)
        st.plotly_chart(fig)