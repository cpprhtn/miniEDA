import polars as pl
import time
from typing import Union, List, Dict, Callable, Optional
import io
# print(pl.__version__)

# 파일 읽기
def read_file(filename: Union[str, io.BytesIO], file_type: str, encoding: str = "utf-8", infer_sampling: int = 1000, header: bool = True) -> pl.DataFrame:
    start = time.time()
    
    if file_type == 'csv':
        if isinstance(filename, str):
            df = pl.read_csv(filename, infer_schema_length=infer_sampling, encoding=encoding, ignore_errors=True, has_header=header)
        else:
            df = pl.read_csv(io.BytesIO(filename.read()), infer_schema_length=infer_sampling, encoding=encoding, ignore_errors=True, has_header=header)
    elif file_type == 'xlsx':
        df = pl.read_excel(filename, sheet_id=0)
    elif file_type == 'json':
        df = pl.read_json(filename)
    elif file_type == 'parquet':
        df = pl.read_parquet(filename)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    csv_read_time = time.time() - start
    print(f'  Time to read {file_type.upper()}: {csv_read_time:.5f} seconds')
    print(df)
    return df

# Html로 변환
def convert_html(data: pl.DataFrame) -> str:
    return data._repr_html_()

# 결측치 보간
def fill_interpolation(data: pl.DataFrame, columns: Union[List[str], None] = None, type: Union[str, pl.Expr] = "linear") -> pl.DataFrame:
    if columns is None:
        columns = data.columns
    if type == "linear":
        data = data.with_columns([data[col].fill_null(0).interpolate() for col in columns])  # fill_null 추가
    else:
        data = data.with_columns([data[col].fill_null(strategy=type) if isinstance(type, str) else data[col].fill_null(type) for col in columns])
    return data

# 형 변환
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
        # 조건 문자열을 파싱하여 pl.Expr로 변환
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
