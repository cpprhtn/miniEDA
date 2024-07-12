# miniEDA

### README
1. Basically, the data is only converted and shown internally using the session of streamlit. The uploaded original data will not be transformed. (including apply button)

2. If you would like to download the transformed data, please download it through the upper right corner above the Dataframe table.

3. If the large data option is turned on, a ./cache directory is created, and csv is converted to that location to read and use data with the .parquet extension. If you specify a path on the miniEDA main page, csv is converted to ./cache, and if you leave the path empty and go to another page, it automatically reads the most recent imported dataset (./cache/df.parquet).

### install
```
pip install -r requirements.txt
```
### run
```
streamlit run main.py  # --server.maxUploadSize 1000
                       # Limit 1GB per file
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
