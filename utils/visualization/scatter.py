from utils.util import *
import plotly.express as px

page_title()

df = load_df()

st.write(df)

st.subheader('Select Data Target')
data_x = st.selectbox("Select a column with x", df.columns)
data_y = st.multiselect(
    "Select data to use",
    df.columns,
    [])
data_title = st.text_input("title")
if st.button("Draw"):
    fig = px.scatter(df, x=data_x, y=data_y, title=data_title)
    st.plotly_chart(fig)