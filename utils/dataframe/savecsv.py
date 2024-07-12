from utils.util import *
import plotly.express as px

page_title()
if st.session_state["LCSV"]:
    
    df = load_df(type=st.session_state["LCSV"])

    file_path = st.text_input("Write file name", "test.csv")
    encoding = st.selectbox('Select encoding', ["utf-8", "euc-kr"])
    if st.button("save csv"):
        try:
            df.to_csv(file_path, encoding=encoding)
        except FileNotFoundError:
                st.error('FileNotFoundError: Invalid file path') 
                
else:
    st.error('Available only when the "Large Scale CSV option" is on ') 