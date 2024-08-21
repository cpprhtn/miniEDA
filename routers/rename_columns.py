# routers/rename_columns.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from typing import List

from utils.utils import filter_data, convert_html

rename_columns = APIRouter()

@rename_columns.get("/rename_columns", response_class=HTMLResponse)
async def get_rename_columns(request: Request):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        return "No data uploaded"
    columns = data_frame.columns
    return request.app.state.templates.TemplateResponse("rename_column.html", {
        "request": request,
        "columns": columns
    })

@rename_columns.post("/rename_columns", response_class=HTMLResponse)
async def rename_columns_endpoint(request: Request, columns: List[str] = Form(...), new_names: List[str] = Form(...)):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        return "No data uploaded"
    
    columns_dict = {col: new_name for col, new_name in zip(columns, new_names) if new_name and new_name != col}

    try:
        data_frame = rename_columns(data_frame, columns_dict)
        request.app.state.data_frame = data_frame
    except Exception as e:
        return request.app.state.templates.TemplateResponse("data_preview.html", {
            "request": request,
            "error_message": f"Error renaming columns: {str(e)}"
        })

    return request.app.state.templates.TemplateResponse("data_preview.html", {
        "request": request,
        "df_head": convert_html(data_frame),
        "df_isna": convert_html(data_frame.fill_nan(None).null_count()),
    })
