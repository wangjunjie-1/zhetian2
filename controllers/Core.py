# core/game_engine.py
import time
import threading
import tkinter as tk
from .world import World
from .event_controller import EventController
from .player_controller import PlayerController

from views.main_view import MainView
from views.app import App

import logging

class GameEngine:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.is_running = False
        self.eventcontroller = EventController()
        self.world = World(eventcontroller=self.eventcontroller)
        self.playercontroller = PlayerController(event_controller=self.eventcontroller)
        self.build_app()

    def build_app(self):
        # 初始化 UI
        self.root = tk.Tk()
        self.app = App(self.root,self.eventcontroller,self.playercontroller) 
        
    def start(self):
        """启动游戏"""
        if self.is_running:
            return

        self.is_running = True
        self.logger.info("游戏启动！")

        self.logger.debug("初始化人物信息")
        self.playercontroller.buildPlayer(name='wjj')

        self.logger.debug("启动主线程")
        self.thread = threading.Thread(target=self.main_loop)
        self.thread.daemon = True  # 设置为守护线程，主线程退出时自动结束
        self.thread.start()

        if hasattr(self,'app') :
            print("启动UI线程")
            self.app.start()
        
        self.thread.join()


    def stop(self):
        """停止游戏"""
        self.is_running = False
        print("游戏停止！")

    def main_loop(self):
        """游戏主循环"""
        while self.is_running:
            try:
                self.world.update(1)  # 每秒更新一次
                time.sleep(1)  # 控制游戏速度
            except KeyboardInterrupt:
                self.stop()