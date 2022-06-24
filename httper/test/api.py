from typing import List

from fastapi import FastAPI ,File,UploadFile
from pydantic import BaseModel

app = FastAPI()

class PostBody(BaseModel):
    a: str
    b: str

@app.get("/get")
def get(a : int):
    return f"hello:{a}"

@app.post("/post")
def post(a : int):
    return f"hello:{a}"

@app.post("/postjson")
def postjson(body : PostBody):
    return body

@app.post("/upload1")
def upload1(file : UploadFile = File(...)):
    print(file.filename)
    return {"file_size": 0}

@app.post("/upload2")
def upload2(files : List[UploadFile] = File(...)):
    return {"file_size": 0}

@app.post("/upload3")
def upload3(file : bytes = File(...)):
    return {"file_size": len(file)}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080)