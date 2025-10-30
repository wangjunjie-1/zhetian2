import pyautogui
from war3helper.base.Army import Army
class Farmer(Army):
    def __init__(self,name='farmer'):
        super().__init__(name)  

    def build(self,construct_idx = 'F',Real_pox=None):
        pyautogui.press('B')
        # 选择建筑
        pyautogui.press(construct_idx)
        if Real_pox is not None:
            self.move_rel(*Real_pox)
        # 确认建筑
        pyautogui.click(duration=0.5)

class Farmer01(Farmer):
    def __init__(self,name='farmer01'):
        super().__init__(name)  
    def build_wall(self,Real_pox=None):
        self.build(construct_idx='Q',Real_pox=Real_pox)
    def build_base(self,Real_pox=None):
        self.build(construct_idx='A',Real_pox=Real_pox)
    def build_farm(self,Real_pox=None):
        self.build(construct_idx='F',Real_pox=Real_pox)
    def build_reacher(self,Real_pox=None):
        self.build(construct_idx='V',Real_pox=Real_pox)
    def build_hero(self,Real_pox=None):
        self.build(construct_idx='A',Real_pox=Real_pox)
    def build_camp(self,Real_pox=None):
        self.build(construct_idx='S',Real_pox=Real_pox)

class Farmer02(Farmer):
    def __init__(self,name='farmer02'):
        super().__init__(name)  

