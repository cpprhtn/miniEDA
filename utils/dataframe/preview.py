from utils.util import *

page_title()

df = load_df(type=st.session_state["LCSV"])

if df is None:
    st.warning("Visit 'miniEDA' main page and load .CSV file")
else:
    if st.session_state["LCSV"]:
        st.dataframe(df.head())
        st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")
    else:
        st.dataframe(df)

    st.write("Number of missing values")
    info = pd.concat([df.isna().sum(), df.dtypes], axis=1)
    info.columns = ["Missing Values", "Dtype"]

    st.dataframe(info)
