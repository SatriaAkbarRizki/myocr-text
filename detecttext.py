import cv2
import os

from onnxtr.io import DocumentFile
from onnxtr.models import ocr_predictor, EngineConfig
from onnxruntime.quantization import quantize_dynamic, QuantType


model = ocr_predictor(

            det_arch='db_mobilenet_v3_large', 
            reco_arch='crnn_mobilenet_v3_small',  
            det_bs=2,
            detect_language=True,
            reco_bs=512,
            assume_straight_pages=True, 
            straighten_pages=False, 
            det_engine_cfg=EngineConfig(),  
            reco_engine_cfg=EngineConfig(),  
            clf_engine_cfg=EngineConfig(), 

        )

class TextOCRMobile:
    responsText : str = " "

    def __init__(self, pathImage):
        self.pathImage = pathImage




    def doDetectOCR(self):
        try:
            self.convertImagetoCV()
            self.processOCR()
        except NameError:
            print(NameError)
        except:
            print("Error processing ocr")


    def convertImagetoCV(self):
        img = cv2.imread(self.pathImage)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(self.pathImage, img, )



    def processOCR(self):
        doc = DocumentFile.from_images(self.pathImage)
        result = model(doc)
        self.responsText = result.export()
  
        response_list = []

        for page in self.responsText.get("pages", []):
            for block in page.get("blocks", []):
                for line in block.get("lines", []):
                    for word in line.get("words", []):
                        if len(word["value"])>= 2 and float(word['confidence']) >= 0.60:
                            response_list.append(word['value'])

 

        self.responsText = ' '.join(response_list)


        listRemove = [self.pathImage ]
        for x in listRemove:
            os.remove(x)


   
        
