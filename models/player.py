from .realm import Realm
from .spiritroot import SpiritRoot
from controllers import EventController
import random
import numpy as np
import logging
# models/player.py
class Player:
    def __init__(self, event_manager:EventController):
        """
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.event_manager = event_manager
        # 基础属性
        self.id = -1
        self.name = '龙傲天'
        self.age = 0
        self.sex = 0
        self.isMaster = 0
        self.isDead = 0
        self.father_id = -1
        self.mother_id = -1
        self.teacher_id = -1
        self.root = ""
        self.base_breakup_probability = -1
        self.realm_level = 1
        self.current_exp = 0

        # 武力
        # self.spiritroot = SpiritRoot()
        # self.base_cultivation_coefficient = self.spiritroot.getRate()   
        # self.base_attack_up_limit = 10*self.realm.current_realm_index
        
        # 时间流逝触发修炼
        self.event_manager.subscribe('time_pass',self.cultivate)

    def update_state(self, player_info):
        self.id = player_info.get('id', self.id)
        self.name = player_info.get('name', self.name)
        self.age = player_info.get('age', self.age)
        self.sex = player_info.get('sex', self.sex)
        self.root = player_info.get('root', self.root)
        self.father_id = player_info.get('father_id', self.father_id)
        self.mother_id = player_info.get('mother_id', self.mother_id)
        self.teacher_id = player_info.get('teacher_id', self.teacher_id)
        self.realm_level = player_info.get('realm_level',-1)
        self.base_breakup_probability = player_info.get('base_breakup_probability', self.base_breakup_probability)
        self.isMaster = player_info.get('isMaster', self.isMaster)
        self.isDead = player_info.get('isDead', self.isDead)
        self.current_exp = player_info.get('current_exp', self.current_exp)

    @property
    def realm(self):
        realm = Realm()

    @property
    def breakup_probability(self):
        probability = np.clip(self.base_breakup_probability + self.realm.current_probability,0,1)
        return probability


    def cultivate(self):
        """
        玩家修炼功法，提升修为。
        :param skill: 修炼的功法对象
        """
        # 可以获得的修为
        new_exp = self._cultivate_get_exp()

        # 增加经验后进行判断情况
        now_exp = self.current_exp + new_exp
        # 存在晋级的可能
        if now_exp >= self.realm.current_exp_required:
            if self.realm.next_realm is not None:
                if random.random() < self.breakup_probability:
                    self.logger.info(f"突破 {self.realm.current_realm['name']}，进入 {self.realm.next_realm['name']}！")
                    self.realm.current_realm_index += 1
                else:
                    self.logger.info(f"突破{self.realm.next_realm['name']}失败")
                self.current_exp = 0
            else:
                self.current_exp = self.realm.current_exp_required
                self.logger.info(f"已达到最高境界，无法继续修炼！")
        else:
            self.current_exp = now_exp
            self.event_manager.publish('cultivate')
            self.logger.info(f"修炼成功，获得 {new_exp:.2f} 点修为，当前修为: {self.current_exp:.2f}")
    
    # 修炼相关函数
    def _cultivate_get_exp(self):
        # 灵根修炼系数
        root_coef = self.base_cultivation_coefficient

        weapon_coef = 0
        weapon_upgrade = 0
        #武器修炼系数
        for weapon in self.weapons:
            if weapon.is_equip ==True:
                weapon_coef += weapon.weapon_cultivation_coefficient
                weapon_upgrade += weapon.weapon_cultivation_upgrade

        #功法修炼系数
        skill_coef = 0
        skill_upgrade = 0

        return (1+weapon_upgrade+skill_upgrade)*(root_coef+weapon_coef+skill_coef)

    def auto_equip_weapon(self):
        """自动装备未穿戴的武器"""
        from controllers.weapon_controller import WeaponController  # 新增导入
        
        # 遍历所有装备槽位（使用WeaponController中的标准定义）
        for slot, parts in WeaponController.PARTS_MAP.items():
            # 获取该槽位当前已装备的武器（如果有）
            equipped = [w for w in self.weapons if w.is_equip and w.part_type in parts]
            
            # 查找玩家拥有的该类型武器（包含已装备和未装备）
            available = [w for w in self.weapons if w.part_type in parts]
            
            if available:
                # 选择品级最高的武器
                best_weapon = max(available, key=lambda x: x.level)
                
                # 如果当前没有装备或找到更好的武器
                if not equipped or best_weapon != equipped[0]:
                    # 卸载原有装备
                    for w in equipped:
                        w.is_equip = False
                    # 装备新武器
                    best_weapon.is_equip = True

        # 确保每个武器最多只装备一件
        equipped_weapons = [w for w in self.weapons if w.is_equip]
        for weapon in equipped_weapons:
            # 检查是否有更优的同部位装备
            slot = next(k for k,v in WeaponController.PARTS_MAP.items() 
                      if weapon.part_type in v)
            current_best = max(
                (w for w in self.weapons if w.part_type in WeaponController.PARTS_MAP[slot]),
                key=lambda x: x.level
            )
            if current_best != weapon:
                weapon.is_equip = False
                current_best.is_equip = True


    def __str__(self):
        return (f"玩家: {self.name}\n" +
            f"年龄: {self.age}\n" +
            f"性别: {'男' if self.sex == 0 else '女'}\n" +
            f"灵根: {self.root}\n" +
            f"境界: {self.realm_level}\n" +
            f"当前经验: {self.current_exp}\n" +
            f"突破概率: {self.base_breakup_probability:.2f}\n" +
            f"是否已死: {'是' if self.isDead else '否'}\n" +
            f"父亲ID: {self.father_id}\n" +
            f"母亲ID: {self.mother_id}\n" +
            f"老师ID: {self.teacher_id}\n"+
            f"是否宗主: {'是' if self.isMaster else '否'}\n"+
            f"用户id: {self.id}\n")
            