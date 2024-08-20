import polars as pl
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.express as px

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

# 데이터 품질 측정을 종합하는 함수
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

def plot_quality_metrics(quality_metrics: pl.DataFrame):
    """Plotly로 데이터 품질 메트릭을 시각화"""
    metrics_df = quality_metrics.to_pandas().melt(var_name='Metric', value_name='Value')

    fig = px.bar(metrics_df, x='Metric', y='Value', title='Data Quality Metrics', color='Metric',
                 labels={'Value': 'Metric Value'}, height=400)

    fig.update_layout(showlegend=False)
    fig.show()