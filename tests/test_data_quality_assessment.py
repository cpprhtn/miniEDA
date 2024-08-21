import pytest
import polars as pl
from datetime import datetime, timedelta
from utils.data_quality_assessment_utils import *
from faker import Faker

fake = Faker()

@pytest.mark.parametrize("data_scenario", [
    {"has_timeliness": True, "columns": ["col1", "col2", "col3", "date_col"]},  # 기본 케이스
    {"has_timeliness": False, "columns": ["col1", "col2", "col3"]},  # 타임 시리즈가 없는 경우
    {"has_timeliness": True, "columns": ["col1", "col2"]},  # 일부 컬럼만 있는 경우
    # {"has_timeliness": False, "columns": ["col1"]},  # 하나의 컬럼만 있는 경우
])
def test_assess_data_quality(data_scenario):
    num_rows = 100
    data = {}

    # data_scenario의 설정에 따라 컬럼 데이터 생성
    if "col1" in data_scenario["columns"]:
        data["col1"] = [fake.random_int(min=1, max=5) for _ in range(num_rows)]
    
    if "col2" in data_scenario["columns"]:
        data["col2"] = [fake.random_int(min=1, max=100) for _ in range(num_rows)]
    
    if "col3" in data_scenario["columns"]:
        data["col3"] = [fake.random_element(elements=(1, 2, 3, None)) for _ in range(num_rows)]
    
    if data_scenario["has_timeliness"] and "date_col" in data_scenario["columns"]:
        data["date_col"] = [datetime.now() - timedelta(days=fake.random_int(min=0, max=30)) for _ in range(num_rows)]

    sample_df = pl.DataFrame(data)
    
    # accuracy, validity 파라미터 설정
    accuracy_params = {'col1': (1, 5), 'col2': (1, 80)} if "col1" in data_scenario["columns"] else {}
    validity_params = {'col1': 'numeric'} if "col1" in data_scenario["columns"] else {}

    thresholds = {
        "Completeness": 0.9,
        "Accuracy": 0.8,
        "Timeliness": 0.9,
        "Consistency": 0.9,
        "Validity": 0.9,
        "Uniqueness": 0.9
    }

    # assess_data_quality 함수 실행 시 타임 시리즈 컬럼 존재 여부에 따른 처리
    if data_scenario["has_timeliness"] and "date_col" in data_scenario["columns"]:
        quality_metrics = assess_data_quality(
            sample_df,
            accuracy_params=accuracy_params,
            timeliness_column='date_col',
            validity_params=validity_params
        )
    else:
        quality_metrics = assess_data_quality(
            sample_df,
            accuracy_params=accuracy_params,
            validity_params=validity_params
        )

    plot_quality_metrics_with_alerts(quality_metrics, thresholds)

    # 각 메트릭 확인
    if "col1" in data_scenario["columns"]:
        # Completeness 확인
        assert 'Completeness' in quality_metrics.columns
        
        completeness_value = quality_metrics['Completeness'][0]

        if isinstance(completeness_value, dict):  # 여러 컬럼의 Completeness 값이 있는 경우
            completeness_values = completeness_value.values()
        else:  # 하나의 컬럼만 있는 경우 (단일 값)
            completeness_values = [completeness_value]
        
        assert all(0.0 <= v <= 1.0 for v in completeness_values)

        # Accuracy 확인
        assert 'Accuracy_col1' in quality_metrics.columns
        assert 0.0 <= quality_metrics['Accuracy_col1'][0] <= 1.0

        # Validity 확인
        assert 'Validity_col1' in quality_metrics.columns
        assert 0.0 <= quality_metrics['Validity_col1'][0] <= 1.0
    
    # Timeliness 확인 (해당 시나리오에서만)
    if data_scenario["has_timeliness"] and "date_col" in data_scenario["columns"]:
        assert 'Timeliness' in quality_metrics.columns
        assert 0.0 <= quality_metrics['Timeliness'][0] <= 1.0
    
    # Uniqueness 확인
    assert any(col.startswith('Uniqueness') for col in quality_metrics.columns)
    uniqueness_col = next(col for col in quality_metrics.columns if col.startswith('Uniqueness'))
    assert 0.0 <= quality_metrics[uniqueness_col][0] <= 1.0