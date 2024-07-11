from utils.util import *

page_title()

df = load_df()

if df is None:
    st.warning("Visit 'miniEDA' main page and load .CSV file")
else:
    st.dataframe(df)

    st.write("Number of missing values")
    st.dataframe(df.isna().sum())
        