from utils.util import *

page_title()

df = load_df(type=st.session_state["LCSV"])

if st.session_state["LCSV"]:
    st.dataframe(df.head())
    st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")
else:
    st.dataframe(df)

st.subheader('Pivot: Select Data Target')
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
        st.write(f"row: {pdf.shape[0]}, col: {pdf.shape[1]}")
    else:
        st.dataframe(pdf)
        
st.subheader('Melt: Select Data Target')
data_id = st.selectbox("Select a column to go to id_vars", df.columns)


if st.button("melt_button"):
    df_melted = df.melt(id_vars=data_id, var_name='Tag', value_name='Value')
    st.dataframe(df_melted.head())
    st.write(f"row: {df_melted.shape[0]}, col: {df_melted.shape[1]}")
    
if st.button('Apply'):
    df = df.melt(id_vars=data_id, var_name='Tag', value_name='Value')
    save_df(df,type=st.session_state["LCSV"])