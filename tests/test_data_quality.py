import pytest
import polars as pl
import numpy as np
from utils.data_quality import *
import plotly.graph_objs as go


@pytest.fixture
def sample_df():
    return pl.DataFrame({
        "col1": [1, 2, 3, 4, 5],
        "col2": [2, 4, 6, 8, 10],
        "col3": [1, None, 3, 4, None],
        "date_col": [datetime.now() - timedelta(days=i) for i in range(5)]
    })

def test_calculate_completeness(sample_df):
    completeness = calculate_completeness(sample_df)
    expected  = pl.DataFrame({
        "col1": [0.0],
        "col2": [0.0],
        "col3": [0.4],
        "date_col": [0.0]
    })
    
    assert completeness.equals(expected)

def test_calculate_accuracy(sample_df):
    accuracy = calculate_accuracy(sample_df, 'col1', (1, 5))
    expected_accuracy = sample_df.with_columns(
        (pl.col('col1').is_between(1, 5)).alias('valid')
    )['valid'].mean()
    assert accuracy == expected_accuracy

def test_calculate_timeliness(sample_df):
    timeliness = calculate_timeliness(sample_df, 'date_col', days_threshold=7)
    valid_dates = sample_df.with_columns(
        (pl.col('date_col') > (datetime.now() - timedelta(days=7))).alias('valid')
    )['valid'].mean()
    assert timeliness == valid_dates

def test_calculate_consistency(sample_df):
    consistency = calculate_consistency(sample_df, sample_df.columns)
    expected_consistency = sample_df.unique(subset=sample_df.columns).height / sample_df.height
    assert consistency == expected_consistency

def test_calculate_validity(sample_df):
    numeric_validity = calculate_validity(sample_df, 'col1', 'numeric')
    string_validity = calculate_validity(sample_df, 'col1', 'string')
    valid_numeric = sample_df.with_columns(
        pl.col('col1').is_not_null().alias('valid')
    )['valid'].mean()
    assert numeric_validity == valid_numeric
    assert np.isnan(string_validity) or string_validity is None

def test_calculate_uniqueness(sample_df):
    uniqueness = calculate_uniqueness(sample_df, 'col1')
    expected_uniqueness = sample_df['col1'].n_unique() / len(sample_df)
    assert uniqueness == expected_uniqueness

def test_assess_data_quality(sample_df):
    accuracy_params = {'col1': (1, 5)}
    validity_params = {'col1': 'numeric'}

    quality_metrics = assess_data_quality(
        sample_df,
        accuracy_params=accuracy_params,
        timeliness_column='date_col',
        validity_params=validity_params
    )

    assert 'Completeness' in quality_metrics.columns
    assert quality_metrics['Completeness'].shape == (1, )

    assert 'Accuracy_col1' in quality_metrics.columns

    assert 'Timeliness' in quality_metrics.columns

    assert 'Consistency' in quality_metrics.columns

    assert 'Validity_col1' in quality_metrics.columns

    assert 'Uniqueness_col1' in quality_metrics.columns
    
@pytest.fixture
def quality_metrics():
    return pl.DataFrame({
        "Completeness": [0.9],
        "Accuracy_col1": [0.95],
        "Timeliness": [0.85],
        "Consistency": [0.98],
        "Validity_col1": [0.99],
        "Uniqueness_col1": [0.97]
    })

@pytest.fixture
def thresholds():
    return {
        "Completeness": 0.95,
        "Accuracy": 0.9,
        "Timeliness": 0.9,
        "Consistency": 0.95,
        "Validity": 0.9,
        "Uniqueness": 0.95
    }

def test_plot_quality_metrics_with_alerts(quality_metrics, thresholds):
    try:
        plot_quality_metrics_with_alerts(quality_metrics, thresholds)
    except Exception as e:
        pytest.fail(f"plot_quality_metrics_with_alerts raised an exception: {e}")

def test_create_table(quality_metrics):
    table = create_table(quality_metrics.select(["Completeness"]), "Completeness")
    assert isinstance(table, go.Table)
    assert table.cells.values[0] == ["Completeness"]

def test_check_thresholds(quality_metrics, thresholds):
    alerts = []
    check_thresholds(quality_metrics, "Completeness", ["Completeness"], thresholds, alerts)
    assert "Warning: Completeness (Completeness) below threshold 0.95" in alerts

    alerts = []
    check_thresholds(quality_metrics, "Accuracy", ["Accuracy_col1"], thresholds, alerts)
    assert len(alerts) == 0  # No alerts as the accuracy is above the threshold
