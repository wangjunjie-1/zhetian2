from typing import Union, Dict, List, Tuple, Any

wall_idx = 1
farmer02_idx = 2
farmer01_idx = 3
camp_idx = 0
research_idx = 4
base_idx = 5
farm_idx = 6
tree_idx = 8
cailiao_idx = 7
zhuanshen_idx = 9
# jiezhi_idx = 0

_cailiao_box = {
    '1_pass':{
        'build_idx':str(cailiao_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '2_pass':{
        'build_idx':str(cailiao_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '3_pass':{
        'build_idx':str(cailiao_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '4_pass':{
        'build_idx':str(cailiao_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '5_pass':{
        'build_idx':str(cailiao_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '6_pass':{
        'build_idx':str(cailiao_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '7_pass':{
        'build_idx':str(cailiao_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '8_pass':{
        'build_idx':str(cailiao_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '9_pass':{
        'build_idx':str(cailiao_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '10_pass':{
        'build_idx':str(cailiao_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
}


_zhuanshen_box = {
    '1_pass':{
        'build_idx':str(zhuanshen_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '2_pass':{
        'build_idx':str(zhuanshen_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '3_pass':{
        'build_idx':str(zhuanshen_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '4_pass':{
        'build_idx':str(zhuanshen_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '5_pass':{
        'build_idx':str(zhuanshen_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '6_pass':{
        'build_idx':str(zhuanshen_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '7_pass':{
        'build_idx':str(zhuanshen_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '8_pass':{
        'build_idx':str(zhuanshen_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '9_pass':{
        'build_idx':str(zhuanshen_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },
    '10_pass':{
        'build_idx':str(zhuanshen_idx),
        'box_idx':'Q',
        'boss_pos':(100,100,200,200),
        'cost_time':60,
    },

}




class Coordinate:
    def __init__(self, *args, **kwargs):
        """
        初始化坐标对象，支持多种输入方式：
        
        1. Coordinate(abs_x, abs_y, rel_x, rel_y)
        2. Coordinate([abs_x, abs_y, rel_x, rel_y])
        3. Coordinate({'abs_x': ..., 'abs_y': ..., 'rel_x': ..., 'rel_y': ...})
        4. Coordinate(abs_x=..., abs_y=..., rel_x=..., rel_y=...)
        """
        # 默认值
        self.abs_x = 0.0
        self.abs_y = 0.0
        self.rel_x = 0.0
        self.rel_y = 0.0

        # 情况1：传入字典作为第一个位置参数
        if len(args) == 1 and isinstance(args[0], dict):
            data = args[0]
        # 情况2：传入 list/tuple 作为第一个位置参数
        elif len(args) == 1 and isinstance(args[0], (list, tuple)):
            if len(args[0]) != 4:
                raise ValueError("List or tuple must contain exactly 4 elements: [abs_x, abs_y, rel_x, rel_y]")
            data = {
                'abs_x': args[0][0],
                'abs_y': args[0][1],
                'rel_x': args[0][2],
                'rel_y': args[0][3]
            }
        # 情况3：传入4个独立数值
        elif len(args) == 4:
            data = {
                'abs_x': args[0],
                'abs_y': args[1],
                'rel_x': args[2],
                'rel_y': args[3]
            }
        # 情况4：仅使用关键字参数
        elif len(args) == 0 and kwargs:
            data = kwargs
        else:
            raise ValueError(
                "Invalid input. Use one of:\n"
                "  Coordinate(abs_x, abs_y, rel_x, rel_y)\n"
                "  Coordinate([abs_x, abs_y, rel_x, rel_y])\n"
                "  Coordinate({'abs_x': ..., 'abs_y': ..., 'rel_x': ..., 'rel_y': ...})\n"
                "  Coordinate(abs_x=..., abs_y=..., rel_x=..., rel_y=...)"
            )

        # 赋值并做类型转换（转为 float 更通用）
        try:
            self.abs_x = float(data.get('abs_x', 0))
            self.abs_y = float(data.get('abs_y', 0))
            self.rel_x = float(data.get('rel_x', 0))
            self.rel_y = float(data.get('rel_y', 0))
        except (TypeError, ValueError) as e:
            raise ValueError("All coordinate values must be numeric.") from e

    def to_dict(self) -> Dict[str, float]:
        """转换为字典"""
        return {
            'abs_x': self.abs_x,
            'abs_y': self.abs_y,
            'rel_x': self.rel_x,
            'rel_y': self.rel_y
        }

    def to_list(self) -> List[float]:
        """转换为列表 [abs_x, abs_y, rel_x, rel_y]"""
        return [self.abs_x, self.abs_y, self.rel_x, self.rel_y]

    def __repr__(self) -> str:
        return (f"Coordinate(abs_x={self.abs_x}, abs_y={self.abs_y}, "
                f"rel_x={self.rel_x}, rel_y={self.rel_y})")

    def __str__(self) -> str:
        return f"Abs: ({self.abs_x}, {self.abs_y}), Rel: ({self.rel_x}, {self.rel_y})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Coordinate):
            return False
        return (self.abs_x == other.abs_x and
                self.abs_y == other.abs_y and
                self.rel_x == other.rel_x and
                self.rel_y == other.rel_y)