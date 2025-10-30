from base.Construct import Construct
import pyautogui
import logging
logger = logging.getLogger(__name__)
class Tower(Construct):
    def __init__(self,name='tower'):
        super().__init__(name)  
    def move_pos(self,Real_pox=None):
        # 后期的移动位置的操作，大概率用不到
        logger.error(f'Tower.move_pos() Not implemented')

