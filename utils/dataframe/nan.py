from utils.util import *

page_title()

df = load_df(type=st.session_state["LCSV"])
data_how = st.selectbox("Select data to drop NaN", ["subset", "any", "all"])

if data_how == "subset":
    data_drop = st.multiselect(
    "Select data to drop NaN",
    df.columns,
    [])
    df.dropna(subset=data_drop)
    if st.session_state["LCSV"]:
        st.dataframe(df.head())
        st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")
    else:
        st.dataframe(df)
    save_df(df, "df", st.session_state["LCSV"])
else:
    df.dropna(how=data_how)
    if st.session_state["LCSV"]:
        st.dataframe(df.head())
        st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")
    else:
        st.dataframe(df)
    save_df(df, "df", st.session_state["LCSV"])
        
