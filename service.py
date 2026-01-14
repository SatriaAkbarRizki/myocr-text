import uuid
import os
import shutil
from fastapi import UploadFile

class ServiceOperation:
    fileLocation = None
    def __init__(self, files : UploadFile):
        self.files = files

    def usingUniqueNameImage(self):
        fileExtension = os.path.splitext(self.files.filename)[1]
        uniqueFileName = f"{uuid.uuid4()}{fileExtension}"
        self.fileLocation = f"storage/images/{uniqueFileName}"
        return self.fileLocation
    
    def saveImageTempUpload(self):
        with open(self.fileLocation, "wb") as buffer:
            shutil.copyfileobj(self.files.file, buffer)