import os
import shutil
from io import BytesIO
import requests
import zipfile

UI_URL = "https://github.com/swagger-api/swagger-ui/archive/master.zip"
BUILD_PATH = "_build"
DIST_PATH = os.path.join("flask_transmute", "swagger-ui")


def main(uranium):
    if os.path.exists(DIST_PATH):
        shutil.rmtree(DIST_PATH)
    response = requests.get(UI_URL, stream=True)
    zip_file = zipfile.ZipFile(BytesIO(response.content))
    for name in zip_file.namelist():
        if os.path.join("swagger-ui-master", "dist") in name:
            zip_file.extract(name, BUILD_PATH)
    source_path = os.path.join(BUILD_PATH, "swagger-ui-master", "dist")
    shutil.move(source_path, DIST_PATH)
