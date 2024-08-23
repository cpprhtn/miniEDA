import pytest
import polars as pl
import io
from utils.io_utils import read_file, convert_html

# 테스트용 샘플 데이터 생성
@pytest.fixture
def sample_csv():
    csv_data = io.StringIO("col1,col2,col3\n1,2,3\n4,5,6\n")
    return csv_data

@pytest.fixture
def sample_json():
    json_data = io.StringIO('[{"col1": 1, "col2": 2, "col3": 3}, {"col1": 4, "col2": 5, "col3": 6}]')
    return json_data

@pytest.fixture
def sample_parquet(tmp_path):
    df = pl.DataFrame({"col1": [1, 4], "col2": [2, 5], "col3": [3, 6]})
    parquet_path = tmp_path / "sample.parquet"
    df.write_parquet(parquet_path)
    return parquet_path

# 테스트: CSV 파일 읽기
def test_read_file_csv(sample_csv):
    df = read_file(sample_csv, file_type='csv')
    assert df.shape == (2, 3)  # 2 rows, 3 columns
    assert df.columns == ['col1', 'col2', 'col3']
    assert df['col1'][0] == 1

# 테스트: JSON 파일 읽기
def test_read_file_json(sample_json):
    df = read_file(sample_json, file_type='json')
    assert df.shape == (2, 3)
    assert df.columns == ['col1', 'col2', 'col3']
    assert df['col1'][0] == 1

# 테스트: Parquet 파일 읽기
def test_read_file_parquet(sample_parquet):
    df = read_file(str(sample_parquet), file_type='parquet')
    assert df.shape == (2, 3)
    assert df.columns == ['col1', 'col2', 'col3']
    assert df['col1'][0] == 1

# 테스트: 지원되지 않는 파일 형식에 대한 예외 처리
def test_read_file_invalid_type():
    with pytest.raises(ValueError, match="Unsupported file type: unknown"):
        read_file("invalid_file", file_type='unknown')

# 테스트: DataFrame을 HTML로 변환
def test_convert_html(sample_csv):
    df = read_file(sample_csv, file_type='csv')
    html_str = convert_html(df)
    assert isinstance(html_str, str)
    assert "<table" in html_str  # HTML 테이블 태그 포함 여부 확인
    assert "col1" in html_str  # 열 이름 포함 여부 확인
