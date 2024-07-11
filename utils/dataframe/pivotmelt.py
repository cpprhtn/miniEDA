from utils.util import *

page_title()

df = load_df(type=st.session_state["LCSV"])

if st.session_state["LCSV"]:
    st.dataframe(df.head())
else:
    st.dataframe(df)

st.subheader('Select Data Target')
data_index = st.selectbox("Select a column to go to index", df.columns)
data_colum = st.selectbox("Select a column to go to colums", df.columns)
data_value = st.selectbox("Select a column to go to value", df.columns)

# Pivot DataFrame
pivot_button = st.button('Pivot')
if pivot_button:
    pdf = df.pivot(index=data_index, columns=data_colum, values=data_value)
    st.subheader('Pivot DataFrame')
    st.write('This data is not used. Download if necessary using the button on the top right.')
    if st.session_state["LCSV"]:
        st.dataframe(pdf.head())
    else:
        st.dataframe(pdf)