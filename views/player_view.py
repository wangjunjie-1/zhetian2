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
        # 清空原有内容
        for widget in self.frame.winfo_children():
            widget.destroy()
   
        # 创建一个框架来组织标签
        main_frame = self.frame
        main_frame.pack(fill="both", expand=True)
   
        # 第一列 - 原有属性列
        personal_frame = tk.Frame(main_frame, bg="lightblue", bd=2, relief="sunken")
        personal_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.create_personal_attributes(personal_frame)

        # 第二列 - 武器展示列
        weapon_frame = tk.Frame(main_frame, bg="lightyellow", bd=2, relief="sunken")
        weapon_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.create_weapon_display(weapon_frame)

        
    def create_weapon_inventory(self, frame):
        """创建武器库存区域"""
        tk.Label(frame, text="武器库存", font=("Arial", 12)).pack(pady=5)
        
        # 创建滚动条
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建列表框
        self.inventory_listbox = tk.Listbox(
            frame, 
            yscrollcommand=scrollbar.set,
            width=30,
            height=15,
            bg="white",
            selectbackground="#ADD8E6"
        )
        self.inventory_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.inventory_listbox.yview)
        
        # 获取玩家所有武器
        weapons = self.playercontroller.playerList[self.player.name].weapons
        self.update_weapon_inventory(weapons)

    def create_personal_attributes(self, frame):
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
    
    def create_weapon_display(self, frame):
        """创建武器展示区域"""
        # 上方装备槽位
        top_frame = tk.Frame(frame)
        top_frame.pack(fill="x", pady=5)
        tk.Label(top_frame, text="装备栏", font=("Arial", 12)).pack()
        
        # 装备槽位
        self.weapon_labels = {
            0: self.create_weapon_slot(top_frame, "头盔"),
            1: self.create_weapon_slot(top_frame, "饰品"), 
            2: self.create_weapon_slot(top_frame, "武器"),
            3: self.create_weapon_slot(top_frame, "鞋子"),
            4: self.create_weapon_slot(top_frame, "护甲")
        }
        
 
        # 初始化数据
        weapons = self.playercontroller.playerList[self.player.name].weapons
        self.update_weapon_display(weapons)
    
    
    def update_weapon_display(self, weapons):
        """更新武器显示"""
        part_mapping = {
            "头盔": ["盔", "帽"],
            "饰品": ["戒", "佩", "巾", "璎珞", "如意"],
            "武器": ["剑", "刀", "枪", "戟", "钺", "弓", "棍"],
            "鞋子": ["鞋", "屐", "履", "靴"],
            "护甲": ["衣", "甲", "袍"]
        }
        
        # 重置所有槽位
        for label in self.weapon_labels.values():
            label.config(text="[空]", fg="gray")
        
        # 更新已有武器
        for weapon in weapons:
            for slot_name, parts in part_mapping.items():
                if weapon.part_type in parts:
                    self.weapon_labels[list(part_mapping.keys()).index(slot_name)].config(
                        text=f"{weapon.name}({weapon.part_type})",
                        fg="black"
                    )
        
  
    def create_weapon_slot(self, frame, slot_name):
        """创建单个装备槽位"""
        slot_frame = tk.Frame(frame, bg="white", bd=1)
        slot_frame.pack(fill="x", padx=5, pady=2)
        
        tk.Label(slot_frame, text=f"{slot_name}:", width=8, anchor="w").pack(side="left")
        label = tk.Label(slot_frame, text="[空]", fg="gray")
        label.pack(side="left", fill="x", expand=True)
        return label
