import time
import pyautogui
from mouse import MouseController
from Item import Item
import logging
import sys
from pynput import mouse, keyboard
from typing import List
from utils import enter_info, form_item
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    )
from coordinate import *
game_01_flag = False
game_02_flag = False

mouse_controller = MouseController()
N_pos_list = [(990, 591)]  # 难度选择位置 休闲
# N_pos = [(973,310),(976,157)] # 难度选择位置 常规 N1
camp_pos_list = [(171, 982, 1246, 458)]
tree_aim_list = [(178, 987, 738, 356)]


hero_tower_pos =(174, 990,1068,528)

wall_pos =       (174, 990, 1156, 467)  
base_pos =       (174, 990, 1120, 307)  
first_camp_pos = (174, 990, 1451, 713)  

farm_pos =     (175,958, 500, 562)  
research_pos = (175,958, 563, 562) 
hero_pos = (400, 500, 300, 400)  
running = True

tower_coord_list = []

def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        print(f"鼠标左键被按下，当前位置: {pyautogui.position()}")

def on_press(key):
    global running
    try:
        # 普通字符键（如 'a', '1', 'Q'）
        if hasattr(key, "char"):
            char = key.char.lower()
            if char == "g":
                game_step01()
            if char == "h":
                game_step02()
            if char == "j":
                hero_start()
            if char == "t":
                logging.error(f"{time.time()}")
            elif char == "x":
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

def killer(key):
    try:
        # 检查是否按下了字母 'k'（区分大小写，但 char 会反映实际按键）
        if hasattr(key, 'char') and key.char in ('k', 'K'):
            print("K pressed! Killing main process...")
            # 强制终止当前进程
            os.kill(os.getpid(), signal.SIGTERM)
            # 或者在 Windows 上也可以用 os._exit(1) 立即退出（不推荐用于生产）
    except Exception as e:
        pass  # 忽略异常（如特殊键）

def build_construct(builder_idx, construct_idx, box_list: List):
    """通用建筑函数
    Args:
        builder_idx: 建筑工类型索引
        construct_idx: 建筑类型索引
        Real_pox: 真实坐标位置
    """
    if len(box_list) != 4:
        raise ValueError(
            "box_list must contain exactly 4 elements: [map_x, map_y, real_x, real_y]"
        )
    mouse_controller.map_coordinate_move(
        box_list[0], box_list[1], box_list[2], box_list[3]
    )
    pyautogui.press(str(builder_idx))
    pyautogui.press("B")
    pyautogui.press(str(construct_idx))
    mouse_controller.left_click(box_list[2], box_list[3])

def build_army(builder_idx, army_idx, box_list: List,time:int=1):
    if len(box_list) != 4:
        raise ValueError(
            "box_list must contain exactly 4 elements: [map_x, map_y, real_x, real_y]"
        )
    mouse_controller.map_coordinate_move(
        box_list[0], box_list[1], box_list[2], box_list[3]
    )
    pyautogui.press(str(builder_idx))
    for i in range(time):
        pyautogui.press(str(army_idx))
    mouse_controller.right_click(box_list[2], box_list[3])

def game_step01():
    global game_01_flag
    if game_01_flag:
        enter_info("game01 pass")
        return
    game_01_flag = True
    # enter_info("game start...")

    buyer_pos = (897,337,1029,483)  # 鱼竿商人位置

    # 选择游戏难度
    for N in N_pos_list:
        mouse_controller.left_click(*N)

    # 编队
    time.sleep(1)
    mouse_controller.left_click(63, 730)
    time.sleep(0.5)
    form_item(farmer01_idx,"famer01")
    time.sleep(1)

    # 购买鱼竿
    """
    查找鱼竿商人位置,应该是一个固定位置，跳过视觉检测方案。
    """
    time.sleep(1)
    mouse_controller.drag_mouse(*buyer_pos)
    time.sleep(1)
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.press("R")
    time.sleep(1)

    # 选天赋，开自动维修
    screen_move2self(farmer01_idx)
    mouse_controller.right_click(1638, 941)
    pyautogui.press("D")
    mouse_controller.left_click(1920 // 2, 1080 // 3)
     


    # 造墙，造基地，造伐木场
    """
    墙和基地用固定位置，跳过视觉检测方案。
    """
    build_construct(builder_idx=farmer01_idx, construct_idx="Q", box_list=wall_pos)
    mouse_controller.left_click(wall_pos[2], wall_pos[3])
    time.sleep(30)
    mouse_controller.left_click(wall_pos[2]-15, wall_pos[3]-15)
    form_item(wall_idx,"wall")

   

    build_construct(builder_idx=farmer01_idx, construct_idx="A", box_list=base_pos)
    mouse_controller.left_click(base_pos[2], base_pos[3])
    time.sleep(10)
    mouse_controller.left_click(base_pos[2]-15, base_pos[3]-15)
    form_item(base_idx,"base")
     

    camp_pos = first_camp_pos
    build_construct(builder_idx=farmer01_idx, construct_idx="S", box_list=camp_pos)
    mouse_controller.left_click(camp_pos[2], camp_pos[3])
    time.sleep(10)
    mouse_controller.left_click(camp_pos[2]-15, camp_pos[3]-15)
    form_item(camp_idx,"camp")
    

    build_construct(builder_idx=farmer01_idx, construct_idx="v", box_list=research_pos)
    mouse_controller.left_click(research_pos[2], research_pos[3])
    time.sleep(10)
    mouse_controller.left_click(research_pos[2]-15, research_pos[3]-15)
    form_item(research_idx,"research")
   
    build_construct(builder_idx=farmer01_idx, construct_idx="f", box_list=farm_pos)
    mouse_controller.left_click(farm_pos[2], farm_pos[3])
    time.sleep(10)
    mouse_controller.left_click(farm_pos[2]-15, farm_pos[3]-15)
    form_item(farm_idx,"farm")

    # base 创建农民

    build_army(builder_idx=base_idx, army_idx="Q", box_list=tree_aim_list[0],time=6)
    time.sleep(5)
    build_army(builder_idx=base_idx, army_idx="Q", box_list=tree_aim_list[0],time=3)
    time.sleep(5)
    build_army(builder_idx=base_idx, army_idx="Q", box_list=tree_aim_list[0],time=3)
    enter_info("game01 end")
     

    global game_02_flag
    if game_02_flag:
        enter_info("step02 pass")
        return
    game_02_flag = True
    enter_info("step02...")

    
    pyautogui.press(str(camp_idx))
    # 研究科技
    for i in range(4):
        time.sleep(1)
        pyautogui.press("R")

        pyautogui.press(str(camp_idx))

    # 研究科技
    for i in range(11):
        time.sleep(3)
        pyautogui.press("Q")
    # 成长塔
    time.sleep(30)
    build_construct(builder_idx=farmer01_idx, construct_idx="D", box_list=hero_tower_pos)
    time.sleep(30)
    mouse_controller.left_click(hero_tower_pos[2]-15, hero_tower_pos[3]-15)
    # 研究科技
    for i in range(11):
        time.sleep(10)
        pyautogui.press("Q")
        
def hero_box_train(box_info):
    build_idx = box_info['build_idx']
    box_idx = box_info['box_idx']
    boss_pos = box_info['boss_pos']
    pyautogui.press([str(build_idx), str(box_idx)], interval=0.25)
    pyautogui.press(["F1","F1"],interval=0.05)
    mouse_controller.map_coordinate_move(
        boss_pos[0], boss_pos[1], boss_pos[2], boss_pos[3]
    )
    mouse_controller.right_click(boss_pos[2], boss_pos[3])
    pyautogui.press(["D","A"],interval=0.1)

def hero_start():
    enter_info("hero process...")
    build_construct(farmer01_idx, "A", hero_pos)
    time.sleep(2)
    mouse_controller.left_click(hero_pos[2], hero_pos[3])
    pyautogui.press("Q")
    # 这里应该使用视觉方案，但是暂时也先试用随机吧。
    mouse_controller.left_click(1920 // 2, 1080 // 3)

def tower_update():
    enter_info("tower update...")
    for tower_coord in tower_coord_list:
        mouse_controller.map_coordinate_move(
            tower_coord[0], tower_coord[1], tower_coord[2], tower_coord[3]
        )
        mouse_controller.left_click(tower_coord[2], tower_coord[3])
        time.sleep(1)
        # 好像只能按键升级，默认是眩晕塔
        pyautogui.press("Q")
        
        time.sleep(1)

if __name__ == "__main__":
    # 启动监听器
    mouse_listener = mouse.Listener(on_click=on_click)
    kb_listener = keyboard.Listener(on_press=on_press)
    killer_listener = keyboard.Listener(on_press=killer)
    killer_listener.start()
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
