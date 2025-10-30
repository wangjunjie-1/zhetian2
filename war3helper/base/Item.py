import pyautogui
# 可以操作的一切都应该集成元素基类
import logging
logger = logging.getLogger(__name__)

class Item:
    def __init__(self,name):
        self.name = name
        self.screen_box_pos = (0,0)

    def screen_move2self(self):
        """屏幕移动到元素位置 模拟键盘按下alt+c"""
        pyautogui.hotkey('alt', 'c')  # 按下 Alt+C

    def move_rel(self,width,height):
        # 相对移动
        self.screen_box_pos = (self.screen_box_pos[0]+width,self.screen_box_pos[1]+height)
        self._move(self.screen_box_pos[0],self.screen_box_pos[1])
    def move_abl(self,x,y):
        # 移动到绝对位置
        self.screen_box_pos = (x,y)
        self._move(self.screen_box_pos[0],self.screen_box_pos[1])
    def _move(self,x,y):
        # 移动到元素位置
        pyautogui.moveTo(x,y)
        logger.info(f'{self.name} move to {x},{y}')
