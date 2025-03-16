from .event_controller import EventController
from models import Player
class PlayerController:
    playerList = {}
    def __init__(self,event_controller:EventController):
        self.event_controller = event_controller

    def buildPlayer(self,name,*args,**kargs):
        player_item = Player(event_manager=self.event_controller,name=name,*args,**kargs)
        PlayerController.playerList[name] = player_item
        return player_item
        
    # 默认第一个作为宗主
    def getMaster(self):
        for k,v in self.playerList.items():
            return k,v