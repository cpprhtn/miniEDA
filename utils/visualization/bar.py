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
data_x = st.selectbox("Select a column with x", df.columns)
data_y = st.multiselect(
    "Select data to use",
    df.columns,
    [])
data_title = st.text_input("title")
if st.button("Draw"):
    fig = px.bar(df, x=data_x, y=data_y, title=data_title)
    st.plotly_chart(fig)