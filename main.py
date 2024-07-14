from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import dask.dataframe as dd
import os
import io

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Define df and file path globally
df = None
file_location = None

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/data_preview", response_class=HTMLResponse)
async def data_preview(request: Request):
    global df
    if df is not None:
        head = df.head().to_html()
        isna = df.isna().sum().compute().to_string()
        buf = io.StringIO()
        df.info(buf=buf)
        info = buf.getvalue()
    else:
        head = "<p>No data available. Please upload a file first.</p>"
        isna = ""
        info = ""

    return templates.TemplateResponse("data_preview.html", {"request": request, "head": head, "isna": isna, "info": info})

@app.get("/remove_nan", response_class=HTMLResponse)
async def remove_nan(request: Request):
    global df
    if df is not None:
        head = df.head().to_html()
        isna = df.isna().sum().compute().to_string()
    else:
        head = "<p>No data available. Please upload a file first.</p>"
        isna = ""

    return templates.TemplateResponse("remove_nan.html", {"request": request, "head": head, "isna": isna})

@app.get("/unique_values", response_class=HTMLResponse)
async def unique_values(request: Request):
    return templates.TemplateResponse("unique_values.html", {"request": request})

@app.get("/unique_values_data")
async def unique_values_data():
    global df
    if df is None:
        raise HTTPException(status_code=400, detail="No data available. Please upload a file first.")
    
    try:
        unique_values = {col: df[col].dropna().unique().compute().tolist() for col in df.columns}
        return JSONResponse(content=unique_values)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update_value")
async def update_value(column: str = Form(...), old_value: str = Form(...), new_value: str = Form(...)):
    global df
    if df is None:
        raise HTTPException(status_code=400, detail="No data available. Please upload a file first.")
    
    try:
        df[column] = df[column].map(lambda x: new_value if x == old_value else x)
        return HTMLResponse(content=f"Updated value {old_value} to {new_value} in column {column}.", status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/astype_column")
async def astype_column(column: str = Form(...), new_dtype: str = Form(...)):
    global df
    if df is None:
        raise HTTPException(status_code=400, detail="No data available. Please upload a file first.")
    
    try:
        df[column] = df[column].astype(new_dtype)
        return HTMLResponse(content=f"Changed data type of column {column} to {new_dtype}.", status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/upload")
async def upload(file: UploadFile = File(...), csv_header: bool = Form(False)):
    global df, file_location
    # Save the file
    file_location = f"cache/{file.filename.rsplit('.', 1)[0]}.csv"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    # Read the file into a Dask DataFrame
    try:
        df = dd.read_csv(file_location, header=0 if csv_header else None,
                         na_values=['', 'NA', 'NaN'], keep_default_na=False)
        head = df.head().to_html()
        return HTMLResponse(content=head, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/handle_nan", response_class=HTMLResponse)
async def handle_nan(request: Request, method: str = Form(...), 
                     dropna_how: str = Form(None), fillna_value: str = Form(None)):
    global df
    if df is None:
        raise HTTPException(status_code=400, detail="No data available. Please upload a file first.")
    
    try:
        if method == "dropna":
            how = dropna_how if dropna_how else "any"
            df = df.dropna(how=how)
        elif method == "fillna":
            fill_value = fillna_value if fillna_value else 0
            df = df.fillna(fill_value)
        else:
            raise HTTPException(status_code=400, detail="Invalid method for handling NaN values.")
        
        head = df.head().to_html()
        return head
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
