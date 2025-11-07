from paddleocr import TextRecognition

class OCR:
    def __init__(self, model_name, model_dir):
        self.model = TextRecognition(model_name=model_name, model_dir=model_dir)
    def predict(self, input, batch_size=1):
        return self.model.predict(input=input, batch_size=batch_size)



    
