from utils.util import *

page_title()

df = load_df(type=st.session_state["LCSV"])

if st.session_state["LCSV"]:
        st.dataframe(df.head())
        st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")
else:
    st.dataframe(df)

# Option to filter data based on a column value
filter_column = st.selectbox('Select column to filter', df.columns)
is_reg = st.checkbox("use regex?")

if is_reg:
        reg = st.text_input(f'Enter value to filter in column "{filter_column}"')
else:
    filter_value = st.text_input(f'Enter value to filter in column "{filter_column}"')
    try:
        filter_value = int(filter_value)
    except:
        pass
if st.button('Filter Data'):
    if is_reg:
        filtered_df = df[df[filter_column].str.contains(reg, regex=True)]
    else:
        filtered_df = df[df[filter_column] == filter_value]
    st.write('''This data is not applied by default.''')
    if st.session_state["LCSV"]:
        st.dataframe(filtered_df.head(), width=1000)
        st.write(f"row: {filtered_df.shape[0]}, col: {filtered_df.shape[1]}")
    else:
        st.dataframe(filtered_df, width=1000)

if st.button('Apply'):
    if is_reg:
        df = df[df[filter_column].str.contains(reg, regex=True)]
    else:
        df = df[df[filter_column] == filter_value]
    save_df(df,type=st.session_state["LCSV"])