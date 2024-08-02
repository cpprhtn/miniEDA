# routers/interpolate.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse

from utils import fill_interpolation, convert_html

interpolate = APIRouter()

@interpolate.get("/fill_interpolation", response_class=HTMLResponse)
async def fill_interpolation_get(request: Request):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        return "No data uploaded"
    
    fill_option = ['linear', 'forward', 'backward', 'min', 'max', 'mean', 'zero', 'one']
    return request.app.state.templates.TemplateResponse("fill_interpolation.html", {
        "request": request,
        "columns": data_frame.columns,
        "fill_option": fill_option
    })
    
@interpolate.post("/fill_interpolation", response_class=HTMLResponse)
async def fill_interpolation_post(
    request: Request,
    column: str = Form(...),
    fill_null: str = Form("linear")
):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        return "No data uploaded"

    try:
        if column == "__all__":
            columns = None
        else:
            columns = [column]

        data_frame = fill_interpolation(data_frame, columns=columns, type=fill_null)
        request.app.state.data_frame = data_frame

    except Exception as e:
        return request.app.state.templates.TemplateResponse("data_preview.html", {
            "request": request,
            "error_message": f"Error filling missing values: {str(e)}"
        })

    return request.app.state.templates.TemplateResponse("data_preview.html", {
        "request": request,
        "df_head": convert_html(data_frame),
        "df_isna": convert_html(data_frame.null_count()),
    })