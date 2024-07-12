from utils.util import *

page_title()

df = load_df(type=st.session_state["LCSV"])
    
st.subheader('Modify Column Names')
new_columns = {}
for col in df.columns:
    new_name = st.text_input(f'New name for column "{col}"', value=col)
    new_columns[col] = new_name

if st.button('Rename Columns'):
    df.rename(columns=new_columns, inplace=True)
    st.write('Updated DataFrame with new column names:')
    st.write(df.head())
    st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")

save_df(df, "df", st.session_state["LCSV"])