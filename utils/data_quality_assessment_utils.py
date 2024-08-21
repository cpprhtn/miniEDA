import polars as pl
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots


def calculate_completeness(df: pl.DataFrame) -> pl.Series:
    """완전성 확인: 데이터가 누락없이 완전한지 확인 (결측치)"""
    return df.null_count() / len(df)

def calculate_accuracy(df: pl.DataFrame, column: str, valid_range: tuple) -> float:
    """정확성 확인: 특정 열이 주어진 범위 내에 있는지 확인 (숫자형 데이터에 적용)"""
    valid = df.with_columns((pl.col(column).is_between(valid_range[0], valid_range[1])).alias('valid'))
    accuracy = valid['valid'].mean()
    return accuracy

def calculate_timeliness(df: pl.DataFrame, column: str, days_threshold: int = 7) -> float:
    """적시성 확인: 날짜 데이터가 주어진 기간 이내에 있는지 확인"""
    if df[column].dtype == pl.Datetime:
        valid = df.with_columns((pl.col(column) > (datetime.now() - timedelta(days=days_threshold))).alias('valid'))
        timeliness = valid['valid'].mean()
        return timeliness
    else:
        return np.nan

def calculate_consistency(df: pl.DataFrame, subset: list) -> float:
    """일관성 확인: 주어진 열에 대해 중복된 행이 있는지 확인"""
    return df.unique(subset=subset).height / df.height

def calculate_validity(df: pl.DataFrame, column: str, expected_type: str) -> float:
    """유효성 확인: 데이터가 기대된 형식이나 타입에 맞는지 확인"""
    if expected_type == 'datetime':
        valid = df.with_columns(pl.col(column).is_not_null().alias('valid'))
        return valid['valid'].mean()
    elif expected_type == 'numeric':
        column_dtype = df[column].dtype
        if column_dtype in [pl.Float32, pl.Float64, pl.Int32, pl.Int64]:
            valid = df.with_columns(pl.col(column).is_not_null().alias('valid'))
            return valid['valid'].mean()
        else:
            return np.nan
    elif expected_type == 'string':
        valid = df.with_columns(pl.col(column).is_not_null().alias('valid'))
        return valid['valid'].mean() if df[column].dtype == pl.Utf8 else np.nan
    else:
        return np.nan

def calculate_uniqueness(df: pl.DataFrame, column: str) -> float:
    """유일성 확인: 특정 열에서 중복된 값이 있는지 확인"""
    return df[column].n_unique() / len(df)

def assess_data_quality(df: pl.DataFrame, accuracy_params: dict = {}, timeliness_column: str = None, validity_params: dict = {}) -> pl.DataFrame:
    quality_metrics = {}

    # Completeness
    quality_metrics['Completeness'] = calculate_completeness(df)

    # Accuracy (예: {'Age': (0, 100)})
    for column, valid_range in accuracy_params.items():
        quality_metrics[f'Accuracy_{column}'] = calculate_accuracy(df, column, valid_range)

    # Timeliness (날짜열이 있는 경우에만 적용)
    if timeliness_column and timeliness_column in df.columns:
        quality_metrics['Timeliness'] = calculate_timeliness(df, timeliness_column)
    else:
        quality_metrics['Timeliness'] = np.nan

    # Consistency (여러 열의 중복 여부 확인)
    quality_metrics['Consistency'] = calculate_consistency(df, df.columns)

    # Validity (예: {'Registration Date': 'datetime', 'Age': 'numeric'})
    for column, expected_type in validity_params.items():
        quality_metrics[f'Validity_{column}'] = calculate_validity(df, column, expected_type)

    # Uniqueness (ID나 다른 열에 대해 중복 여부 확인)
    for column in df.columns:
        quality_metrics[f'Uniqueness_{column}'] = calculate_uniqueness(df, column)

    return pl.DataFrame(quality_metrics)

def plot_quality_metrics_with_alerts(quality_metrics: pl.DataFrame, thresholds: dict):
    """데이터 품질 시각화 및 임계값 초과 알림"""

    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=("Completeness", "Accuracy", "Timeliness", "Consistency", "Validity", "Uniqueness"),
        specs=[[{"type": "table"}, {"type": "table"}],  # 첫 번째 줄 (Completeness, Accuracy)
               [{"type": "table"}, {"type": "table"}],  # 두 번째 줄 (Timeliness, Consistency)
               [{"type": "table"}, {"type": "table"}]], # 세 번째 줄 (Validity, Uniqueness)
    )

    alerts = []

    # Completeness 처리
    if "Completeness" in quality_metrics.columns:
        completeness_value = quality_metrics["Completeness"][0]
        
        # Completeness 값이 단일 값인지, 여러 컬럼의 값인지 확인
        if isinstance(completeness_value, dict):  # 여러 컬럼의 Completeness 값이 있는 경우
            completeness_df = pl.DataFrame({
                "Column": list(completeness_value.keys()),
                "Value": list(completeness_value.values())
            })
        else:  # 하나의 컬럼만 있는 경우
            completeness_df = pl.DataFrame({
                "Column": ["Completeness"],
                "Value": [completeness_value]
            })

        # 임계값 체크
        completeness_threshold = thresholds.get("Completeness", 1.0)
        if completeness_df["Value"].min() < completeness_threshold:
            alerts.append(f"Warning: Completeness below threshold {completeness_threshold}")

        # 테이블 생성
        completeness_table = go.Table(
            header=dict(values=["Column", "Value"], fill_color='paleturquoise', align='left'),
            cells=dict(values=[completeness_df["Column"].to_list(), completeness_df["Value"].to_list()],
                       fill_color='lavender', align='left')
        )
    else:
        completeness_table = go.Table(
            header=dict(values=["Column", "Value"], fill_color='paleturquoise', align='left'),
            cells=dict(values=[[], []], fill_color='lavender', align='left')
        )

    # 다른 메트릭들에 대한 처리
    accuracy_columns = [col for col in quality_metrics.columns if col.startswith("Accuracy_")]
    validity_columns = [col for col in quality_metrics.columns if col.startswith("Validity_")]
    uniqueness_columns = [col for col in quality_metrics.columns if col.startswith("Uniqueness_")]

    check_thresholds(quality_metrics, "Accuracy", accuracy_columns, thresholds, alerts)
    check_thresholds(quality_metrics, "Timeliness", ["Timeliness"], thresholds, alerts)
    check_thresholds(quality_metrics, "Consistency", ["Consistency"], thresholds, alerts)
    check_thresholds(quality_metrics, "Validity", validity_columns, thresholds, alerts)
    check_thresholds(quality_metrics, "Uniqueness", uniqueness_columns, thresholds, alerts)

    fig.add_trace(completeness_table, row=1, col=1)
    fig.add_trace(create_table(quality_metrics.select(accuracy_columns), "Accuracy"), row=1, col=2)
    fig.add_trace(create_table(quality_metrics.select("Timeliness"), "Timeliness"), row=2, col=1)
    fig.add_trace(create_table(quality_metrics.select("Consistency"), "Consistency"), row=2, col=2)
    fig.add_trace(create_table(quality_metrics.select(validity_columns), "Validity"), row=3, col=1)
    fig.add_trace(create_table(quality_metrics.select(uniqueness_columns), "Uniqueness"), row=3, col=2)

    # 경고 메시지
    if alerts:
        alert_text = "<br>".join(alerts)
        fig.update_layout(
            annotations=[go.layout.Annotation(
                text=alert_text,
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=1.0,
                font=dict(color="red", size=12),
                align="center"
            )]
        )

    fig.update_layout(height=900, showlegend=False, title_text="Data Quality Metrics Overview")
    fig.show()

def create_table(data: pl.DataFrame, metric_name: str):
    """테이블 생성 도우미 함수"""
    if data.shape[0] == 0:
        return go.Table(
            header=dict(values=[metric_name, "Value"], fill_color='paleturquoise', align='left'),
            cells=dict(values=[[], []], fill_color='lavender', align='left')
        )

    return go.Table(
        header=dict(values=[metric_name, "Value"], fill_color='paleturquoise', align='left'),
        cells=dict(values=[data.columns, data.row(0)], fill_color='lavender', align='left')
    )

def check_thresholds(df: pl.DataFrame, metric_name: str, columns: list, thresholds: dict, alerts: list):
    """임계값을 초과하는지 확인하고 경고 메시지를 추가하는 함수"""
    if columns:
        metric_threshold = thresholds.get(metric_name, 1.0)
        for column in columns:
            if df[column].min() < metric_threshold:
                alerts.append(f"Warning: {metric_name} ({column}) below threshold {metric_threshold}")