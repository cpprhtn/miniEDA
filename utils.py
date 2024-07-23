import pandas as pd
import dask.dataframe as dd
from datasets import load_dataset

def load_and_process_dataset(dataset_name, split='train', save_parquet=False):
    if dataset_name.endswith('.csv'):
        dataset = load_dataset("csv", data_files=dataset_name)
        data_split = dataset[split]

        features = data_split.features
        dtypes = {}
        for column, feature in features.items():
            dtype = feature.dtype
            if dtype == 'string':
                dtype = 'object'
            dtypes[column] = dtype

        df = pd.DataFrame(data_split)
        if save_parquet == True:
            df.to_parquet(f"{dataset_name[:-4]}.parquet", engine='pyarrow', index=False)
            ddf = dd.read_parquet(f"{dataset_name[:-4]}.parquet", engine='pyarrow', columns=list(dtypes.keys()), dtype=dtypes)
            return ddf
        return df
        
    if dataset_name.endswith('.parquet'):
        dataset = load_dataset("parquet", data_files=dataset_name)
        data_split = dataset[split]

        features = data_split.features
        dtypes = {}
        for column, feature in features.items():
            dtype = feature.dtype
            if dtype == 'string':
                dtype = 'object'
            dtypes[column] = dtype
            
        ddf = dd.read_parquet(dataset_name, engine='pyarrow', columns=list(dtypes.keys()), dtype=dtypes)
        
    return ddf

# ddf = dd.read_csv(file_path, blocksize=partition_size)

def fill_missing_times(df, n, unit='minutes', data_index='timestamp'):
    df = df.copy()
    # df.loc[:, data_index] = pd.to_datetime(df[data_index])
    df[data_index] = dd.to_datetime(df[data_index])

    time_units = {
        'minutes': 'min',
        'hours': 'H',
        'seconds': 'S'
    }
    
    if unit not in time_units:
        raise ValueError("Unit must be 'minutes', 'hours', or 'seconds'")
    # try:
    # df = df[~df.index.duplicated(keep='first')]
    df = df.set_index(data_index).resample(f'{n}{time_units[unit]}').asfreq().reset_index()
    return df
    # except Exception as e:
    #     return templates.TemplateResponse({"error_message": str(e)})

# def fill_missing_times(df, n, unit='minutes', data_index='timestamp'):
#     df = df.copy()
#     df[data_index] = dd.to_datetime(df[data_index])

#     time_units = {
#         'minutes': 'min',
#         'hours': 'H',
#         'seconds': 'S'
#     }
    
#     if unit not in time_units:
#         raise ValueError("Unit must be 'minutes', 'hours', or 'seconds'")

#     df = df.set_index(data_index).resample(f'{n}{time_units[unit]}').asfreq().reset_index()
#     return df
    
