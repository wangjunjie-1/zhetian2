import time
from paddleocr import TextRecognition
from utils import enter_info
import numpy as np
from PIL import ImageGrab

gold_area = (1000, 0, 1300, 100)
wooden_area = (1300, 0, 1500, 100)
mode_area = (1104, 2, 1290, 30)

class OCR:
    def __init__(self, model_name, model_dir):
        self.model = TextRecognition(model_name=model_name, model_dir=model_dir)
        self.gold = 0
        self.wooden = 0
        
    def _predict(self, input, batch_size=1):
        return self.model.predict(input=input, batch_size=batch_size)
    def check_gold_wooden(self):
        gold_info = ""
        wooden_info = ""
        while gold_info=="":
            time.sleep(1)
            screenshot = ImageGrab.grab(include_layered_windows=True, all_screens=True)
            screenshot.save('screenshot.png')
            gold_screenshot = screenshot.crop(gold_area)
            gold_screenshot.save('gold.png')
            wooden_screenshot = screenshot.crop(wooden_area)
            wooden_screenshot.save('wooden.png')
            # return 
            gold_info = self._predict(np.array(gold_screenshot))[0]['rec_text']

                
            print(gold_info)
            enter_info(gold_info)
            if gold_info=="":
                continue
            if gold_info.endswith('万'):
                gold = int(gold_info[:-1]* 10000) 
            elif gold_info.endswith('亿'):
                gold = int(gold_info[:-1]* 100000000) 
            else:
                gold = int(gold)

        while wooden_info=="":
            time.sleep(1)
            wooden_screenshot = ImageGrab.grab(bbox=wooden_area)
            wooden_screenshot.save('wooden.png')
            wooden_info = self._predict(np.array(wooden_screenshot))[0]['rec_text']
            print(wooden_info)
            enter_info(wooden_info)
            if wooden_info=="":
                continue
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

    
