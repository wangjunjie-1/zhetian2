import random
from typing import Optional
from models.player import Player

class WEAPON:
    LEVELS = ['天', '地', '玄', '黄', '宇', '宙', '洪', '荒']
    PARTS = ['头盔', '配饰', '武器', '鞋履', '衣甲']
    
    def __init__(self, level: int=-1, part: int=-1, owner: Optional[Player] = None):
        self.level = level
        self.part = part
        self.owner = owner

    def __str__(self):
        return f"{self.level}级{self.part}（拥有者：{self.owner.name if self.owner else '无'}）"

class WEAPONManager:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.all_weapon = []
        return cls._instance
    
    @classmethod
    def generate_random(cls):
        """随机生成武器"""
        level = random.choices(
            cls._instance.LEVELS,
            weights=[1, 2, 3, 5, 8, 13, 21, 34],  # 按稀有度反向权重
            k=1
        )[0]
        part = random.choice(cls._instance.PARTS)
        weapon = WEAPON(level, part)
        cls._instance.all_weapon.append(weapon)
        return weapon
    
    @classmethod
    def assign(cls, weapon: WEAPON, owner: Player):
        """分配武器给玩家"""
        if weapon.owner:
            raise ValueError("该武器已有主人")
        weapon.owner = owner
        
    @classmethod
    def find_by_owner(cls, owner: Player):
        """查找玩家拥有的武器"""
        return [w for w in cls._instance.all_weapon if w.owner == owner]
    
    @classmethod
    def find_unassigned(cls):
        """查找未分配的武器"""
        return [w for w in cls._instance.all_weapon if not w.owner]