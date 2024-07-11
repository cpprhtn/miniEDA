import time
import pandas as pd
import dask.dataframe as dd

df = pd.read_csv('test.csv', low_memory=False)

# Write the dataframe to various file formats
start = time.time()
df.to_csv('df.csv', index=False)
csv_time = time.time() - start

start = time.time()
df.to_feather('df.feather')
feather_time = time.time() - start

start = time.time()
df.to_pickle('df.pickle')
pickle_time = time.time() - start

start = time.time()
df.to_parquet('df.parquet', index=False)
parquet_time = time.time() - start

# Read the data from various file formats and convert to dask dataframe
start = time.time()
dd.from_pandas(pd.read_csv('df.csv'), npartitions=4)
csv_read_time = time.time() - start

start = time.time()
dd.from_pandas(pd.read_feather('df.feather'), npartitions=4)
feather_read_time = time.time() - start

start = time.time()
dd.from_pandas(pd.read_pickle('df.pickle'), npartitions=4)
pickle_read_time = time.time() - start

start = time.time()
dd.from_pandas(pd.read_parquet('df.parquet'), npartitions=4)
parquet_read_time = time.time() - start

# Print the results
print('Writing:')
print(f'  Time to write CSV: {csv_time:.5f} seconds')
print(f'  Time to write feather: {feather_time:.5f} seconds')
print(f'  Time to write pickle: {pickle_time:.5f} seconds')
print(f'  Time to write parquet: {parquet_time:.5f} seconds')

# Determine the fastest and slowest file formats for writing
writing_times = {
    'CSV': csv_time,
    'feather': feather_time,
    'pickle': pickle_time,
    'parquet': parquet_time
}
fastest_format_writing = min(writing_times, key=writing_times.get)
slowest_format_writing = max(writing_times, key=writing_times.get)
print(f'The fastest file format for writing is {fastest_format_writing}')
print(f'The slowest file format for writing is {slowest_format_writing}')

print('\nReading and converting to dask dataframe:')
print(f'  Time to read CSV and convert: {csv_read_time:.5f} seconds')
print(f'  Time to read feather and convert: {feather_read_time:.5f} seconds')
print(f'  Time to read pickle and convert: {pickle_read_time:.5f} seconds')
print(f'  Time to read parquet and convert: {parquet_read_time:.5f} seconds')

# Determine the fastest and slowest file formats for reading and converting
reading_times = {
    'CSV': csv_read_time,
    'feather': feather_read_time,
    'pickle': pickle_read_time,
    'parquet': parquet_read_time
}
fastest_format_reading = min(reading_times, key=reading_times.get)
slowest_format_reading = max(reading_times, key=reading_times.get)
print(f'The fastest file format for reading and converting to dask dataframe is {fastest_format_reading}')
print(f'The slowest file format for reading and converting to dask dataframe is {slowest_format_reading}')
