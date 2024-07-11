from utils.util import *

page_title()

df = load_df()

if st.session_state["LCSV"]:
        st.dataframe(df.head())
else:
    st.dataframe(df)

# Option to filter data based on a column value
filter_column = st.selectbox('Select column to filter', df.columns)
is_reg = st.checkbox("use regex?")
if is_reg:
        reg = st.text_input(f'Enter value to filter in column "{filter_column}"')
else:
    filter_value = st.text_input(f'Enter value to filter in column "{filter_column}"')
if st.button('Filter Data'):
    if is_reg:
    # filtered_df = df[df[filter_column] == filter_value]
        filtered_df = df[df[filter_column].str.contains(reg, regex=True)]
    else:
        filtered_df = df[df[filter_column] == filter_value]
    st.write('''This data is not applied by default.''')
    # st.write(f'Filtered data for column "{filter_column}" where value is "{filter_value}":')
    if st.session_state["LCSV"]:
        st.dataframe(filtered_df.head(), width=1000)
    else:
        st.dataframe(filtered_df, width=1000)
