import random
from typing import Optional
from models.player import Player

class WEAPON:
    def __init__(self, name: str, level: int, part_type: str, owner_name: str = '宗门'):
        self.name = name        # 武器全名
        self.level = level      # 品级索引
        self.part_type = part_type  # 部件类型
        self.owner_name = owner_name
        
        # 属性
        self.is_equip = False
        self.weapon_cultivation_coefficient = 1.1
        self.weapon_cultivation_upgrade = 1
        self.weapon_attact_coefficient = 1
        self.weapon_attact_upgrade = 1
        self.weapon_breakup_probability = 0.1

    def __str__(self):
        return f"{self.name}（{self.part_type}）"