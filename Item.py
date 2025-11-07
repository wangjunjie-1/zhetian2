import pyautogui
from utils import enter_info
class Item:
    def __init__(self,name,form_idx):
        self.name = name
        self.form_idx = form_idx
        pyautogui.hotkey('ctrl', str(self.form_idx))
        enter_info(f"init from idx {form_idx} item {name}")

    def screen_move2self(self):
        """屏幕移动到元素位置 模拟键盘按下alt+c"""
        pyautogui.hotkey('alt', 'c')  # 按下 Alt+C
    def _select(self):
        """选择元素 模拟键盘按下alt+c"""
        pyautogui.press(str(self.form_idx))
        enter_info(f"select item {self.name} from idx {self.form_idx}")
    def _seclect_2_center(self):
        """选择元素并移动到屏幕中心"""
        self._select()
        self.screen_move2self()
    