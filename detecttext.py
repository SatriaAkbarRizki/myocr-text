import cv2
import os

from onnxtr.io import DocumentFile
from onnxtr.models import ocr_predictor, EngineConfig
from onnxruntime.quantization import quantize_dynamic, QuantType

class TextOCRMobile:
    responsText : str = " "

    def __init__(self, pathImage, model = ocr_predictor(

            det_arch='db_mobilenet_v3_large', 
            reco_arch='crnn_mobilenet_v3_small',  
            det_bs=2,
            reco_bs=512,
            assume_straight_pages=True, 
            straighten_pages=False, 
            det_engine_cfg=EngineConfig(),  
            reco_engine_cfg=EngineConfig(),  
            clf_engine_cfg=EngineConfig(), 

        )):
        self.pathImage = pathImage
        self.model = model



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
        cv2.imwrite("storage/images/images_clean.jpg", img, )



    def processOCR(self):
        doc = DocumentFile.from_images(self.pathImage)
        result = self.model(doc)
        self.responsText = result.export()
  
        response_list = []

        for page in self.responsText.get("pages", []):
            for block in page.get("blocks", []):
                for line in block.get("lines", []):
                    for word in line.get("words", []):
                        if len(word["value"])>= 2 and float(word['confidence']) >= 0.60:
                            response_list.append(word['value'])

        # self.saveImageOCR()

        self.responsText = ' '.join(response_list)
        print(self.responsText)
        result.show()


        listRemove = [self.pathImage,"storage/images/images_clean.jpg" ]
        for x in listRemove:
            os.remove(x)

    
    # def saveImageOCR(self):
    #     img = cv2.imread(self.pathImage)
    #     h, w = img.shape[:2]
    #     for page in self.responsText.get("pages", []):
    #         for block in page.get("blocks", []):
    #             for line in block.get("lines", []):
    #                 for word in line.get("words", []):
    #                     if float(word["confidence"]) < 0.6:
    #                         continue

    #                     (x1, y1), (x2, y2) = word["geometry"]

    #                     x1 = int(x1 * w)
    #                     y1 = int(y1 * h)
    #                     x2 = int(x2 * w)
    #                     y2 = int(y2 * h)

    #                     cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

    #     cv2.imwrite("storage/images/ocr_result.jpg", img)


   
        
