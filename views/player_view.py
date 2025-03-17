import tkinter as tk
from models import player
import logging
from .base_view import BaseView

class PlayerInfoView(BaseView):
    def __init__(self,*args,player:player=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.player = player

        self.eventcontroller.subscribe('cultivate',self.update_player_info)
        self.eventcontroller.subscribe('breakup',self.update_player_info)
        self.create_gui()

    def update_player_info(self):
        if self.is_show:
            # 通过after方法调度到主线程
            self.frame.after(0, self.create_gui)

    def create_gui(self):
        # 创建一个框架来组织标签
        frame = self.frame
        frame.pack(padx=20, pady=20)

        # 定义属性和值
        attributes = {
            "姓名": self.player.name,
            "年龄": f"{self.player.age}/{self.player.realm.current_realm_info['lifespan']}",
            "境界": f"{self.player.realm.current_realm_info['current_realm_name']}",
            "职位": f"掌门",
            "出身": f"异界",
            "传承": f"无",
            "灵根": f"{self.player.spiritroot}",
            "庇护人数上限": "-1000",
            "渡劫死亡率": "-1.00%",
            "灵力": f"{int(self.player.current_exp)}/{self.player.realm.current_exp_required}+{self.player.spiritroot.getRate():.2f}",
            "突破几率": f"{self.player.breakup_probability:.2%}",
            "探索速度": "-171.96%",
            "种植效率": "-100.00%",
            "采矿效率": "-107.00%",
            "炼丹速度": "-107.00%",
            "炼器效率": "-107.00%",
            "武力": "-1",
            "父母": "-1",
            "师尊": "-1",
            "道侣": "-1",
            "特质": "-1",
            "弟子": "-1",
            "子嗣": "-1",
            "著作": "-1"
        }

        # 创建标签并添加到框架
        row = 0
        for key, value in attributes.items():
            label = tk.Label(frame, text=f"{key}: {value}", font=("Arial", 12))  # 设置字体大小
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")  # 增加行间距
            row += 1
        button = tk.Button(frame, text="返回", command=lambda: self.eventcontroller.publish('show_main_view'))
        button.grid(row=row, column=0, padx=10, pady=5, sticky="w")
