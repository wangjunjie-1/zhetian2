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