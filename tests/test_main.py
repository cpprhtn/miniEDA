import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

@pytest.fixture
def setup_state():
    app.state.data_frame = None

def test_get_index_no_data(setup_state):
    # 데이터가 없을 때 index 페이지 테스트
    response = client.get("/")
    assert response.status_code == 200
    assert "No Data" in response.text

def test_get_index_with_data(setup_state):
    # 데이터가 있을 때 index 페이지 테스트
    import polars as pl
    app.state.data_frame = pl.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})

    response = client.get("/")
    assert response.status_code == 200
    assert "Raw Data" in response.text

def test_get_canvas(setup_state):
    # canvas 페이지 테스트
    response = client.get("/canvas")
    assert response.status_code == 200
    assert "diagram" in response.text

def test_get_data_preview_no_data(setup_state):
    # 데이터가 없을 때 data_preview 페이지 테스트
    response = client.get("/data_preview")
    assert response.status_code == 200
    assert "No data uploaded" in response.text

def test_get_data_preview_with_data(setup_state):
    # 데이터가 있을 때 data_preview 페이지 테스트
    import polars as pl
    app.state.data_frame = pl.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})

    response = client.get("/data_preview")
    assert response.status_code == 200
    # assert "data_preview.html" in response.text
    # assert 'data_preview.html' in response.data.decode()

def test_export_csv_no_data(setup_state):
    # 데이터가 없을 때 export_csv 엔드포인트 테스트
    response = client.get("/export_csv")
    assert response.status_code == 404

def test_export_csv_with_data(setup_state):
    # 데이터가 있을 때 export_csv 엔드포인트 테스트
    import polars as pl
    app.state.data_frame = pl.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})

    response = client.get("/export_csv")
    assert response.status_code == 200
    assert response.headers['Content-Type'].startswith('text/csv')
    assert "col1,col2" in response.text

def test_upload_file(setup_state):
    # 파일 업로드 테스트
    file_data = ("col1,col2\n1,2\n3,4\n").encode("utf-8")
    response = client.post(
        "/upload",
        files={"file": ("test.csv", file_data, "text/csv")},
        data={"csv_header": "true"}
    )
    assert response.status_code == 200
