import pytest
import polars as pl
from utils.utils import *
from io import BytesIO


csv_content = b"col1,col2,col3\n1,2,3\n4,5,6\n7,8,9"
xlsx_content = b""
@pytest.fixture
def sample_csv():
    return BytesIO(csv_content)

@pytest.fixture
def sample_df():
    return pl.DataFrame({
        "col1": [1, 4, 7],
        "col2": [2, 5, 8],
        "col3": [3, 6, 9]
    })

def test_read_file_csv(sample_csv):
    df = read_file(sample_csv, "csv")
    assert isinstance(df, pl.DataFrame)
    assert df.shape == (3, 3)
    assert df.columns == ["col1", "col2", "col3"]

def test_convert_html(sample_df):
    html = convert_html(sample_df)
    assert isinstance(html, str)
    assert "<table" in html

def test_fill_interpolation(sample_df):
    df_with_nan = sample_df.with_columns(pl.lit(None).alias("col4"))
    filled_df = fill_interpolation(df_with_nan)
    assert filled_df["col4"].null_count() == 0

def test_type_casting(sample_df):
    casted_df = type_casting(sample_df, {"col1": "float"})
    assert casted_df["col1"].dtype == pl.Float64

def test_select_col(sample_df):
    selected_df = select_col(sample_df, ["col1", "col2"])
    assert selected_df.shape == (3, 2)
    assert selected_df.columns == ["col1", "col2"]

def test_slice_data(sample_df):
    sliced_df = slice_data(sample_df, 0, 2)
    assert sliced_df.shape == (2, 3)

def test_rename_columns(sample_df):
    renamed_df = rename_columns(sample_df, {"col1": "new_col1"})
    assert "new_col1" in renamed_df.columns

def test_pivot_data():
    df = pl.DataFrame({
        "A": ["foo", "foo", "bar", "bar"],
        "B": ["one", "two", "one", "two"],
        "C": [1, 2, 3, 4]
    })
    pivoted_df = pivot_data(df, values=["C"], index=["A"], on=["B"])
    assert pivoted_df.shape == (2, 3)
    assert "one" in pivoted_df.columns

def test_melt_data():
    df = pl.DataFrame({
        "A": ["foo", "bar"],
        "B": [1, 3],
        "C": [2, 4]
    })
    melted_df = melt_data(df, id_vars=["A"], value_vars=["B", "C"])
    assert melted_df.shape == (4, 3)
    assert "variable" in melted_df.columns

def test_filter_data(sample_df):
    filtered_df = filter_data(sample_df, "col1 >= 4")
    print(filtered_df)
    assert filtered_df.shape == (2, 3)