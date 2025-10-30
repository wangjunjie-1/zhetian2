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

    
    def move_mouse(self, x: int, y: int, duration: Optional[float] = None) -> None:
        """
        移动鼠标到指定坐标
        
        Args:
            x: 目标X坐标
            y: 目标Y坐标
            duration: 移动持续时间，如果为None则使用随机延迟
        """
        if duration is None:
            duration = random.uniform(*self.move_delay_range)
        
        pyautogui.moveTo(x, y, duration=duration)
        time.sleep(random.uniform(*self.click_delay_range) / 2)
    
    def left_click(self, x: Optional[int] = None, y: Optional[int] = None, 
                  clicks: int = 1, duration: Optional[float] = None) -> None:
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
        
        pyautogui.click(button='left', clicks=clicks, duration=duration)
        time.sleep(random.uniform(*self.click_delay_range))
    
    def right_click(self, x: Optional[int] = None, y: Optional[int] = None, 
                   duration: Optional[float] = None) -> None:
        """
        右键点击
        
        Args:
            x: 点击X坐标，为None则在当前位置点击
            y: 点击Y坐标，为None则在当前位置点击
            duration: 点击持续时间
        """
        if x is not None and y is not None:
            self.move_mouse(x, y)
        
        pyautogui.click(button='right', duration=duration)
        time.sleep(random.uniform(*self.click_delay_range))
    
    def select_unit(self, x: int, y: int) -> None:
        """
        左键选择单位
        
        Args:
            x: 单位X坐标
            y: 单位Y坐标
        """
        # 添加一些随机性，让选择看起来更自然
        x += random.randint(-5, 5)
        y += random.randint(-5, 5)
        
        self.left_click(x, y)
    
    def move_to_position(self, x: int, y: int) -> None:
        """
        右键移动到指定位置
        
        Args:
            x: 目标X坐标
            y: 目标Y坐标
        """
        # 添加一些随机性，让移动指令看起来更自然
        x += random.randint(-10, 10)
        y += random.randint(-10, 10)
        
        self.right_click(x, y,duration=0.5)
    
    def drag_mouse(self, start_x: int, start_y: int, end_x: int, end_y: int, 
                  duration: Optional[float] = None) -> None:
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
        pyautogui.dragTo(end_x, end_y, duration=duration, button='left')
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
    
    def box_select(self, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        """
        框选多个单位
        
        Args:
            start_x: 框选起始X坐标
            start_y: 框选起始Y坐标
            end_x: 框选结束X坐标
            end_y: 框选结束Y坐标
        """
        self.drag_mouse(start_x, start_y, end_x, end_y)
    
    def get_current_position(self) -> Tuple[int, int]:
        """
        获取鼠标当前位置
        
        Returns:
            当前鼠标坐标 (x, y)
        """
        return pyautogui.position()
    
    def is_mouse_at_edge(self) -> Tuple[bool, Optional[str]]:
        """
        检查鼠标是否在屏幕边缘
        
        Returns:
            (是否在边缘, 边缘方向或None)
        """
        x, y = self.get_current_position()
        
        if x <= self.edge_margin:
            return True, 'left'
        elif x >= self.screen_width - self.edge_margin:
            return True, 'right'
        elif y <= self.edge_margin:
            return True, 'up'
        elif y >= self.screen_height - self.edge_margin:
            return True, 'down'
        
        return False, None
    
    def simulate_random_movement(self, count: int = 5, area: Optional[Tuple[int, int, int, int]] = None) -> None:
        """
        模拟随机鼠标移动，增加操作的自然性
        
        Args:
            count: 随机移动次数
            area: 移动区域 (x, y, width, height)，None表示整个屏幕
        """
        if area is None:
            area = (self.edge_margin, self.edge_margin, 
                   self.screen_width - 2 * self.edge_margin, 
                   self.screen_height - 2 * self.edge_margin)
        
        for _ in range(count):
            x = random.randint(area[0], area[0] + area[2])
            y = random.randint(area[1], area[1] + area[3])
            self.move_mouse(x, y)
    
    def click_at_random_point_in_area(self, x: int, y: int, width: int, height: int) -> None:
        """
        在指定区域内随机点击
        
        Args:
            x: 区域起始X坐标
            y: 区域起始Y坐标
            width: 区域宽度
            height: 区域高度
        """
        target_x = x + random.randint(0, width)
        target_y = y + random.randint(0, height)
        self.left_click(target_x, target_y)


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
