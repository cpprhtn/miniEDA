import polars as pl
import numpy as np
from datetime import datetime, timedelta
from typing import List
from scipy.stats import shapiro
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def calculate_completeness(df: pl.DataFrame) -> pl.DataFrame:
    return df.null_count() / len(df)

def calculate_accuracy(df: pl.DataFrame, column: str, valid_range: tuple) -> float:
    valid = df.with_columns((pl.col(column).is_between(valid_range[0], valid_range[1])).alias('valid'))
    accuracy = valid['valid'].mean()
    return accuracy

def calculate_timeliness(df: pl.DataFrame, column: str, days_threshold: int = 7) -> float:
    if df[column].dtype == pl.Datetime:
        valid = df.with_columns((pl.col(column) > (datetime.now() - timedelta(days=days_threshold))).alias('valid'))
        timeliness = valid['valid'].mean()
        return timeliness
    else:
        return np.nan

def calculate_consistency(df: pl.DataFrame, subset: list) -> float:
    return df.unique(subset=subset).height / df.height

def calculate_validity(df: pl.DataFrame, column: str, expected_type: str) -> float:
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
    return df[column].n_unique() / len(df)

def assess_data_quality(df: pl.DataFrame, accuracy_params: dict = {}, timeliness_column: str = None, validity_params: dict = {}) -> pl.DataFrame:
    quality_metrics = {}

    quality_metrics['Completeness'] = calculate_completeness(df)

    for column, valid_range in accuracy_params.items():
        quality_metrics[f'Accuracy_{column}'] = calculate_accuracy(df, column, valid_range)

    if timeliness_column and timeliness_column in df.columns:
        quality_metrics['Timeliness'] = calculate_timeliness(df, timeliness_column)
    else:
        quality_metrics['Timeliness'] = np.nan

    quality_metrics['Consistency'] = calculate_consistency(df, df.columns)

    for column, expected_type in validity_params.items():
        quality_metrics[f'Validity_{column}'] = calculate_validity(df, column, expected_type)

    for column in df.columns:
        quality_metrics[f'Uniqueness_{column}'] = calculate_uniqueness(df, column)

    return pl.DataFrame(quality_metrics)

def validate_unique_columns(data: pl.DataFrame, columns: List[str]) -> bool:
    for col in columns:
        if data[col].is_duplicated().any():
            return False
    return True

def validate_data_distribution(data: pl.DataFrame, column: str, distribution: str = "normal") -> bool:
    if distribution == "normal":
        stat, p_value = shapiro(data[column].to_numpy())
        return p_value > 0.05  # p-value > 0.05 means data is normally distributed
    else:
        raise ValueError("Unsupported distribution type")
    
def plot_quality_metrics_with_alerts(quality_metrics: pl.DataFrame, thresholds: dict):
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=("Completeness", "Accuracy", "Timeliness", "Consistency", "Validity", "Uniqueness"),
        specs=[[{"type": "table"}, {"type": "table"}],
               [{"type": "table"}, {"type": "table"}],
               [{"type": "table"}, {"type": "table"}]],
    )

    alerts = []
    completeness_value = quality_metrics["Completeness"][0]
    completeness_df = pl.DataFrame({
        "Column": ["Completeness"],
        "Value": [completeness_value]
    })

    completeness_threshold = thresholds.get("Completeness", 1.0)
    if completeness_df["Value"].min() < completeness_threshold:
        alerts.append(f"Warning: Completeness below threshold {completeness_threshold}")

    completeness_table = go.Table(
        header=dict(values=["Column", "Value"], fill_color='paleturquoise', align='left'),
        cells=dict(values=[completeness_df["Column"].to_list(), completeness_df["Value"].to_list()],
                   fill_color='lavender', align='left')
    )

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
    if columns:
        metric_threshold = thresholds.get(metric_name, 1.0)
        for column in columns:
            if df[column].min() < metric_threshold:
                alerts.append(f"Warning: {metric_name} ({column}) below threshold {metric_threshold}")
