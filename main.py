from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routers.casting import casting
import polars as pl
import os
from typing import List, Dict, Union, Optional
from utils import read_file, convert_html, fill_interpolation, type_casting, select_col, slice_data, rename_columns, pivot_data, melt_data, filter_data

app = FastAPI()
 
app.include_router(casting)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    app.state.templates = templates
    app.state.data_frame = None

templates = Jinja2Templates(directory="templates")

data_frame: Optional[pl.DataFrame] = None

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/data_preview", response_class=HTMLResponse)
async def get_data_preview(request: Request):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        return "No data uploaded"
    return templates.TemplateResponse("data_preview.html", {
        "request": request,
        "df_head": convert_html(data_frame),
        "df_shape": data_frame.shape,
        "df_isna": convert_html(data_frame.fill_nan(None).null_count()),
        })

@app.get("/fill_interpolation", response_class=HTMLResponse)
async def fill_interpolation(request: Request):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        return "No data uploaded"
    
    fill_option = ['linear', 'forward', 'backward', 'min', 'max', 'mean', 'zero', 'one']
    return templates.TemplateResponse("fill_interpolation.html", {"request": request, "columns": data_frame.columns, "fill_option": fill_option})

@app.get("/export_csv")
async def export_csv(response: Response):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    
    try:
        csv_data = data_frame.write_csv("export.csv")
        response.headers["Content-Disposition"] = "attachment; filename=data.csv"
        response.headers["Content-Type"] = "text/csv"
        return Response(content=csv_data, media_type="text/csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export CSV: {str(e)}")


@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...), csv_header: bool = Form(False)):
    try:
        file_type = file.filename.split('.')[-1].lower()
        df = read_file(file.file, file_type, header=csv_header)
        app.state.data_frame = df
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error_message": f"Error loading dataset: {str(e)}"
        })
    return templates.TemplateResponse("data_preview.html", {
        "request": request,
        "df_head": convert_html(app.state.data_frame),
        "df_shape": app.state.data_frame.shape,
        "df_isna": convert_html(app.state.data_frame.fill_nan(None).null_count()),
    })

@app.post("/fill_interpolation", response_class=HTMLResponse)
async def fill_interpolation_endpoint(
    request: Request,
    column: str = Form(...),
    fill_null: str = Form("linear")
):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        return "No data uploaded"

    try:
        columns = []
        if column == "__all__":
            columns = None  # 모든 컬럼을 대상으로 설정
        else:
            columns = [column]

        # fill_interpolation 함수를 사용하여 결측치 보간
        data_frame = fill_interpolation(data_frame, columns=columns, type=fill_null)
    except Exception as e:
        return templates.TemplateResponse("data_preview.html", {
            "request": request,
            "error_message": f"Error filling missing values: {str(e)}"
        })

    return templates.TemplateResponse("data_preview.html", {
        "request": request,
        "df_head": convert_html(data_frame),
        "df_shape": data_frame.shape,
        "df_isna": convert_html(data_frame.null_count()),
        "df_dtypes": convert_html(data_frame.schema)
    })

@app.post("/rename_columns", response_class=HTMLResponse)
async def rename_columns_endpoint(request: Request, columns: Dict[str, str] = Form(...)):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        return "No data uploaded"
    try:
        data_frame = rename_columns(data_frame, columns)
    except Exception as e:
        return templates.TemplateResponse("data_preview.html", {
            "request": request,
            "error_message": f"Error renaming columns: {str(e)}"
        })
    return templates.TemplateResponse("data_preview.html", {
        "request": request,
        "df_head": convert_html(data_frame.head()),
        "df_shape": data_frame.shape,
        "df_isna": convert_html(data_frame.is_null().sum().to_frame().rename({'count': 'NaN'}, axis=1)),
        "df_dtypes": convert_html(data_frame.dtypes.to_frame(name='dtype'))
    })

@app.post("/filter_data", response_class=HTMLResponse)
async def filter_data_endpoint(request: Request, condition: str = Form(...)):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        return "No data uploaded"
    try:
        data_frame = filter_data(data_frame, condition)
    except Exception as e:
        return templates.TemplateResponse("data_preview.html", {
            "request": request,
            "error_message": f"Error filtering data: {str(e)}"
        })
    return templates.TemplateResponse("data_preview.html", {
        "request": request,
        "df_head": convert_html(data_frame.head()),
        "df_shape": data_frame.shape,
        "df_isna": convert_html(data_frame.is_null().sum().to_frame().rename({'count': 'NaN'}, axis=1)),
        "df_dtypes": convert_html(data_frame.dtypes.to_frame(name='dtype'))
    })

@app.get("/export_csv")
async def export_csv(response: Response):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        raise HTTPException(status_code=404, detail="No data uploaded")
    
    try:
        csv_data = data_frame.write_csv()
        response.headers["Content-Disposition"] = "attachment; filename=data.csv"
        response.headers["Content-Type"] = "text/csv"
        return Response(content=csv_data, media_type="text/csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export CSV: {str(e)}")
