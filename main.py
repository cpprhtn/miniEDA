from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routers.casting import casting
from routers.interpolate import interpolate
from routers.filtering import filtering
from routers.rename_columns import rename_columns
import polars as pl
from typing import Optional
from utils import read_file, convert_html

app = FastAPI()
 
app.include_router(casting)
app.include_router(interpolate)
app.include_router(filtering)
app.include_router(rename_columns)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    app.state.templates = templates
    app.state.data_frame = None

templates = Jinja2Templates(directory="templates")

data_frame: Optional[pl.DataFrame] = None

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    data_frame = request.app.state.data_frame
    if data_frame is None:
         mermaid_diagram = """
    graph TD;
        df1[No Data];
    """
    else:
        mermaid_diagram = """
    graph TD;
        df1[Raw Data];
    """

    return templates.TemplateResponse("index.html", {
        "request": request,
        "mermaid_diagram": mermaid_diagram
    })

@app.get("/canvas", response_class=HTMLResponse)
async def get_canvas(request: Request):
    return templates.TemplateResponse("canvas.html", {
        "request": request,
        "diagram": {
            "nodes": [
            ],
        }
    })
    
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
    
@app.get("/export_csv")
async def export_csv(response: Response, request: Request):
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
        "df_isna": convert_html(app.state.data_frame.fill_nan(None).null_count()),
    })