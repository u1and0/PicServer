""" 画像ファイルを日付別に配信します。
Usage:
    $ uvicorn main:app --port 8888 --host 0.0.0.0
"""
import os
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
# テンプレートhtmlファイルの場所
templates = Jinja2Templates(directory="templates")
# 画像ファイル置き場は必ずroot以下に設置する
image_directory = "static"
app.mount("/static", StaticFiles(directory=image_directory), name="static")


@app.get("/")
async def root():
    """/indexへリダイレクト"""
    return RedirectResponse("/index")


@app.get("/index", response_class=HTMLResponse)
async def read_root(request: Request):
    """最新の画像ファイルを表示"""
    thumbnail_filenames = [
        os.path.join(image_directory, filename)
        for filename in os.listdir(image_directory)
        if filename.endswith(".jpg")
    ]
    print(thumbnail_filenames[-10:])
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "thumbnail_filenames": thumbnail_filenames[-10:],
        })


@app.get("/{date}", response_class=HTMLResponse)
async def show_selected_date(request: Request, date: str):
    """指定した日付の画像を表示"""
    dt = datetime.strptime(date, "%Y-%m-%d").strftime("%y%m%d")
    thumbnail_filenames = [
        os.path.join(image_directory, filename)
        for filename in os.listdir(image_directory)
        if filename.startswith(dt) and filename.endswith(".jpg")
    ]
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "thumbnail_filenames": thumbnail_filenames,
        })
