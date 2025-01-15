# routers/sort.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
import pandas as pd
import polars as pl

from utils.io_utils import convert_html
from utils.data_processing import filter_data

sort_router = APIRouter()

def sort_data(data_frame: pl.DataFrame, column: str, param: str) -> pl.DataFrame:
    """주어진 열과 정렬 순서에 따라 Polars DataFrame을 정렬"""
    if param == '오름차순':
        return data_frame.sort(by=[column], descending=False)
    elif param == '내림차순':
        return data_frame.sort(by=[column], descending=True)
    elif param == '글자수':
        # 문자열 길이를 기준으로 정렬
        return data_frame.with_columns(
            pl.col(column).apply(lambda x: len(str(x)), return_dtype=pl.Int64).alias('length')
        ).sort(by=['length'], descending=False).drop('length')
    else:
        raise ValueError("Invalid sort parameter")

@sort_router.get("/sort_data", response_class=HTMLResponse)
async def get_sort_data(request: Request):
    data_frame = request.app.state.data_frame
    nodes_dict = [node.dict() for node in request.app.state.nodes]
    if data_frame is None:
        return "No data uploaded"
    
    param = ['오름차순', '내림차순', '글자수']
    return request.app.state.templates.TemplateResponse("sort.html", {
        "request": request,
        "columns": data_frame.columns,
        "param": param,
        "diagram": {
            "nodes": nodes_dict,
        }
    })

@sort_router.post("/sort_data", response_class=HTMLResponse)
async def sort_data_endpoint(
    request: Request,
    column: str = Form(...),
    param: str = Form("오름차순")
):
    data_frame = request.app.state.data_frame
    nodes_dict = [node.dict() for node in request.app.state.nodes]
    if data_frame is None:
        return "No data uploaded"
    try:
        sorted_df = sort_data(data_frame, column, param)
        request.app.state.data_frame = sorted_df  # 정렬된 데이터프레임 저장
    except Exception as e:
        return request.app.state.templates.TemplateResponse("data_preview.html", {
            "request": request,
            "error_message": f"Error filling missing values: {str(e)}"
        })

    return request.app.state.templates.TemplateResponse("data_preview.html", {
        "request": request,
        "df_head": convert_html(data_frame),
        "df_isna": convert_html(data_frame.null_count()),
        "diagram": {
            "nodes": nodes_dict,
        }
    })