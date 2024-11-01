# routers/filtering.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse

from utils.io_utils import convert_html
from utils.data_processing import filter_data
filtering = APIRouter()

@filtering.get("/filter_data", response_class=HTMLResponse)
async def get_filter_data(request: Request):
    data_frame = request.app.state.data_frame
    nodes_dict = [node.dict() for node in request.app.state.nodes]
    if data_frame is None:
        return "No data uploaded"
    return request.app.state.templates.TemplateResponse("filtering.html", {
        "request": request,
        "df_head": convert_html(data_frame),
        "df_isna": convert_html(data_frame.fill_nan(None).null_count()),
        "diagram": {
            "nodes": nodes_dict,
        }
    })

@filtering.post("/filter_data", response_class=HTMLResponse)
async def filter_data_endpoint(request: Request, condition: str = Form(...)):
    data_frame = request.app.state.data_frame
    nodes_dict = [node.dict() for node in request.app.state.nodes]
    if data_frame is None:
        return "No data uploaded"
    try:
        data_frame = filter_data(data_frame, condition)
        request.app.state.data_frame = data_frame
    except Exception as e:
        return request.app.state.templates.TemplateResponse("data_preview.html", {
            "request": request,
            "error_message": f"Error filtering data: {str(e)}"
        })
    return request.app.state.templates.TemplateResponse("data_preview.html", {
        "request": request,
        "df_head": convert_html(data_frame),
        "df_isna": convert_html(data_frame.fill_nan(None).null_count()),
        "diagram": {
            "nodes": nodes_dict,
        }
    })
