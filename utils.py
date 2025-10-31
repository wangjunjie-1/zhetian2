import pyautogui
import time

def enter_info(info: str):
    """输入信息，前后各按一次回车，并加入合理延迟"""
    pyautogui.press('enter')
    time.sleep(0.1)           # 等待输入框准备好（可调）
    pyautogui.typewrite(info, interval=0.05)  # 模拟逐字输入
    time.sleep(0.1)          # 可选：确保文本完全输入
    pyautogui.press('enter')