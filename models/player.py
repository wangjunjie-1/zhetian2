from .realm import Realm
from .spiritroot import SpiritRoot
from controllers import EventController
import random
import numpy as np
import logging
# models/player.py
class Player:
    def __init__(self, event_manager:EventController,name:str='zhangsan',age = 16,sex = 0,current_exp = 0):
        """
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        # 基础属性
        self.name = name
        self.age = age
        self.sex = 0

        # 灵根
        self.spiritroot = SpiritRoot()
        self.cultivation_coefficient= self.spiritroot.getRate()     
        
        # 修为相关
        self.realm = Realm()
        self.current_exp = current_exp

        # 突破几率
        self.base_breakup_probability = 0.01

        # 事件订阅
        self.event_manager = event_manager
        
        # 时间流逝触发修炼
        self.event_manager.subscribe('time_pass',self.cultivate)

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
        base_exp = self.cultivation_coefficient
        #todo：
        #武器修炼系数
        weapon_exp = 0
        #功法修炼系数
        skill_exp = 0

        return (base_exp+weapon_exp+skill_exp)

    def __str__(self):
        return (f"玩家: {self.name}\n"+
                f"年龄: {self.age}\n"+
                f"灵根：{self.spiritroot}\n"+
                f"修为:\n{self.realm}\n")