from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import dask.dataframe as dd
import plotly.express as px
import pandas as pd
import psutil
import os
from utils import load_and_process_dataset, fill_missing_times

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

data_frame = None
ROWS_PER_PAGE = 50
file_size = 0
system_memory = psutil.virtual_memory().total
partition_size = system_memory // 4
min_partition_size = 100 * 1024 ** 2 # 100MB
max_partition_size = 500 * 1024 ** 2 # 500MB
partition_size = max(min_partition_size, min(partition_size, max_partition_size))
npartitions = 1

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/export_csv")
async def export_csv(response: Response):
    global data_frame
    if data_frame is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    
    try:
        csv_data = data_frame.to_csv("export.csv", index=False, single_file=True)
        response.headers["Content-Disposition"] = "attachment; filename=data.csv"
        response.headers["Content-Type"] = "text/csv"
        return Response(content=csv_data, media_type="text/csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export CSV: {str(e)}")

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...), csv_header: bool = Form(False),  csv_index: bool = Form(False)):
    global data_frame
    header = 0 if csv_header else None
    index = 0 if csv_index else None
    global file_size, npartitions
    file_size = os.path.getsize(file.filename)
    npartitions = max(1, file_size // partition_size)
    # try:
    #     data_frame = pd.read_csv(file.file, header=header, index_col=index, encoding='cp949', low_memory=False)
    # except:
    #     data_frame = pd.read_csv(file.file, header=header, index_col=index, encoding='utf-8', low_memory=False)
    data_frame = load_and_process_dataset(file.filename, save_parquet=True)
    return templates.TemplateResponse("data_preview.html", {
        "request": request, 
        "df_head": data_frame.head().to_html(classes='table table-striped'), 
        "df_shape": data_frame.shape, 
        "df_isna": data_frame.isna().sum().compute().to_frame(name='NaN').to_html(classes='table table-striped'), 
        "df_dtypes": data_frame.dtypes.to_frame(name='dtype').to_html(classes='table table-striped')
    })

@app.get("/data_preview", response_class=HTMLResponse)
async def get_data_preview(request: Request):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    return templates.TemplateResponse("data_preview.html", {
        "request": request, 
        "df_head": data_frame.head().to_html(classes='table table-striped'), 
        "df_shape": data_frame.shape, 
        "df_isna": data_frame.isna().sum().compute().to_frame(name='NaN').to_html(classes='table table-striped'), 
        "df_dtypes": data_frame.dtypes.to_frame(name='dtype').to_html(classes='table table-striped')
    })

@app.get("/remove_nan", response_class=HTMLResponse)
async def get_remove_nan(request: Request):
    return templates.TemplateResponse("remove_nan.html", {"request": request})

@app.post("/remove_nan", response_class=HTMLResponse)
async def post_remove_nan(request: Request, option: str = Form(...), value: str = Form(None), axis: str = Form(None), how: str = Form(None)):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    
    if option == 'dropna':
        axis = axis if axis else 'index'
        how = how if how else 'any'
        data_frame = data_frame.dropna(axis=axis, how=how)
    elif option == 'fillna':
        fill_value = int(value) if value else 0
        data_frame = data_frame.fillna(fill_value)
    
    return templates.TemplateResponse("data_preview.html", {
        "request": request, 
        "df_head": data_frame.head().to_html(classes='table table-striped'), 
        "df_shape": data_frame.shape, 
        "df_isna": data_frame.isna().sum().compute().to_frame(name='NaN').to_html(classes='table table-striped'), 
        "df_dtypes": data_frame.dtypes.to_frame(name='dtype').to_html(classes='table table-striped')
    })

@app.get("/unique_values", response_class=HTMLResponse)
async def get_unique_values(request: Request):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    unique_values = {col: data_frame[col].unique().compute().tolist() for col in data_frame.columns}
    return templates.TemplateResponse("unique_values.html", {"request": request, "unique_values": unique_values, "columns": data_frame.columns})

@app.post("/unique_values", response_class=HTMLResponse)
async def post_unique_values(request: Request, column: str = Form(...), old_value: str = Form(...), new_value: str = Form(...)):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    try:
        # Convert column name to integer if possible
        try:
            column_name = int(column)
        except ValueError:
            column_name = column
        
        data_frame[column_name] = data_frame[column_name].replace(old_value, new_value)
    except Exception as e:
        return f"Error: {str(e)}"
    unique_values = {col: data_frame[col].unique().tolist() for col in data_frame.columns}
    return templates.TemplateResponse("data_preview.html", {
        "request": request, 
        "df_head": data_frame.head().to_html(classes='table table-striped'), 
        "df_shape": data_frame.shape, 
        "df_isna": data_frame.isna().sum().compute().to_frame(name='NaN').to_html(classes='table table-striped'), 
        "df_dtypes": data_frame.dtypes.to_frame(name='dtype').to_html(classes='table table-striped')
    })


@app.get("/astype", response_class=HTMLResponse)
async def get_astype(request: Request):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    dtype_options = ['int', 'float', 'str', 'bool', 'category', 'datetime64[ns]']
    return templates.TemplateResponse("astype.html", {"request": request, "columns": data_frame.columns, "dtype_options": dtype_options})

@app.post("/astype", response_class=HTMLResponse)
async def post_astype(request: Request, column: str = Form(...), dtype: str = Form(...)):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    try:
        try:
            column_name = int(column)
        except ValueError:
            column_name = column

        data_frame[column_name] = data_frame[column_name].astype(dtype)
    except Exception as e:
        return f"Error: {str(e)}"
    return templates.TemplateResponse("data_preview.html", {
        "request": request, 
        "df_head": data_frame.head().to_html(classes='table table-striped'), 
        "df_shape": data_frame.shape, 
        "df_isna": data_frame.isna().sum().compute().to_frame(name='NaN').to_html(classes='table table-striped'), 
        "df_dtypes": data_frame.dtypes.to_frame(name='dtype').to_html(classes='table table-striped')
    })

@app.get("/modify_columns", response_class=HTMLResponse)
async def get_modify_columns(request: Request):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    return templates.TemplateResponse("modify_columns.html", {"request": request, "columns": data_frame.columns})

@app.post("/modify_columns", response_class=HTMLResponse)
async def post_modify_columns(request: Request, new_columns: list[str] = Form(...)):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    try:
        new_columns_dict = dict(zip(data_frame.columns, new_columns))
        data_frame = data_frame.rename(columns=new_columns_dict)
    except Exception as e:
        return templates.TemplateResponse("modify_columns.html", {"request": request, "columns": data_frame.columns, "error_message": str(e)})
    
    return templates.TemplateResponse("data_preview.html", {
        "request": request, 
        "df_head": data_frame.head().compute().to_html(classes='table table-striped'), 
        "df_shape": data_frame.shape, 
        "df_isna": data_frame.isna().sum().compute().to_frame(name='NaN').to_html(classes='table table-striped'), 
        "df_dtypes": data_frame.dtypes.to_frame(name='dtype').to_html(classes='table table-striped')
    })
    
@app.get("/time_series", response_class=HTMLResponse)
async def get_time_series(request: Request):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    return templates.TemplateResponse("time_series.html", {"request": request, "columns": data_frame.columns})

@app.post("/time_series", response_class=HTMLResponse)
async def post_time_series(request: Request, n: int = Form(...), unit: str = Form(...), data_index: str = Form(...)):
    global data_frame
    if data_frame is None:
        return "No data uploaded"

    try:
        data_frame = fill_missing_times(data_frame, n, unit, data_index)
    except Exception as e:
        return templates.TemplateResponse("time_series.html", {"request": request, "columns": data_frame.columns, "error_message": str(e)})

    return templates.TemplateResponse("data_preview.html", {
        "request": request, 
        "df_head": data_frame.head().compute().to_html(classes='table table-striped'), 
        "df_shape": (data_frame.shape[0].compute(), len(data_frame.columns)), 
        "df_isna": data_frame.isna().sum().compute().to_frame(name='NaN').to_html(classes='table table-striped'), 
        "df_dtypes": data_frame.dtypes.to_frame(name='dtype').compute().to_html(classes='table table-striped')
    })

    
@app.get("/visualization", response_class=HTMLResponse)
async def get_visualization(request: Request):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    return templates.TemplateResponse("visualization.html", {"request": request, "columns": data_frame.columns})

@app.post("/visualization", response_class=HTMLResponse)
async def post_visualization(request: Request, data_x: str = Form(...), data_y: str = Form(...), data_title: str = Form(...)):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    
    try:
        fig = px.bar(data_frame, x=data_x, y=data_y, title=data_title)
        fig_html = fig.to_html(full_html=False)
    except Exception as e:
        return templates.TemplateResponse("visualization.html", {"request": request, "error_message": str(e), "columns": data_frame.columns})
    
    return templates.TemplateResponse("visualization.html", {"request": request, "plot": fig_html, "columns": data_frame.columns})

@app.get("/slice", response_class=HTMLResponse)
async def get_slice(request: Request):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    return templates.TemplateResponse("slice.html", {
        "request": request, 
        "start_idx": 0,
        "end_idx": data_frame.tail(1).index[0], 
        "columns": data_frame.columns
    })

@app.post("/slice", response_class=HTMLResponse)
async def post_slice(request: Request, start_idx: int = Form(...), end_idx: int = Form(...)):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    
    try:
        def slice_partition(partition):
            partition = partition.sort_index()
            return partition.loc[start_idx:end_idx]

        sliced_partitions = data_frame.map_partitions(slice_partition)
        sliced_df = sliced_partitions.compute()

        sliced_html = sliced_df.to_html(classes='table table-striped')

        return templates.TemplateResponse("slice.html", {
            "request": request, 
            "sliced_df": sliced_html, 
            "start_idx": start_idx, 
            "end_idx": end_idx, 
            "columns": sliced_df.columns
        })
    
    except Exception as e:
        return templates.TemplateResponse("slice.html", {
            "request": request, 
            "error_message": str(e), 
            "start_idx": start_idx, 
            "end_idx": end_idx, 
            "columns": data_frame.columns
        })
    
@app.get("/split", response_class=HTMLResponse)
async def get_split(request: Request):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    
    columns = data_frame.columns
    return templates.TemplateResponse("split.html", {
        "request": request,
        "columns": columns
    })

@app.post("/split", response_class=HTMLResponse)
async def post_split(request: Request, column: str = Form(...), value: str = Form(None)):
    global data_frame
    if data_frame is None:
        return "No data uploaded"
    
    filtered_df = data_frame.copy()
    
    if value:
        filtered_df = filtered_df[filtered_df[column] == value]
    
    return templates.TemplateResponse("split.html", {
        "request": request,
        "columns": data_frame.columns,
        "filtered_df": filtered_df.to_html(classes='table table-striped'),
        "selected_column": column,
        "selected_value": value
    })

@app.get("/get_unique_values/{column}", response_class=JSONResponse)
async def get_unique_values(column: str):
    global data_frame
    if data_frame is None:
        return JSONResponse(content={"error": "No data uploaded"}, status_code=400)
    
    unique_values = data_frame[column].unique().tolist()
    return JSONResponse(content={"unique_values": unique_values})

@app.get("/bar_plot", response_class=HTMLResponse)
async def get_bar_plot(request: Request):
    global data_frame
    if data_frame is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    return templates.TemplateResponse("bar_plot.html", {"request": request, "columns": data_frame.columns})

@app.post("/bar_plot", response_class=HTMLResponse)
async def post_bar_plot(request: Request, data_x: str = Form(...), data_y: str = Form(...), data_title: str = Form(...)):
    global data_frame
    if data_frame is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    try:
        fig = px.bar(data_frame, x=data_x, y=data_y, title=data_title)
        fig_html = fig.to_html(full_html=False)
    except Exception as e:
        return templates.TemplateResponse("bar_plot.html", {"request": request, "error_message": str(e), "columns": data_frame.columns})
    return templates.TemplateResponse("bar_plot.html", {"request": request, "plot": fig_html, "columns": data_frame.columns})

@app.get("/line_plot", response_class=HTMLResponse)
async def get_line_plot(request: Request):
    global data_frame
    if data_frame is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    return templates.TemplateResponse("line_plot.html", {"request": request, "columns": data_frame.columns})

@app.post("/line_plot", response_class=HTMLResponse)
async def post_line_plot(request: Request, data_x: str = Form(...), data_y: str = Form(...), data_title: str = Form(...)):
    global data_frame
    if data_frame is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    try:
        fig = px.line(data_frame, x=data_x, y=data_y, title=data_title)
        fig_html = fig.to_html(full_html=False)
    except Exception as e:
        return templates.TemplateResponse("line_plot.html", {"request": request, "error_message": str(e), "columns": data_frame.columns})
    return templates.TemplateResponse("line_plot.html", {"request": request, "plot": fig_html, "columns": data_frame.columns})

@app.get("/scatter_plot", response_class=HTMLResponse)
async def get_scatter_plot(request: Request):
    global data_frame
    if data_frame is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    return templates.TemplateResponse("scatter_plot.html", {"request": request, "columns": data_frame.columns})

@app.post("/scatter_plot", response_class=HTMLResponse)
async def post_scatter_plot(request: Request, data_x: str = Form(...), data_y: str = Form(...), data_title: str = Form(...)):
    global data_frame
    if data_frame is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    try:
        fig = px.scatter(data_frame, x=data_x, y=data_y, title=data_title)
        fig_html = fig.to_html(full_html=False)
    except Exception as e:
        return templates.TemplateResponse("scatter_plot.html", {"request": request, "error_message": str(e), "columns": data_frame.columns})
    return templates.TemplateResponse("scatter_plot.html", {"request": request, "plot": fig_html, "columns": data_frame.columns})

@app.get("/view_search", response_class=HTMLResponse)
async def get_view_search(request: Request, page: int = Query(1, ge=1)):
    global data_frame
    if data_frame is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    
    total_pages = (len(data_frame) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE
    start_idx = (page - 1) * ROWS_PER_PAGE
    end_idx = start_idx + ROWS_PER_PAGE
    
    def slice_partition(partition):
        return partition.loc[start_idx:end_idx]
    
    # paginated_df = data_frame[start_idx:end_idx]
    paginated_df = data_frame.map_partitions(slice_partition).compute()
    
    return templates.TemplateResponse("view_search.html", {
        "request": request,
        "columns": data_frame.columns,
        "df_html": paginated_df.to_html(classes='table table-striped'),
        "page": page,
        "total_pages": total_pages
    })

@app.post("/view_search", response_class=HTMLResponse)
async def post_view_search(request: Request, search_column: str = Form(...), search_value: str = Form(...), page: int = Query(1, ge=1)):
    global data_frame
    if data_frame is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    
    try:
        filtered_df = data_frame[data_frame[search_column].astype(str).str.contains(search_value, na=False)]
        total_pages = (len(filtered_df) + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE
        start_idx = (page - 1) * ROWS_PER_PAGE
        end_idx = start_idx + ROWS_PER_PAGE
        
        def slice_partition(partition):
            return partition.loc[start_idx:end_idx]
        
        # paginated_df = filtered_df[start_idx:end_idx]
        paginated_df = filtered_df.map_partitions(slice_partition).compute()
        
        return templates.TemplateResponse("view_search.html", {
            "request": request,
            "columns": data_frame.columns,
            "df_html": paginated_df.to_html(classes='table table-striped'),
            "search_column": search_column,
            "search_value": search_value,
            "page": page,
            "total_pages": total_pages
        })
    except Exception as e:
        return templates.TemplateResponse("view_search.html", {
            "request": request,
            "columns": data_frame.columns,
            "df_html": data_frame.to_html(classes='table table-striped'),
            "error_message": str(e),
            "page": page,
            "total_pages": total_pages
        })