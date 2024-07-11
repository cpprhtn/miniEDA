# miniEDA

### install
```
pip install -r requirements.txt
```
### run
```
streamlit run main.py

# --server.maxUploadSize 1000: Limit 1GB per file
streamlit run main.py --server.maxUploadSize 1000
```

## Large Data test
example dataset: [Kaggle 100-million-data-csv](https://www.kaggle.com/datasets/zanjibar/100-million-data-csv/data) 3GB `.csv`

### read & write test
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
