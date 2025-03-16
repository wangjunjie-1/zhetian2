import random
import math

class SpiritRoot:
    # 定义灵根属性及其权重
    BASE_ATTRIBUTES = {
        '金': 0.2,
        '木': 0.2,
        '水': 0.2,
        '火': 0.2,
        '土': 0.2,
    }
    
    ADVANCED_ATTRIBUTES = {
        '风': 0.1,  # 高级属性权重更高
        '冰': 0.1,
        '空': 0.05,
    }
    
    # 定义灵根级别及其权重
    LEVELS = {
        '普通': 0.7,
        '变异': 0.2,
        '地': 0.08,
        '天': 0.02,
    }
    
    # 灵根数量的分布权重（灵根越多，几率越小）
    ATTRIBUTE_COUNT_WEIGHTS = [0.4, 0.3, 0.2, 0.08, 0.02]  # 1到5个灵根的权重
    
    def __init__(self):
        self.attributes = self._generate_attributes()
        self.level = self._generate_level()
        self.coefficient = self.calculate_cultivation_coefficient
    
    def _generate_attributes(self):
        # 合并基础属性和高级属性
        all_attributes = {**self.BASE_ATTRIBUTES, **self.ADVANCED_ATTRIBUTES}
        
        # 根据权重随机选择灵根数量（1到5个）
        attribute_count = random.choices(
            range(1, 6),
            weights=self.ATTRIBUTE_COUNT_WEIGHTS,
            k=1
        )[0]
        
        # 根据权重随机选择属性
        attributes = random.choices(
            list(all_attributes.keys()),
            weights=list(all_attributes.values()),
            k=attribute_count
        )
        
        # 去重并返回
        return list(set(attributes))
    
    def _generate_level(self):
        # 根据权重随机选择灵根级别
        return random.choices(
            list(self.LEVELS.keys()),
            weights=list(self.LEVELS.values()),
            k=1
        )[0]
    
    def getRate(self):
        return self.calculate_cultivation_coefficient

    @property
    def calculate_cultivation_coefficient(self):
        # 基础修炼系数：每个基础属性为1，每个高级属性为2
        base_coefficient = 0
        for attr in self.attributes:
            if attr in self.BASE_ATTRIBUTES:
                base_coefficient += 1
            elif attr in self.ADVANCED_ATTRIBUTES:
                base_coefficient += 2
        
        # 多灵根加成系数（非线性增长，使用对数增长）
        attribute_count = len(self.attributes)
        if attribute_count == 1:
            multi_attr_bonus = 1.0  # 单灵根无加成
        else:
            multi_attr_bonus = 1.1**attribute_count  # 对数增长
        
        # 灵根级别加成
        level_bonus = {
            '普通': 1.0,
            '变异': 1.5,
            '地': 2.0,
            '天': 3.0,
        }.get(self.level, 1.0)
        
        # 总修炼系数
        total_coefficient = (base_coefficient * multi_attr_bonus) * level_bonus 
        return total_coefficient
    
    def __str__(self):
        # 对属性进行排序：基础属性在前，高级属性在后
        sorted_attributes = ""
        for  base in self.BASE_ATTRIBUTES:
            if base in self.attributes:
                sorted_attributes += base
        for  advanced in self.ADVANCED_ATTRIBUTES:
            if advanced in self.attributes:
                sorted_attributes += advanced
        name_map = {
            1:'单',
            2:'双',
            3:'三',
            4:'四',
            5:'五'
        }
        return f"{''.join(sorted_attributes)} {self.level} {name_map[len(self.attributes)]}灵根"
     

# 示例用法
if __name__ == "__main__":
    spirit_root = SpiritRoot()
    print(f"生成的灵根: {spirit_root}")
    
    coefficient = spirit_root.calculate_cultivation_coefficient
    print(f"修炼系数: {coefficient}")

    spirit_root = SpiritRoot()
    spirit_root.attributes = ['空','空','空','空','空']
    spirit_root.level = '天'
    print(f"生成的灵根: {spirit_root}")
    
    coefficient = spirit_root.calculate_cultivation_coefficient
    print(f"修炼系数: {coefficient}")

