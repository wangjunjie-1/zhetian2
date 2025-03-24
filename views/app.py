
import tkinter as tk


from controllers import PlayerController
from controllers import EventController
from models import Player

from views.main_view import MainView
from .player_view import PlayerInfoView
import logging
class App:
    def __init__(self, root,eventcontroller:EventController,playercontroller:PlayerController):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.root = root
        self.current_view = None
        self.eventcontroller = eventcontroller
        self.playercontroller = playercontroller

        self.eventcontroller.subscribe('show_player_view',self.show_player_view)
        self.eventcontroller.subscribe('show_main_view',self.show_main_view)
        
    def start(self):
        # # 启动游戏循环
        self.show_main_view()
        self.root.mainloop() 

    def show_main_view(self):
        # 隐藏当前界面
        if self.current_view:
            self.current_view.hide()

        # 显示主界面
        self.current_view = MainView(self.root,self.eventcontroller,self.playercontroller)
        self.current_view.show()

    def show_player_view(self,player:Player=None):
        # 隐藏当前界面
        if self.current_view:
            self.current_view.hide()

        # 显示第二界面
        self.current_view = PlayerInfoView(self.root,self.eventcontroller,self.playercontroller,player = player)
        self.current_view.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop() 