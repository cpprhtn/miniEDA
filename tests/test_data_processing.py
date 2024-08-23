import pytest
import polars as pl
import numpy as np
from utils.data_processing import *

# 테스트용 샘플 데이터 생성
@pytest.fixture
def sample_data():
    return pl.DataFrame({
        "col1": [1, 2, 3, None, 5],
        "col2": [10, None, 30, 40, 50],
        "col3": ["A", "B", "C", "D", "E"]
    })

@pytest.fixture
def sample_data2():
    return pl.DataFrame({
        "col1": [1, 2, 6, 7, 8],
        "col4": [100, 200, 300, 400, 500],
    })

# 테스트: 선형 보간으로 결측치 채우기
def test_fill_interpolation(sample_data):
    result = fill_interpolation(sample_data, columns=["col2"])
    assert result["col2"].null_count() == 0  # 결측치가 없어야 함

# 테스트: 중복 데이터 제거
def test_deduplicate_data():
    df = pl.DataFrame({"col1": [1, 1, 2, 3], "col2": [10, 10, 20, 30]})
    result = deduplicate_data(df)
    assert result.shape == (3, 2)  # 중복이 제거되어 3개의 행만 남아야 함

# 테스트: 결측치 제거
def test_drop_nulls(sample_data):
    result = drop_nulls(sample_data)
    assert result.shape == (3, 3)  # 결측치가 있는 행이 제거되어야 함

# 테스트: 사용자 정의 함수 적용
def test_apply_custom_function(sample_data):
    custom_func = lambda df: df.with_columns([(pl.col("col1") * 2).alias("col1")])
    result = apply_custom_function(sample_data, custom_func)
    assert result["col1"][0] == 2  # col1의 값이 두 배로 되어야 함

# 테스트: 결측치 처리 - 드롭
def test_handle_missing_values_drop(sample_data):
    result = handle_missing_values(sample_data, strategy="drop")
    assert result.shape == (3, 3)  # 결측치가 있는 행이 제거되어야 함

# 테스트: 결측치 처리 - 채우기
def test_handle_missing_values_fill(sample_data):
    result = handle_missing_values(sample_data, strategy="fill", fill_value=0)
    assert result["col1"].null_count() == 0  # 결측치가 채워져야 함
    assert result["col1"][3] == 0  # None 값이 0으로 채워져야 함

# 테스트: 타입 캐스팅
def test_type_casting(sample_data):
    result = type_casting(sample_data, {"col1": "float", "col3": "str"})
    assert result["col1"].dtype == pl.Float64  # col1이 float으로 변환되어야 함
    assert result["col3"].dtype == pl.Utf8  # col3이 문자열로 변환되어야 함

# 테스트: 컬럼 선택
def test_select_col(sample_data):
    result = select_col(sample_data, ["col1", "col3"])
    assert result.shape == (5, 2)  # 선택한 2개의 열만 포함해야 함

# 테스트: 데이터 슬라이스
def test_slice_data(sample_data):
    result = slice_data(sample_data, 1, 3)
    assert result.shape == (2, 3)  # 선택된 범위의 행만 포함해야 함

# 테스트: 컬럼 이름 변경
def test_rename_columns(sample_data):
    result = rename_columns(sample_data, {"col1": "new_col1"})
    assert "new_col1" in result.columns  # 컬럼 이름이 변경되어야 함

# 테스트: 피벗 데이터
def test_pivot_data():
    df = pl.DataFrame({
        "index": ["A", "A", "B"],
        "columns": ["X", "Y", "X"],
        "values": [1, 2, 3]
    })
    result = pivot_data(df, values=["values"], index=["index"], on=["columns"])
    assert result.shape == (2, 3)  # 피벗된 데이터의 형상이 맞아야 함

# 테스트: melt 데이터
def test_melt_data():
    df = pl.DataFrame({
        "A": [1, 2],
        "B": [3, 4],
        "C": [5, 6]
    })
    result = melt_data(df, id_vars=["A"], value_vars=["B", "C"])
    assert result.shape == (4, 3)  # melt된 데이터의 형상이 맞아야 함

# 테스트: 데이터 필터링
def test_filter_data(sample_data):
    result = filter_data(sample_data, "col1 > 2")
    assert result.shape == (2, 3)  # 필터링 조건에 맞는 행만 포함해야 함

# 테스트: 데이터 병합
def test_merge_dataframes(sample_data, sample_data2):
    result = merge_dataframes(sample_data, sample_data2, on=["col1"], how="inner")
    assert result.shape == (2, 4)  # 병합된 데이터의 형상이 맞아야 함

# 테스트: 그룹화 및 집계
# def test_group_and_aggregate():
#     df = pl.DataFrame({
#         "A": ["foo", "foo", "bar"],
#         "B": ["one", "two", "one"],
#         "C": [1, 2, 3]
#     })
    
#     result_df = group_and_aggregate(df, by=["A"], agg_funcs={"C": "sum"})
    
#     expected_df = pl.DataFrame({
#         "A": ["foo", "bar"],
#         "C_sum": [3, 3]
#     })
    
#     assert result_df.frame_equal(expected_df)


# 테스트: 데이터 정렬
def test_sort_data():
    df = pl.DataFrame({
        "A": [3, 1, 2],
        "B": [4, 2, 3]
    })
    
    sorted_df = sort_data(df, by=["A"], descending=False)
    
    expected_df = pl.DataFrame({
        "A": [1, 2, 3],
        "B": [2, 3, 4]
    })
    
    assert sorted_df.shape == expected_df.shape
    assert (sorted_df.to_numpy() == expected_df.to_numpy()).all()


# 테스트: 조건에 따른 컬럼 추가
# def test_add_column_based_on_condition():
#     df = pl.DataFrame({
#         "A": [1, 2, 3, 4, 5]
#     })
    
#     df_with_condition = add_column_based_on_condition(df, "GT_3", pl.col("A") > 3, "Yes", "No")
    
#     expected_df = pl.DataFrame({
#         "A": [1, 2, 3, 4, 5],
#         "GT_3": ["No", "No", "No", "Yes", "Yes"]
#     })
    
#     assert df_with_condition.shape == expected_df.shape
#     assert (df_with_condition.to_numpy() == expected_df.to_numpy()).all()


# 테스트: 로그 변환
def test_log_transform():
    df = pl.DataFrame({
        "A": [0, 1, 2, 3, 4]
    })
    
    df_transformed = log_transform(df, ["A"])
    
    expected_df = pl.DataFrame({
        "A": np.log1p([0, 1, 2, 3, 4])
    })
    
    assert df_transformed.shape == expected_df.shape
    assert (df_transformed.to_numpy() == expected_df.to_numpy()).all()


# 테스트: 데이터 표준화
def test_standardize_data():
    df = pl.DataFrame({"col1": [1, 2, 3, 4, 5]})
    result = standardize_data(df, columns=["col1"])
    assert np.isclose(result["col1"].mean(), 0, atol=1e-7)  # 평균이 0에 가까워야 함
    assert np.isclose(result["col1"].std(), 1, atol=1e-7)  # 표준편차가 1에 가까워야 함

# 테스트: 범주형 인코딩
def test_encode_categorical():
    df = pl.DataFrame({"category": ["A", "B", "A", "C"]})
    result = encode_categorical(df, columns=["category"], encoding="one_hot")
    assert "category_A" in result.columns  # 원-핫 인코딩된 컬럼이 포함되어야 함
    assert result.shape == (4, 3)  # 원-핫 인코딩 후 3개의 열이 있어야 함
