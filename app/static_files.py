from fastapi.staticfiles import StaticFiles

def setup_static_files(app):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.mount("/css", StaticFiles(directory="app/static/css"), name="static_css")
    app.mount("/images", StaticFiles(directory="app/static/images"), name="static_images")
    app.mount("/js", StaticFiles(directory="app/static/js"), name="static_js")
    app.mount("/downloads", StaticFiles(directory="app/static/downloads"), name="static_downloads")
