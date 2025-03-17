import logging

class World:
    def __init__(self, eventcontroller):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.eventcontroller = eventcontroller
        self.time_elapsed = 0  # 游戏时间（秒）

    def update(self, delta_time):
        self.time_elapsed += delta_time
        self.logger.debug(f"时间流逝: {self.time_elapsed} 秒")
        self.eventcontroller.publish("time_pass")

    def to_dict(self):
        return {
            'time_elapsed': self.time_elapsed
        }
    
    @classmethod
    def from_dict(cls, data, eventcontroller):
        world = cls(eventcontroller)
        world.time_elapsed = data['time_elapsed']
        return world