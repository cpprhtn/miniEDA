from utils.util import *
import plotly.express as px

page_title()

df = load_df()

if st.session_state["LCSV"]:
    st.dataframe(df.head())
else:
    st.dataframe(df)

st.subheader('Select Data Target')
data_x = st.selectbox("Select a column with x", df.columns)
data_y = st.selectbox("Select a Column with y", df.columns)
data_title = st.text_input("title")
if st.button("Draw"):
    try:
        fig = px.imshow(df, x=data_x, y=data_y, text_auto=True)
    except:
        fig = px.imshow(df, text_auto=True)
    st.plotly_chart(fig)