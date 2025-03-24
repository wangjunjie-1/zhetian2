
import csv
import random
from pathlib import Path
from models.weapon import WEAPON
from models.player import Player
from .event_controller import EventController
from collections import defaultdict

class WeaponController:
    """武器系统控制器"""
    # 移动所有常量到控制器类
    LEVELS = ['天', '地', '玄', '黄', '宇', '宙', '洪', '荒']
    PARTS_MAP = {
        0: ['盔','帽'],
        1: ['戒','佩','巾','璎珞','如意'],
        2: ['剑','刀','枪','戟','钺','弓','棍'],
        3: ['鞋','屐','履','靴'],
        4: ['衣','甲','袍']
    }
    weaponList = []
    def __init__(self, event_controller:EventController=None):
        self.event_controller = event_controller
        
        self.name_pool = self._load_names()
                # 触发事件（如果有事件控制器）
        if self.event_controller:
            self.event_controller.subscribe('weapon_created', self.create_weapon)
            self.event_controller.subscribe('weapon_assigned', lambda args: self.assign_weapon(*args)) 
            
    
    def _load_names(self):
        """加载武器名称库"""
        csv_path = Path(__file__).parent.parent/'weapon_name.csv'
        with open(csv_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    
    def create_weapon(self, part_category: int = None, level: int = None) -> WEAPON:
        """创建武器实例"""
        # 随机选择部件类型（如果未指定）
        part_category = part_category if part_category is not None else random.choice(list(self.PARTS_MAP.keys()))
        part_type = random.choice(self.PARTS_MAP[part_category])
        
        # 生成武器级别（如果未指定）
        level = level if level is not None else random.randint(0, len(self.LEVELS)-1)
        
        # 生成武器名称
        base_name = random.choice(self.name_pool)
        full_name = f"{base_name}·{self.LEVELS[level]}"
        
        # 创建武器实例
        weapon = WEAPON(
            name=full_name,
            level=level,
            part_type=part_type,
            owner_name='宗门'
        )
        
        
        # 添加到武器列表
        WeaponController.weaponList.append(weapon)
            
        return weapon
    
    def find_by_owner(self, owner_name: str = '宗门'):
        """查找玩家拥有的武器"""
        return [w for w in self.weapons if w.owner == owner]
    
    def save_state(self):
        """序列化武器数据"""
        weapon_data = []
        for weapon in WeaponController.weaponList:
            data = {
                'name': weapon.name,
                'level': weapon.level,
                'part_type': weapon.part_type,
                'owner_name': weapon.owner_name,
                # 新增系数保存
                'weapon_cultivation_coefficient': weapon.weapon_cultivation_coefficient,
                'weapon_attact_coefficient': weapon.weapon_attact_coefficient,
                'weapon_attact_upgrade': weapon.weapon_attact_upgrade,
                'weapon_breakup_probability': weapon.weapon_breakup_probability
            }
            weapon_data.append(data)
        return weapon_data
    
    @classmethod
    def from_dict(cls, saved_data, eventcontroller):
        weaponController = cls(eventcontroller)
        """反序列化武器数据"""
        weaponController.weaponList = []
        for data in saved_data:
            weapon = WEAPON(
                name=data['name'],
                level=data['level'],
                part_type=data['part_type'],
                owner_name=data['owner_name']
            )
            # 恢复系数
            weapon.weapon_cultivation_coefficient = data.get('weapon_cultivation_coefficient', 0)
            weapon.weapon_cultivation_upgrade = data.get('weapon_cultivation_upgrade', 0)
            weapon.weapon_attact_coefficient = data.get('weapon_attact_coefficient', 1)
            weapon.weapon_attact_upgrade = data.get('weapon_attact_upgrade', 0)
            weapon.weapon_breakup_probability = data.get('weapon_breakup_probability', 0.1)
            weapon.is_equip = data.get('is_equip', False)
            WeaponController.weaponList.append(weapon)
    
    def assign_weapon(self, owner_name: str, weapon: WEAPON):
        old_owner_name= weapon.owner_name
        ret = self.event_controller.publish('player_lose_weapon', (old_owner_name,weapon))[0]
        print(f'{old_owner_name} lose {weapon.name} {ret}')

        weapon.owner_name = owner_name
        ret = self.event_controller.publish('player_get_weapon', (owner_name, weapon))[0]
        print(f'{owner_name} get {weapon.name} {ret}')
