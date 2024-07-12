from utils.util import *

page_title()

df = load_df(type=st.session_state["LCSV"])

start_row = st.number_input("Start Row", min_value=0, max_value=len(df)-1, value=0)
end_row = st.number_input("End Row", min_value=0, max_value=len(df)-1, value=len(df)-1)

sliced_df = df.iloc[start_row:end_row+1]

if st.session_state["LCSV"]:
    st.dataframe(sliced_df.head())
    st.write(f"row: {sliced_df.shape[0]}, col: {sliced_df.shape[1]}")
else:
    st.dataframe(sliced_df)
    st.write(f"row: {sliced_df.shape[0]}, col: {sliced_df.shape[1]}")


save_df(sliced_df, "slice_df", st.session_state["LCSV"])

if st.button('Apply'):
    save_df(sliced_df,type=st.session_state["LCSV"])

