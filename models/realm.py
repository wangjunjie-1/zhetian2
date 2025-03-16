# models/realm.py
import random
import logging

class Realm:
    REALMS = [
        {"name": "凡人境","probability":0.99,"exp_required": 0,           "spirit_power": 0, "spirit_sense": 0,             "lifespan": 100},
        {"name": "炼气境","probability":0.9,"exp_required": 100,          "spirit_power": 10, "spirit_sense": 5,            "lifespan": 150},
        {"name": "筑基境","probability":0.8,"exp_required": 1000,         "spirit_power": 50, "spirit_sense": 20,           "lifespan": 300},
        {"name": "金丹境","probability":0.7,"exp_required": 10000,        "spirit_power": 200, "spirit_sense": 100,         "lifespan": 500},
        {"name": "元婴境","probability":0.6,"exp_required": 100000,       "spirit_power": 1000, "spirit_sense": 500,        "lifespan": 1000},
        {"name": "化神境","probability":0.5,"exp_required": 1000000,      "spirit_power": 5000, "spirit_sense": 2000,       "lifespan": 2000},
        {"name": "合体境","probability":0.4,"exp_required": 10000000,     "spirit_power": 20000, "spirit_sense": 10000,     "lifespan": 5000},
        {"name": "大乘境","probability":0.3,"exp_required": 100000000,    "spirit_power": 100000, "spirit_sense": 50000,    "lifespan": 10000},
        {"name": "渡劫境","probability":0.2,"exp_required": 1000000000,   "spirit_power": 500000, "spirit_sense": 200000,   "lifespan": 20000},
        {"name": "真仙境","probability":0.0,"exp_required": 10000000000,  "spirit_power": 2000000, "spirit_sense": 1000000, "lifespan": -1},  # 长生不老
    ]

    def __init__(self, current_realm_index=0):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.current_realm_index = current_realm_index

    @property
    def current_realm(self):
        """获取当前境界"""
        return self.REALMS[self.current_realm_index]
    
    @property
    def next_realm(self):
        """获取下一个境界"""
        if self.current_realm_index + 1 < len(self.REALMS):
            return self.REALMS[self.current_realm_index + 1]
        return None
    
    @property
    def current_exp_required(self):
        return self.REALMS[self.current_realm_index]['exp_required']

    @property
    def current_probability(self):
        return self.REALMS[self.current_realm_index]['probability']

    @property
    def lifespan(self):
        return self.REALMS[self.current_realm_index]['lifespan']

    @property
    def current_realm_info(self):
        """获取当前境界信息"""
        return {
            'exp_required':self.current_exp_required,
            'probability':self.current_probability,
            'lifespan': self.REALMS[self.current_realm_index]['lifespan'],
            'current_realm_name': self.current_realm['name'],
            'next_realm_name': self.next_realm['name'],
        }


    
    def __str__(self):
        return "当前境界: {current_realm_name}\n经验: {exp_current}/{exp_required}\n寿命: {lifespan}\n".format(**self.current_realm_info)


# 测试代码
if __name__ == "__main__":
    realm = Realm()
    print(realm)

    realm.add_exp(150)  # 炼气境
    print(realm)

    realm.add_exp(1000)  # 筑基境
    print(realm)