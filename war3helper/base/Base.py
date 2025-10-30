import logging
import pyautogui
logger = logging.getLogger(__name__)
class Base:
    # 所有单位的基础情况
    def __init__(self):
        self.cur_item  = None # 当前选中的单位
        # 快捷键编队列表
        # 0-9 键对应 0-9 个单位
        self.form_list = [False]*10
        
    def fast_form_select(self,index):
        # 快速选择单位  
        if index < 0 or index > 9:
            logger.error(f'index {index} out of range')
            return
        if self.form_list[index] is None:
            logger.error(f'index {index} is None')
            return
        pyautogui.press(index)
    def fast_form_up(self,index):
        if self.form_list[index] is not False:
            logger.warning(f'index {index} already form')
        # 快速编队
        pyautogui.hotkey('ctrl', index)
        self.form_list[index] = True