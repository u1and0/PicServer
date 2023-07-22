""" 画像ファイルを日付別に配信します。
Usage:
    $ uvicorn main:app --port 8888 --host 0.0.0.0
"""
import os
from itertools import islice
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
    """最新の画像ファイル10件を表示"""
    thumbnail_filenames = sorted(
        (os.path.join(image_directory, i)
         for i in os.listdir(image_directory) if i.endswith(".jpg")),
        reverse=True)[:10]
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "thumbnail_filenames": thumbnail_filenames
        })


@app.get("/{date}", response_class=HTMLResponse)
async def show_selected_date(request: Request, date: str):
    """指定した日付の画像を表示"""
    thumbnail_filenames = sorted([
        os.path.join(image_directory, filename)
        for filename in os.listdir(image_directory)
        if filename.startswith(date) and filename.endswith(".jpg")
    ])

    # 最初の1個で走査を終了するならlistdir()よりscandir()の方が20%速い
    #
    # In [24]: %timeit list(islice((i.name for i in os.scandir(image_dir) if i.name.
    #     ...: startswith("230720") and i.name.endswith(".jpg")), 1))
    # 5.93 ms ± 475 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    #
    # In [25]: %timeit list(islice((i for i in os.listdir(image_dir) if i.startswith
    #     ...: ("230720") and i.endswith(".jpg")) , 1))
    # 7.4 ms ± 305 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

    # 最初に見つけたgifファイルを返す
    gif_filename = list(
        islice((i.name for i in os.scandir(image_directory)
                if i.name.startswith(date) and i.name.endswith(".gif")), 1))[0]
    gif_filename = os.path.join(image_directory, gif_filename)
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "gif_filenames": gif_filename,
            "thumbnail_filenames": thumbnail_filenames,
            "date": f"20{date[:2]}-{date[2:4]}-{date[-2:]}",
        })
