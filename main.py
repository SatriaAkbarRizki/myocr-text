import logging
import uuid
import os
from pathlib import Path
from detecttext import TextOCRMobile
from service import ServiceOperation
from fastapi import FastAPI, File, UploadFile, HTTPException


app = FastAPI()

logger = logging.getLogger("uvicorn.error")
logger.propagate = False




@app.get("/")
def root():

    return {"message" : f"Welcome to api myocr-text"}



@app.post("/files/uploadImage")
def uploadImage(file: UploadFile | None = None):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="This not file image")
    else:
        objService = ServiceOperation(file)
        fileLocation = objService.usingUniqueNameImage()
        objTextOCR = TextOCRMobile(fileLocation)
        try:

                objService.saveImageTempUpload()
                objTextOCR.doDetectOCR()
                return {"status" : "success" ,"message" : objTextOCR.responsText}
        except:
                raise HTTPException(status_code=500, detail= "Error saving image")


 