from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, Response, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routers.casting import casting
from routers.interpolate import interpolate
from routers.filtering import filtering
from routers.rename_columns import rename_columns
from routers.sort import sort_router
from routers.canvas import canvasRouter
import polars as pl
from typing import Optional
from utils.io_utils import read_file, convert_html
from utils.visualization import *
from routers.model.nodes import LoadFileNode
from utils import id_generator

app = FastAPI()
 
app.include_router(casting)
app.include_router(interpolate)
app.include_router(filtering)
app.include_router(rename_columns)
app.include_router(sort_router)
app.include_router(canvasRouter, prefix="/canvas")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    app.state.fileDict = {}
    app.state.templates = templates
    app.state.data_frame = None
    app.state.nodes = []
    
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

templates = Jinja2Templates(directory="templates")

data_frame: Optional[pl.DataFrame] = None

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    data_frame = request.app.state.data_frame
    nodes_dict = [node.dict() for node in request.app.state.nodes]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "diagram": {
            "nodes": nodes_dict,
        }
    })

    
@app.get("/data_preview", response_class=HTMLResponse)
async def get_data_preview(request: Request):
    data_frame = request.app.state.data_frame
    nodes_dict = [node.dict() for node in request.app.state.nodes]
    print(data_frame.describe())
    if data_frame is None:
        return "No data uploaded"
    return templates.TemplateResponse("data_preview.html", {
        "request": request,
        "df_head": convert_html(data_frame),
        "df_shape": data_frame.shape,
        "df_describe": convert_html(data_frame.describe()),
        "df_isna": convert_html(data_frame.fill_nan(None).null_count()),
        "diagram": {
            "nodes": nodes_dict,
        }
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
        node_id = id_generator.createId()
        new_node = LoadFileNode(
            id=node_id,
            name=file.filename,
            type="DATA",
            dataType="LOAD_FILE",
            fileId=node_id
        )
        if not new_node.validate():
            raise Exception("Invalid node configuration")
        app.state.nodes.append(new_node)
        
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error_message": f"Error loading dataset: {str(e)}"
        })
        
    nodes_dict = [node.dict() for node in app.state.nodes]
    return templates.TemplateResponse("data_preview.html", {
        "request": request,
        "df_head": convert_html(app.state.data_frame),
        "df_isna": convert_html(app.state.data_frame.fill_nan(None).null_count()),
        "diagram": {
            "nodes": nodes_dict,
        }
    })
    
@app.post("/visualize", response_class=HTMLResponse)
async def visualize_data(
    request: Request,
    x_column: str = Form(...),
    y_column: Optional[str] = Form(None),
    plot_type: str = Form(...),
    max_rows: int = Form(10000)
):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        raise HTTPException(status_code=400, detail="No data uploaded")
    
    try:
        optimized_df = optimize_dataframe_for_visualization(data_frame, max_rows=max_rows)
        graph_html = visualize_dataframe(optimized_df, x_column, y_column, plot_type)
    except Exception as e:
        return templates.TemplateResponse("data_preview.html", {
            "request": request,
            "error_message": f"Error creating plot: {str(e)}"
        })

    return templates.TemplateResponse("visualize.html", {
        "request": request,
        "columns": data_frame.columns,
        "graph_html": graph_html
    })

# 데이터 정렬 함수
def sort_data(data_frame, column: str, order: str):
    """주어진 열과 정렬 순서에 따라 데이터프레임을 정렬"""
    ascending = True if order == "asc" else False
    return data_frame.sort_values(by=column, ascending=ascending)

# 데이터 정렬 페이지 렌더링
@sort_router.get("/sort_data", response_class=HTMLResponse)
async def get_sort_data(request: Request):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        return "No data uploaded"

    columns = data_frame.columns  # 열 목록 (이미 list 형식)
    return request.app.state.templates.TemplateResponse("sort.html", {
        "request": request,
        "columns": columns,
        "df_head": convert_html(data_frame.head())  # 데이터프레임 미리보기
    })

# 정렬된 데이터 결과 반환
@sort_router.post("/sort_data", response_class=HTMLResponse)
async def sort_data_endpoint(request: Request, column: str = Form(...), order: str = Form(...)):
    data_frame = request.app.state.data_frame
    if data_frame is None:
        return "No data uploaded"
    
    try:
        sorted_df = sort_data(data_frame, column, order)
        request.app.state.data_frame = sorted_df  # 정렬된 데이터프레임 저장
    except Exception as e:
        return request.app.state.templates.TemplateResponse("sort.html", {
            "request": request,
            "error_message": f"Error sorting data: {str(e)}",
            "columns": data_frame.columns,
            "df_head": convert_html(data_frame.head())  # 원본 데이터 미리보기
        })

    return request.app.state.templates.TemplateResponse("sort.html", {
        "request": request,
        "columns": data_frame.columns,
        "df_head": convert_html(sorted_df.head()),  # 정렬된 데이터 미리보기
        "success_message": "Data successfully sorted!"
    })
