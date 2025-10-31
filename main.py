import logging
import time
from mouse import   MouseController
import os,sys

logging.basicConfig(level=logging.DEBUG)
import pyautogui
from pynput import mouse
from pynput import keyboard
DEBUG_MODE = True
running = True

# 防御塔坐标应该是一个列表，避免编队
tower_coord_list=[]

def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        print(f"鼠标左键被按下，当前位置: {pyautogui.position()}")
        
def on_press(key):
    global running
    try:
        # 普通字符键（如 'a', '1', 'Q'）
        if hasattr(key, 'char'):
            char = key.char.lower()
            if char == 'g':
                game_step01()
            elif char == 'x':
                print("收到 'x'，准备退出...")
                running = False
                return False  # 停止键盘监听
    except AttributeError:
        pass
    # 特殊键（如 Esc）——必须放在 try/except 外或单独判断
    if key == keyboard.Key.esc:
        print("收到 ESC，退出程序...")
        running = False
        return False  # 停止当前监听器

def screen_to_form_idx(form_idx):
    """
    将屏幕坐标转换为小地图坐标
    """
    pyautogui.press(str(form_idx))
    time.sleep(0.1)
    pyautogui.hotkey('alt','c')


def game_step01():
    print("开始游戏...")
    # N_pos = [(973,310),(976,157)] # 难度选择位置 常规 N1
    N_pos = [(1141,599)] # 难度选择位置 休闲
    buyer_pos = (954-100,394-100,954+100,394+100) # 鱼竿商人位置
    wall_pos = (175,976,726,379) # 前两个应该是小地图坐标，后两个基于center的rel坐标
    base_pos = (1205,635) # 后两个基于screen的rel坐标,首先应该确定墙的位置
    farm_pos = (300,400,100,200) # 前两个应该是小地图坐标，后两个基于center的rel坐标
    camp_pos = (171,982,1246,458) # 前两个应该是小地图坐标，后两个基于center的rel坐标
    
    # 选择游戏难度
    for N in N_pos:
        time.sleep(2)
        pyautogui.click(*N,duration=0.2)

    # 编队
    time.sleep(1)
    pyautogui.click(54,735,duration=0.5)
    time.sleep(0.5)
    base.fast_form_up(3)
    time.sleep(1)

    
    # 购买鱼竿
    """
    查找鱼竿商人位置,应该是一个固定位置，跳过视觉检测方案。
    """
    screen_to_form_idx(3)
    time.sleep(5)
    mouse_controller.drag_mouse(*buyer_pos)
    time.sleep(1)
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.press('R') 
    time.sleep(1)

    # 选天赋，开自动维修
    time.sleep(3)

    pyautogui.moveTo(1631,951,duration=1)
    time.sleep(0.5)
    pyautogui.click(button='right',duration=0.5)

    time.sleep(3)
    pyautogui.press('D')
    time.sleep(1)
    pyautogui.click(1920/2,1080/3,duration=0.5)
    time.sleep(1)
    
    # 造墙，造基地，造伐木场
    """
    墙和基地用固定位置，跳过视觉检测方案。
    """

    tiny_map_box.move_abl(*wall_pos[:2])
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)  
    pyautogui.click(wall_pos[2],wall_pos[3]+10,duration=0.5,button='right')
    time.sleep(10)  
    farmer01.build_wall(Real_pox=wall_pos[2:])
    time.sleep(5)  
    pyautogui.click(wall_pos[2:],duration=0.5)
    time.sleep(1)  
    base.fast_form_up(1)


    screen_to_form_idx(1)
    time.sleep(1)  
    pyautogui.press(str(3))
    time.sleep(2)  
    farmer01.build_base(base_pos)
    time.sleep(1)  
    pyautogui.click(*base_pos,duration=0.5)
    time.sleep(5)  
    base.fast_form_up(5)
    time.sleep(1)  

    pyautogui.press(str(3))
    tiny_map_box.move_abl(*camp_pos[:2])
    pyautogui.click()
    time.sleep(1)  
    farmer01.build_camp(Real_pox=camp_pos[2:])
    time.sleep(1)  
    pyautogui.click(camp_pos[2:],duration=0.5)
    time.sleep(1)  
    base.fast_form_up(4)


    # base 创建农民
    tiny_map_box.move_abl(*camp_pos[:2])
    pyautogui.click()
    time.sleep(1)  
    pyautogui.press(str(5))
    time.sleep(1)
    pyautogui.click(1179, 495,duration=0.5,button='right')
    for i in range(11):
        pyautogui.press('q')
        time.sleep(1)
    print("结束初始化")


if __name__ == '__main__':


    # 启动监听器
    mouse_listener = mouse.Listener(on_click=on_click)
    kb_listener = keyboard.Listener(on_press=on_press)

    mouse_listener.start()
    kb_listener.start()

    try:
        # 主线程等待，直到 running 为 False
        while running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("用户中断 (Ctrl+C)")
    finally:
        # 停止监听器（优雅关闭）
        mouse_listener.stop()
        kb_listener.stop()
        mouse_listener.join()
        kb_listener.join()
        print("程序已退出")
        sys.exit(0)


  


   
