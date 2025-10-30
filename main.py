import logging
from war3helper.base.Base import Base 
from war3helper.base.TinyMapBox import TinyMapBox
import time

from war3helper.farm.farmer import Farmer01
logging.basicConfig(level=logging.DEBUG)
import pyautogui
DEBUG_MODE = True

base = Base()
tiny_map_box = TinyMapBox()
farmer01 = Farmer01()

def game_step01():
    N_pos = (100,100) # 难度选择位置
    buyer_pos = (100,200) # 鱼竿商人位置
    wall_pos = (300,400,100,200) # 前两个应该是小地图坐标，后两个基于center的rel坐标
    base_pos = (300,400,100,200) # 前两个应该是小地图坐标，后两个基于center的rel坐标
    farm_pos = (300,400,100,200) # 前两个应该是小地图坐标，后两个基于center的rel坐标
    camp_pos = (300,400,100,200) # 前两个应该是小地图坐标，后两个基于center的rel坐标
    # 选择游戏难度
    pyautogui.click(*N_pos,duration=0.5)
    if DEBUG_MODE:
        time.sleep(1)

    # 购买鱼竿
    """
    查找鱼竿商人位置,应该是一个固定位置，跳过视觉检测方案。
    """
    
    pyautogui.click(*buyer_pos,duration=0.5)
    if DEBUG_MODE:
        time.sleep(1)
    pyautogui.press('?') # 高级鱼竿快捷键？
    if DEBUG_MODE:
        time.sleep(1)
    
    # 编队，造墙，造基地，造伐木场
    """
    墙和基地用固定位置，跳过视觉检测方案。
    """
    base.fast_form_up(3)
    if DEBUG_MODE:
        time.sleep(1)

    tiny_map_box.move_abl(*wall_pos[:2])
    if DEBUG_MODE:
        time.sleep(1)    
    farmer01.build_wall(Real_pox=wall_pos[2:])
    if DEBUG_MODE:
        time.sleep(1)  
    pyautogui.click(wall_pos[2:],duration=0.5)
    if DEBUG_MODE:
        time.sleep(1)  
    base.fast_form_up(1)
    if DEBUG_MODE:
        time.sleep(1)  
    
    tiny_map_box.move_abl(*base_pos[:2])
    if DEBUG_MODE:
        time.sleep(1)  
    farmer01.build_base(Real_pox=base_pos[2:])
    if DEBUG_MODE:
        time.sleep(1)  
    pyautogui.click(base_pos[2:],duration=0.5)
    if DEBUG_MODE:
        time.sleep(1)  
    base.fast_form_up(5)
    if DEBUG_MODE:
        time.sleep(1)  

    tiny_map_box.move_abl(*camp_pos[:2])
    if DEBUG_MODE:
        time.sleep(1)  
    farmer01.build_camp(Real_pox=camp_pos[2:])
    if DEBUG_MODE:
        time.sleep(1)  
    pyautogui.click(camp_pos[2:],duration=0.5)
    if DEBUG_MODE:
        time.sleep(1)  
    base.fast_form_up(4)


    # base 创建农民
    
    


if __name__ == '__main__':
    start_time = time.time()
    
    for i in range(10):
        logging.info(f'{10-i}s ')
        time.sleep(1)
  
    while True:
        game_step01()


   
