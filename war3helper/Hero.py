from Army import Army
import pyautogui
class Hero(Army):
    def __init__(self,name='hero'):
        super().__init__(name)  
    def step_up(self):
        pyautogui.press('D')
