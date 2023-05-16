from typing import List
import uvicorn
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from typing_extensions import Annotated
import requests

app = FastAPI(debug=True)

@app.post("/upload/")
def create_file(data: dict):

    file_path = f"dir2/{data['name']}"
    
    with open(file_path, "wb") as f:
        contents = data['data'].encode("utf-8")
        f.write(contents)

    files = []
    directory = 'dir2'
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)
    return {"files": files}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)