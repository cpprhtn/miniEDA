import polars as pl
import numpy as np
from datetime import datetime, timedelta
from typing import List
from scipy.stats import shapiro

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