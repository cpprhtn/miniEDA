import pytest
import polars as pl
import plotly.graph_objs as go
from utils.visualization import plot_quality_metrics_with_alerts, create_table, check_thresholds

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
