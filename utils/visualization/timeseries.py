from utils.util import *
import plotly.express as px

page_title()

df = load_df()

st.write(df)

st.subheader('Select Data Target')
data_index = st.selectbox("Select a column with time", df.columns)
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
    st.dataframe(marged_df, width=1000)
    fig = px.line(marged_df, 
        x=data_index, 
        y=data_value, 
        title='Time Series Plot', 
        color=data_colum,
        labels={data_index: 'Datetime'})
    fig.update_traces(connectgaps=False)
    st.plotly_chart(fig)
    save_df(marged_df, "df1")
    save_df(data_index, "data_index")
    save_df(data_colum, "data_colum")
    save_df(data_value, "data_value")
except:
    st.write(marged_df)