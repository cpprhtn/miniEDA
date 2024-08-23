import polars as pl
from typing import Union, List, Dict, Optional, Callable

def fill_interpolation(data: pl.DataFrame, columns: Union[List[str], None] = None, type: Union[str, pl.Expr] = "linear") -> pl.DataFrame:
    if columns is None:
        columns = data.columns
    if type == 'linear':
        return data.select([pl.col(col).interpolate() if col in columns else pl.col(col) for col in data.columns])
    return data

def deduplicate_data(data: pl.DataFrame, subset: Optional[List[str]] = None, keep: str = 'first') -> pl.DataFrame:
    return data.unique(subset=subset, keep=keep)

def drop_nulls(data: pl.DataFrame, subset: Optional[List[str]] = None) -> pl.DataFrame:
    return data.drop_nulls(subset=subset)

def apply_custom_function(data: pl.DataFrame, func: Callable) -> pl.DataFrame:
    return func(data)

def handle_missing_values(data: pl.DataFrame, strategy: str = "drop", fill_value: Optional[Union[str, int, float]] = None) -> pl.DataFrame:
    if strategy == "drop":
        return data.drop_nulls()
    elif strategy == "fill" and fill_value is not None:
        return data.fill_null(fill_value)
    else:
        raise ValueError("Invalid strategy or missing fill_value")
    
def type_casting(data: pl.DataFrame, columns: Dict[str, Union[pl.DataType, str]], datetime_format: Optional[str] = None) -> pl.DataFrame:
    for col, dtype in columns.items():
        if dtype == 'datetime' and datetime_format:
            data = data.with_columns([
                pl.col(col).str.strptime(pl.Datetime, format=datetime_format)
            ])
        elif dtype == 'float':
            data = data.with_columns([
                pl.col(col).cast(pl.Float64)
            ])
        elif dtype == 'int':
            data = data.with_columns([
                pl.col(col).cast(pl.Int64)
            ])
        elif dtype == 'str':
            data = data.with_columns([
                pl.col(col).cast(pl.Utf8)
            ])
        elif dtype == 'bool':
            data = data.with_columns([
                pl.col(col).cast(pl.Boolean)
            ])
        elif isinstance(dtype, pl.DataType):
            data = data.with_columns([
                pl.col(col).cast(dtype)
            ])
        else:
            raise ValueError(f"Unsupported dtype or format: {dtype}")
    return data

def select_col(data: pl.DataFrame, columns: Union[List[str], pl.DataType]) -> pl.DataFrame:
    if isinstance(columns, list):
        selected_data = data.select(columns)
    elif isinstance(columns, type(pl.Int64)):
        selected_data = data.select([col for col in data.columns if data[col].dtype == columns])
    else:
        raise ValueError("columns should be a list of column names or a Polars DataType")
    
    return selected_data

def slice_data(data: pl.DataFrame, start: int, end: int) -> pl.DataFrame:
    return data[start:end]

def rename_columns(data: pl.DataFrame, columns: Dict[str, str]) -> pl.DataFrame:
    return data.rename(columns)

def pivot_data(data: pl.DataFrame, values: List[str], index: List[str], on: List[str]) -> pl.DataFrame:
    return data.pivot(values=values, index=index, on=on)

def melt_data(data: pl.DataFrame, id_vars: List[str], value_vars: List[str]) -> pl.DataFrame:
    return data.melt(id_vars=id_vars, value_vars=value_vars)

def filter_data(data: pl.DataFrame, condition: Union[str, pl.Expr, Callable[[pl.DataFrame], pl.DataFrame]]) -> pl.DataFrame:
    if isinstance(condition, str):
        parts = condition.split()
        if len(parts) != 3:
            raise ValueError("Condition must be in the format 'column operator value'")
        
        col_name, operator, value = parts
        expr = pl.col(col_name)

        try:
            value = float(value)
            if operator == '>':
                condition_expr = expr > value
            elif operator == '<':
                condition_expr = expr < value
            elif operator == '==':
                condition_expr = expr == value
            elif operator == '>=':
                condition_expr = expr >= value
            elif operator == '<=':
                condition_expr = expr <= value
            elif operator == '!=':
                condition_expr = expr != value
            else:
                raise ValueError(f"Unsupported operator: {operator}")
        except ValueError:
            if operator == '==':
                condition_expr = expr == value
            elif operator == '!=':
                condition_expr = expr != value
            else:
                raise ValueError(f"Unsupported operator for string comparison: {operator}")
        
        return data.filter(condition_expr)
    elif isinstance(condition, pl.Expr):
        return data.filter(condition)
    elif callable(condition):
        return condition(data)
    else:
        raise ValueError("Unsupported condition type.")
    
def merge_dataframes(df1: pl.DataFrame, df2: pl.DataFrame, on: List[str], how: str = "inner") -> pl.DataFrame:
    if how == "inner":
        return df1.join(df2, on=on, how="inner")
    elif how == "left":
        return df1.join(df2, on=on, how="left")
    elif how == "right":
        return df1.join(df2, on=on, how="right")
    elif how == "outer":
        return df1.join(df2, on=on, how="outer")
    else:
        raise ValueError("Unsupported join type")

def group_and_aggregate(data: pl.DataFrame, by: List[str], agg_funcs: Dict[str, str]) -> pl.DataFrame:
    agg_exprs = [pl.col(col).agg(func) for col, func in agg_funcs.items()]
    return data.groupby(by).agg(agg_exprs)

def sort_data(data: pl.DataFrame, by: List[str], descending: bool = False) -> pl.DataFrame:
    return data.sort(by, descending=descending)

def add_column_based_on_condition(data: pl.DataFrame, new_col_name: str, condition: pl.Expr, true_val: str, false_val: str) -> pl.DataFrame:
    return data.with_columns([
        pl.when(condition).then(true_val).otherwise(false_val).alias(new_col_name)
    ])


def log_transform(data: pl.DataFrame, columns: List[str]) -> pl.DataFrame:
    for col in columns:
        data = data.with_columns([
            (pl.col(col) + 1).log().alias(col)
        ])
    return data

def standardize_data(data: pl.DataFrame, columns: List[str]) -> pl.DataFrame:
    for col in columns:
        mean = data[col].mean()
        std = data[col].std()
        data = data.with_columns([
            ((pl.col(col) - mean) / std).alias(col)
        ])
    return data

def encode_categorical(data: pl.DataFrame, columns: List[str], encoding: str = "one_hot") -> pl.DataFrame:
    if encoding == "one_hot":
        return data.to_dummies(columns)
    elif encoding == "label":
        for col in columns:
            data = data.with_columns([
                pl.col(col).cast(pl.Categorical).cast(pl.Int32)
            ])
        return data
    else:
        raise ValueError("Unsupported encoding type")
