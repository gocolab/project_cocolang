from fastapi.staticfiles import StaticFiles

import os
def setup_static_files(app):
    static_css_directory = os.path.join("app", "resources", "css")
    static_images_directory = os.path.join("app", "resources", "images")
    static_js_directory = os.path.join("app", "resources", "js")
    static_downloads_directory = os.path.join("app", "resources", "downloads")

    app.mount("/css", StaticFiles(directory=static_css_directory), name="static_css")
    app.mount("/images", StaticFiles(directory=static_images_directory), name="static_images")
    app.mount("/js", StaticFiles(directory=static_js_directory), name="static_js")
    app.mount("/downloads", StaticFiles(directory=static_downloads_directory), name="static_downloads")