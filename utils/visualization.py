import polars as pl
import plotly.express as px
import plotly.io as pio
from typing import Optional, Union


def sample_dataframe(df: pl.DataFrame, sample_size: Union[int, float]) -> pl.DataFrame:
    if isinstance(sample_size, float) and 0 < sample_size < 1:
        return df.sample(frac=sample_size)
    elif isinstance(sample_size, int) and sample_size > 0:
        return df.sample(n=sample_size)
    else:
        raise ValueError("sample_size는 0과 1 사이의 비율(float) 또는 양의 정수(int)여야 합니다.")

def optimize_dataframe_for_visualization(
    df: pl.DataFrame, 
    max_rows: int = 10000, 
    reduce_memory: bool = True
) -> pl.DataFrame:
    if df.height > max_rows:
        df = sample_dataframe(df, max_rows)
    
    if reduce_memory:
        df = reduce_dataframe_memory(df)
    
    return df

def reduce_dataframe_memory(df: pl.DataFrame) -> pl.DataFrame:
    for col in df.columns:
        if df[col].dtype == pl.Float64:
            df = df.with_column(df[col].cast(pl.Float32))
        elif df[col].dtype == pl.Int64:
            df = df.with_column(df[col].cast(pl.Int32))
    
    return df

def visualize_scatter(df: pl.DataFrame, x_column: str, y_column: str) -> str:
    df_pandas = df.to_pandas()
    fig = px.scatter(df_pandas, x=x_column, y=y_column, title=f'{x_column} vs {y_column}')
    return pio.to_html(fig, full_html=False)

def visualize_line(df: pl.DataFrame, x_column: str, y_column: str) -> str:
    df_pandas = df.to_pandas()
    fig = px.line(df_pandas, x=x_column, y=y_column, title=f'{x_column} vs {y_column} (Line Plot)')
    return pio.to_html(fig, full_html=False)

def visualize_bar(df: pl.DataFrame, x_column: str, y_column: str) -> str:
    df_pandas = df.to_pandas()
    fig = px.bar(df_pandas, x=x_column, y=y_column, title=f'{x_column} vs {y_column} (Bar Plot)')
    return pio.to_html(fig, full_html=False)

def visualize_histogram(df: pl.DataFrame, x_column: str) -> str:
    df_pandas = df.to_pandas()
    fig = px.histogram(df_pandas, x=x_column, title=f'{x_column} (Histogram)')
    return pio.to_html(fig, full_html=False)


def visualize_dataframe(
    df: pl.DataFrame, 
    x_column: str, 
    y_column: Optional[str] = None, 
    plot_type: str = 'scatter'
) -> str:
    if plot_type == 'scatter':
        return visualize_scatter(df, x_column, y_column)
    elif plot_type == 'line':
        return visualize_line(df, x_column, y_column)
    elif plot_type == 'bar':
        return visualize_bar(df, x_column, y_column)
    elif plot_type == 'histogram':
        return visualize_histogram(df, x_column)
    else:
        raise ValueError(f"지원되지 않는 시각화 유형: {plot_type}")
