# routers/casting.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse

from utils.utils import type_casting, convert_html

casting = APIRouter()

@casting.get("/type_casting", response_class=HTMLResponse, tags=['casting'])
async def get_astype(request: Request):
    data_frame = request.app.state.data_frame
    print(data_frame)
    if data_frame is None:
        return "No data uploaded"
    
    dtype_options = ['int', 'float', 'str', 'bool', 'datetime']
    return request.app.state.templates.TemplateResponse("type_casting.html", {
        "request": request, 
        "columns": data_frame.columns, 
        "dtype_options": dtype_options
        })

@casting.post("/type_casting", response_class=HTMLResponse, tags=['casting'])
async def type_casting_endpoint(request: Request, column: str = Form(...), dtype: str = Form(...)):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        return "No data uploaded"
    try:
        data_frame = type_casting(data_frame, {column: dtype})
        request.app.state.data_frame = data_frame
    except Exception as e:
        return request.app.state.templates.TemplateResponse("data_preview.html", {
            "request": request,
            "error_message": f"Error casting types: {str(e)}"
        })
    return request.app.state.templates.TemplateResponse("data_preview.html", {
        "request": request,
        "df_head": convert_html(data_frame),
        "df_isna": convert_html(data_frame.fill_nan(None).null_count()),
    })
