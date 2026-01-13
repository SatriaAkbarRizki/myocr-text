import logging

from pathlib import Path
from detecttext import TextOCRMobile
from fastapi import FastAPI, File, UploadFile
import shutil

app = FastAPI()

logger = logging.getLogger("uvicorn.error")
logger.propagate = False



@app.get("/")
def root():
    return {"message" : "Welcome to api myocr-text"}



@app.post("/files/uploadImage")
async def uploadImage(file: UploadFile | None = None):
    if not file.content_type.startswith("image/"):
        return {"message" : "This not file image"}
    else:
        fileLocation = f"storage/images/{file.filename}"
        try:
            with open(fileLocation, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                return {"message" : f"Succes upload image: {file.filename}"}
        except:
                return {"message" : "Error saving image"}
       





# Only Testing
@app.get("/product/{product_id}")
async def getProduct(product_id: int):
    return {"message": f"You get specific product with id {product_id}"}




# Here OCR Operation 
# objTextOCR = TextOCRMobile("storage/images/test copy.png")
# objTextOCR.doDetectOCR()


 