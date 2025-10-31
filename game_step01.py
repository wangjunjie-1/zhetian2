import time
import pyautogui
from mouse import MouseController
from Item import Item
import logging
import sys
from pynput import mouse, keyboard
from typing import List
from utils import enter_info
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    )
from coordinate import *

mouse_controller = MouseController()
N_pos_list = [(1141, 599)]  # 难度选择位置 休闲
# N_pos = [(973,310),(976,157)] # 难度选择位置 常规 N1
camp_pos_list = [(171, 982, 1246, 458)]
tree_aim_list = [(500, 600, 200, 300)]



tower_list = []

wall_pos = (175, 976, 726, 379)  # 前两个应该是小地图坐标，后两个基于center的rel坐标
camp_pos = (171, 982, 1246, 458)  # 前两个应该是小地图坐标，后两个基于center的rel坐标
base_pos = (1205, 635)  # 后两个基于screen的rel坐标,首先应该确定墙的位置
farm_pos = (300, 400, 100, 200)  # 前两个应该是小地图坐标，后两个基于center的rel坐标
research_pos = (500, 600, 200, 300)  # 前两个应该是小地图坐标，后两个基于center的rel坐标
hero_pos = (400, 500, 300, 400)  # 前两个应该是小地图坐标，后两个基于center的rel坐标
running = True
# 防御塔坐标应该是一个列表，避免编队
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
    pyautogui.press([str(builder_idx), "B", str(construct_idx)], interval=0.25)
    mouse_controller.left_click(box_list[2], box_list[3])

def build_army(builder_idx, army_idx, box_list: List):
    if len(box_list) != 4:
        raise ValueError(
            "box_list must contain exactly 4 elements: [map_x, map_y, real_x, real_y]"
        )
    mouse_controller.map_coordinate_move(
        box_list[0], box_list[1], box_list[2], box_list[3]
    )
    pyautogui.press([str(builder_idx), str(army_idx)], interval=0.25)
    mouse_controller.right_click(box_list[2], box_list[3])

def game_step01():
    enter_info("game start...")

    buyer_pos = (954 - 100, 394 - 100, 954 + 100, 394 + 100)  # 鱼竿商人位置

    wall_pos = (175, 976, 726, 379)  # 前两个应该是小地图坐标，后两个基于center的rel坐标
    camp_pos = (
        171,
        982,
        1246,
        458,
    )  # 前两个应该是小地图坐标，后两个基于center的rel坐标
    base_pos = (1205, 635)  # 后两个基于screen的rel坐标,首先应该确定墙的位置
    farm_pos = (300, 400, 100, 200)  # 前两个应该是小地图坐标，后两个基于center的rel坐标
    research_pos = (
        500,
        600,
        200,
        300,
    )  # 前两个应该是小地图坐标，后两个基于center的rel坐标

    # 选择游戏难度
    for N in N_pos_list:
        mouse_controller.left_click(*N)

    # 编队
    time.sleep(1)
    mouse_controller.left_click(54, 735)
    time.sleep(0.5)
    famer01 = Item("famer01", farmer01_idx)
    time.sleep(1)

    # 购买鱼竿
    """
    查找鱼竿商人位置,应该是一个固定位置，跳过视觉检测方案。
    """
    time.sleep(5)
    mouse_controller.drag_mouse(*buyer_pos)
    time.sleep(1)
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.press("R")
    time.sleep(1)

    # 选天赋，开自动维修
    famer01._seclect_2_center()
    mouse_controller.right_click(1631, 951)
    pyautogui.press("D")
    mouse_controller.left_click(1920 // 2, 1080 // 3)

    # 造墙，造基地，造伐木场
    """
    墙和基地用固定位置，跳过视觉检测方案。
    """
    build_construct(builder_idx=farmer01_idx, construct_idx="Q", box_list=wall_pos)
    mouse_controller.left_click(wall_pos[2], wall_pos[3])
    wall = Item("wall", wall_idx)

    build_construct(builder_idx=farmer01_idx, construct_idx="A", box_list=base_pos)
    mouse_controller.left_click(base_pos[2], base_pos[3])
    base = Item("base", base_idx)

    camp_pos = camp_pos_list[0]
    build_construct(builder_idx=farmer01_idx, construct_idx="S", box_list=camp_pos)
    mouse_controller.left_click(camp_pos[2], camp_pos[3])
    camp = Item("camp", camp_idx)

    build_construct(builder_idx=farmer01_idx, construct_idx="v", box_list=research_pos)
    mouse_controller.left_click(research_pos[2], research_pos[3])
    research = Item("research", research_idx)

    build_construct(builder_idx=farmer01_idx, construct_idx="f", box_list=farm_pos)
    mouse_controller.left_click(farm_pos[2], farm_pos[3])
    farm = Item("farm", farm_idx)

    # base 创建农民
    for i in range(5):
        time.sleep(1)
        build_army(builder_idx=base_idx, army_idx="Q", box_list=tree_aim_list[0])
    for i in range(3):
        time.sleep(1)
        build_army(builder_idx=base_idx, army_idx="Q", box_list=tree_aim_list[0])
    for i in range(3):
        time.sleep(1)
        build_army(builder_idx=base_idx, army_idx="Q", box_list=tree_aim_list[0])

def game_step02():
    enter_info("game step02...")
    # 造防御塔
    for tower_coord in tower_coord_list:
        build_construct(
            builder_idx=farmer01_idx, construct_idx="Q", box_list=tower_coord
        )
        mouse_controller.left_click(tower_coord[2], tower_coord[3])
        time.sleep(10)
    # 研究科技
    for i in range(200):
        time.sleep(1)
        pyautogui.press("R")
        
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
