# miniEDA

## Preparing for Change (Streamlit -> FastAPI / Flask)
Preparing for Change (Streamlit -> FastAPI / Flask)
In order to support big data, large-scale files were processed by supporting parquet in streamlit as a temporary measure, but we are preparing to migrate to FastAPI or Flask because we clearly feel the limitations of streamlit's single thread or session communication.

**If the data is less than 200MB or up to 1GB, it's also pleasant in the Streamlight version. It can be installed and built in the [Streamlight branch](https://github.com/cpprhtn/miniEDA/tree/streamlit)**

## Pandas -> Dask
For large data processing, we are changing it to the data frame of the dask, which has many advantages.

## run
```
uvicorn main:app --reload
```

### read & write test
example dataset: [Kaggle 100-million-data-csv](https://www.kaggle.com/datasets/zanjibar/100-million-data-csv/data) 3GB `.csv`
#### Writing:
```
  Time to write CSV: 135.87950 seconds
  Time to write feather: 2.44420 seconds
  Time to write pickle: 3.37542 seconds
  Time to write parquet: 11.07131 seconds
```
#### Reading and converting to dask dataframe:
```
  Time to read CSV and convert: 39.27931 seconds
  Time to read feather and convert: 10.95810 seconds
  Time to read pickle and convert: 9.47833 seconds
  Time to read parquet and convert: 7.70233 seconds
```
