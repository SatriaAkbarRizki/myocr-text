import logging
import uuid
import os
from pathlib import Path
from detecttext import TextOCRMobile
from service import ServiceOperation
from dotenv import load_dotenv, dotenv_values
from fastapi.security import APIKeyHeader
from fastapi import Depends, FastAPI, File, UploadFile, HTTPException


app = FastAPI()
load_dotenv()
header_scheme = APIKeyHeader(name="apiKey")

logger = logging.getLogger("uvicorn.error")
logger.propagate = False


@app.get("/")
def root():

    return {"message" : f"Welcome to api myocr-text"}



@app.post("/files/uploadImage")
def uploadImage(file: UploadFile | None = None, key: str = Depends(header_scheme)):
    if key != os.getenv('APIKEYOCR'):
         raise HTTPException(status_code=401)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="This not file image")
    else:
        objService = ServiceOperation(file)
        fileLocation = objService.usingUniqueNameImage()
        objTextOCR = TextOCRMobile(fileLocation)
        try:

                objService.saveImageTempUpload()
                objTextOCR.doDetectOCR()
                if objTextOCR.responsText == "No have text on image":
                     raise HTTPException(status_code=422, detail= "No Detect Text On Image")
                return {"status" : "success" ,"message" : objTextOCR.responsText}
        except HTTPException as e:
                raise e
        
        except HTTPException as e:
            raise HTTPException(status_code=500, detail= "Error saving image")


 