#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
鼠标操作模块
提供魔兽争霸3游戏中的鼠标模拟操作
"""

import time
import random
import pyautogui
from typing import Optional, Tuple, List





from pynput import mouse
import time

def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        print(f"鼠标左键被按下，当前位置: {pyautogui.position()}")




class MouseController:
    """
    鼠标控制器类
    实现游戏中的鼠标操作
    """
    
    def __init__(self):
        """初始化鼠标控制器"""

        
        # 配置pyautogui安全设置
        pyautogui.FAILSAFE = True  # 启用故障安全（移动到屏幕左上角可中断操作）
        pyautogui.PAUSE = 0.01     # 每个操作间的延迟
        
        # 屏幕边缘区域定义（用于滚动屏幕）
        self.screen_width = pyautogui.size()[0]
        self.screen_height = pyautogui.size()[1]
        self.edge_margin = 10  # 边缘区域宽度
        
        # 操作延迟范围（增加随机性，避免被检测）
        self.click_delay_range = (0.05, 0.15)
        self.move_delay_range = (0.02, 0.08)
        self.drag_delay_range = (0.1, 0.3)

    def _cal_duration(self, x:int,y:int) -> float:
        cur_x, cur_y = pyautogui.position()
        distance = ((x - cur_x) ** 2 + (y - cur_y) ** 2) ** 0.5
        distance_factor = 0.002  # 每个像素的时间因子，可调节
        base_duration = distance * distance_factor
        # 添加随机波动
        random_variation = random.uniform(-0.05, 0.05)
        duration = max(0.1, base_duration + random_variation)
        return duration
    
    def move_mouse(self, x: int, y: int) -> None:
        """
        移动鼠标到指定坐标
        
        Args:
            x: 目标X坐标
            y: 目标Y坐标
            duration: 移动持续时间，如果为None则使用随机延迟
        """        
        pyautogui.moveTo(x, y, duration=self._cal_duration(x,y))
        time.sleep(random.uniform(*self.click_delay_range) / 2)
    
    def left_click(self, x: Optional[int] = None, y: Optional[int] = None, 
                  clicks: int = 1) -> None:
        """
        左键点击
        
        Args:
            x: 点击X坐标，为None则在当前位置点击
            y: 点击Y坐标，为None则在当前位置点击
            clicks: 点击次数
            duration: 点击持续时间
        """
        if x is not None and y is not None:
            self.move_mouse(x, y)   
        
        pyautogui.click(button='left', clicks=clicks)
        time.sleep(random.uniform(*self.click_delay_range))
    
    def right_click(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """
        右键点击
        
        Args:
            x: 点击X坐标，为None则在当前位置点击
            y: 点击Y坐标，为None则在当前位置点击
            duration: 点击持续时间
        """
        if x is not None and y is not None:
            self.move_mouse(x, y)
        
        pyautogui.click(button='right')
        time.sleep(random.uniform(*self.click_delay_range))
            
    def drag_mouse(self, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        """
        拖拽鼠标
        
        Args:
            start_x: 起始X坐标
            start_y: 起始Y坐标
            end_x: 结束X坐标
            end_y: 结束Y坐标
            duration: 拖拽持续时间
        """
        if duration is None:
            duration = random.uniform(*self.drag_delay_range)
        
        # 先移动到起始位置
        self.move_mouse(start_x, start_y)
        
        # 执行拖拽
        pyautogui.dragTo(end_x, end_y, duration=self._cal_duration(end_x,end_y), button='left')
        time.sleep(random.uniform(*self.click_delay_range))
    
    def scroll_screen_edge(self, direction: str, duration: float = 0.5) -> None:
        """
        将鼠标放置在屏幕边缘来滚动视角
        
        Args:
            direction: 滚动方向 ('up', 'down', 'left', 'right')
            duration: 鼠标停留在边缘的时间
        """
        # 边缘坐标
        edge_positions = {

            'up': (self.screen_width // 2, self.edge_margin // 2),
            'down': (self.screen_width // 2, self.screen_height - self.edge_margin // 2),
            'left': (self.edge_margin // 2, self.screen_height // 2),
            'right': (self.screen_width - self.edge_margin // 2, self.screen_height // 2),

            'up_right': (self.screen_width - self.edge_margin // 2, self.edge_margin // 2),
            'up_left': (self.edge_margin // 2, self.edge_margin // 2),
            'down_right': (self.screen_width - self.edge_margin // 2, self.screen_height - self.edge_margin // 2),
            'down_left': (self.edge_margin // 2, self.screen_height - self.edge_margin // 2),
        }
        
        if direction in edge_positions:
            x, y = edge_positions[direction]
            
            # 移动到边缘
            self.move_mouse(x, y)
            
            # 停留一段时间以滚动屏幕
            time.sleep(duration)
            
            # 回到屏幕中央附近
            self.move_mouse(self.screen_width // 2, self.screen_height // 2)
    
    def is_mouse_at_edge(self) -> Tuple[bool, Optional[str]]:
        """
        检查鼠标是否在屏幕边缘
        
        Returns:
            (是否在边缘, 边缘方向或None)
        """
        x, y = pyautogui.position()
        
        if x <= self.edge_margin:
            return True, 'left'
        elif x >= self.screen_width - self.edge_margin:
            return True, 'right'
        elif y <= self.edge_margin:
            return True, 'up'
        elif y >= self.screen_height - self.edge_margin:
            return True, 'down'
        
        return False, None
    
    def map_coordinate_move(self,x1,y1,x2,y2):
        """小地图坐标移动"""
        self.left_click(x1,y1)
        self.move_mouse(x2,y2)



# 测试函数
def test_mouse_functions():
    """测试鼠标功能"""
    print("开始测试鼠标功能...")
    # 启动监听器（不阻塞）
    listener = mouse.Listener(on_click=on_click)
    listener.start()  # 启动后台线程
    controller = MouseController()
    
    # 等待用户准备
    print("3秒后开始测试...")
    time.sleep(3)
    
    center_x,center_y = controller.screen_width/2,controller.screen_height/2

    # 测试选择单位
    # print("测试选择单位...")
    # center_x, center_y = pyautogui.size()[0] // 2, pyautogui.size()[1] // 2
    # controller.select_unit(center_x, center_y)
    
    # 测试移动

    # print("测试右键移动...")
    # controller.move_to_position(center_x-200 , center_y)
    # time.sleep(3)
    # controller.move_to_position(center_x+200 , center_y)
    # time.sleep(3)
    # controller.move_to_position(center_x , center_y+200)
    # time.sleep(3)
    # controller.move_to_position(center_x , center_y-200)

    
    # 测试屏幕滚动
    # print("测试屏幕滚动...")
    # controller.scroll_screen_edge('right', 2)
    # time.sleep(3)
    # controller.scroll_screen_edge('left', 2)
    # time.sleep(3)
    # controller.scroll_screen_edge('up', 2)
    # time.sleep(3)
    # controller.scroll_screen_edge('down', 2)
    # time.sleep(3)
    # controller.scroll_screen_edge('up_right', 2)
    # time.sleep(3)
    # controller.scroll_screen_edge('down_right', 2)
    # time.sleep(3)
    # controller.scroll_screen_edge('down_left', 2)
    # time.sleep(3)
    # controller.scroll_screen_edge('up_left', 2) 
    # time.sleep(3)

    # 测试框选
    print("测试框选...")
    controller.box_select(center_x-300, center_y-300, center_x+300, center_y+300)
    time.sleep(3)
    controller.move_to_position(center_x+500 , center_y)
    time.sleep(3)

    print("测试完成!")
    listener.stop()

if __name__ == "__main__":
    test_mouse_functions()
