from paddleocr import TextRecognition
from utils import enter_info
import numpy as np
from PIL import ImageGrab
gold_area = (174, 990, 1156, 467)
wooden_area = (174, 990, 1120, 307)
mode_area = (174, 990, 1451, 713)

class OCR:
    def __init__(self, model_name, model_dir):
        self.model = TextRecognition(model_name=model_name, model_dir=model_dir)
        self.gold = 0
        self.wooden = 0
        
    def _predict(self, input, batch_size=1):
        return self.model.predict(input=input, batch_size=batch_size)
    def check_gold_wooden(self):

        gold_screenshot = ImageGrab.grab(bbox=gold_area)
        gold_info = self._predict(gold_screenshot)['text']
        
        if gold_info.endswith('万'):
            gold = int(gold_info[:-1]* 10000) 
        elif gold_info.endswith('亿'):
            gold = int(gold_info[:-1]* 100000000) 
        else:
            gold = int(gold_info)

        wooden_screenshot = ImageGrab.grab(bbox=wooden_area)
        wooden_info = self._predict(wooden_screenshot)['text']
        if wooden_info.endswith('万'):
            wooden = int(wooden_info[:-1]* 10000) 
        elif wooden_info.endswith('亿'):
            wooden = int(wooden_info[:-1]* 100000000) 
        else:
            wooden = int(wooden_info)
        self.gold = gold
        self.wooden = wooden
        return gold,wooden




    def select_talent(self):
        enter_info("select talent...")
        enter_info("not implemented yet")
        pass

    def select_hero(self):
        enter_info("select hero...")
        enter_info("not implemented yet")
        pass

    
