from utils.util import *
import plotly.express as px
import io
import contextlib

page_title()

df = load_df(type=st.session_state["LCSV"])

def run_code(code, *dfs):
    output = io.StringIO()
    local_vars = {df_name: df for df_name, df in zip(dataframes.keys(), dfs)}
    with contextlib.redirect_stdout(output):
        try:
            exec(code, {}, local_vars)
        except Exception as e:
            print(f"Error: {e}")
    return output.getvalue(), local_vars

if st.session_state["LCSV"]:
    st.dataframe(df.head())
    st.write(f"row: {df.shape[0]}, col: {df.shape[1]}")
else:
    st.dataframe(df)

# st.dataframe(df)

st.title("Custom Python Code Runner")
st.write(
    """
   From this page, you can enter the Python code and press the Run button to see the results. 
   
   A data frame stored in the session state can be used as a 'df' variable.
    """
)
# st.write(st.session_state)

# LCSV False 인 경우
if st.session_state["LCSV"]:
    pass
else:
    key_list = []
    for name in st.session_state.keys():
        if name.startswith('df'):
            key_list.append(name)

    options = st.multiselect(
        "Select data to use",
        key_list,
        [])

    dataframes = {}
    for name in options:
        dataframes[name] = st.session_state[name]
            

    with st.expander("Selected Data info"):
        st.write(dataframes)


    # 세션 상태에서 데이터프레임 읽어오기
    if 'df' in st.session_state:
        df = st.session_state['df']
    else:
        st.write("No DataFrame found in session state. Please create a DataFrame first.")
        st.stop()

    # 코드 입력 텍스트 영역
    code = st.text_area("Enter your Python code here:", height=200)



    # 실행 버튼
    if st.button("Run Code"):
        # 선택된 데이터프레임들을 사용하여 코드 실행
        selected_dfs = [dataframes[name] for name in dataframes.keys()]
        result, local_vars = run_code(code, *selected_dfs)
        st.subheader("Output:")
        st.text(result)
        
        if 'fig' in local_vars:
            st.subheader("Graph Output:")
            st.pyplot(local_vars['fig'])
