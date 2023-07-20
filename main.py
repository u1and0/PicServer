from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

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
    print(thumbnail_filenames[:10])

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "thumbnail_filenames": thumbnail_filenames[:10],
        })
    # return templates.TemplateResponse("index.html", {"request": request})


@app.get("/date/selected_date", response_class=HTMLResponse)
async def show_selected_date(request: Request, selected_date: str):
    """指定した日付の画像を表示"""
    # image_path = os.path.join(image_directory, selected_date)
    return
