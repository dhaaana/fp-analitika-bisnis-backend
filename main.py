import os
from fastapi import FastAPI, Form, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from diagnosis import diagnosis

app = FastAPI()

origins = [
   '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Msg(BaseModel):
    msg: str
    file: UploadFile

# @app.get("/dataset1")
# async def root():
#     diag = diagnosis('cobapng.png')
#     return {"message": diag}

@app.post("/pneumonia")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        diag = diagnosis(file.filename)
        if os.path.exists(file.filename):
            os.remove(file.filename)  
    return {"message": f"Successfully uploaded {file.filename}", "diagnosis": diag}


