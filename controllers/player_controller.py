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
    
    def save_state(self):
        return {
            name: {
                k: v for k, v in player.__dict__.items() 
                if k not in ['event_manager', 'logger']  # Exclude non-pickleable objects
            } for name, player in self.playerList.items()
        }
    
    @classmethod
    def from_dict(cls, saved_data, eventcontroller):
        playerController = cls(eventcontroller)
        for name, data in saved_data.items():
            player = Player(event_manager=eventcontroller,name = data['name'],age = data['age'],sex = data['sex'],current_exp = data['current_exp'])  # Re-inject fresh event manager
            player.__dict__.update(data)
            playerController.playerList[name] = player
        return playerController