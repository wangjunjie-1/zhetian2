# core/game_engine.py
import time
import threading
import tkinter as tk
from .world import World
from .event_controller import EventController
from .player_controller import PlayerController
from .weapon_controller import WeaponController

from views.main_view import MainView
from views.app import App

import os
import logging

class GameEngine:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.is_running = False
        self.eventcontroller = EventController()
        self.eventcontroller.subscribe('exit',self.stop)
        

        filename='savegame.pkl'
        if os.path.exists(filename):
            self.load_game(filename)
        else:
            self.init_game()
            self.playercontroller.buildPlayer(name='龙傲天')
        self.build_app()

    def init_game(self):
        self.world = World(eventcontroller=self.eventcontroller)
        self.playercontroller = PlayerController(event_controller=self.eventcontroller)
        self.weaponController = WeaponController(event_controller=self.eventcontroller)
        
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
        self.save_game()  # 添加保存操作
        self.root.destroy()  # 关闭 Tkinter 窗口
        print("游戏停止！")

    def main_loop(self):
        """游戏主循环"""
        while self.is_running:
            try:
                self.world.update(1)  # 每秒更新一次
                time.sleep(1)  # 控制游戏速度
            except KeyboardInterrupt:
                self.stop()
    
    def save_game(self, filename='savegame.pkl'):
        import pickle
        state = {
            'world': self.world.to_dict(),
            'players': self.playercontroller.save_state(),
            'weapon':self.weaponController.save_state()
        }
        with open(filename, 'wb') as f:
            pickle.dump(state, f)
    
    def load_game(self, filename='savegame.pkl'):
        import pickle
        with open(filename, 'rb') as f:
            state = pickle.load(f)
        self.world = World.from_dict(state['world'], self.eventcontroller)
        self.weaponController = WeaponController.from_dict(state['weapon'], self.eventcontroller)
        self.playercontroller = PlayerController.from_dict(state['players'], self.eventcontroller)
        print("游戏加载完成！")