import polars as pl
import io
import time
from typing import Union

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

def convert_html(data: pl.DataFrame) -> str:
    return data._repr_html_()
