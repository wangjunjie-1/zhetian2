from .event_controller import EventController
from models import Player
from dao.dao_player import UserQuery
class PlayerController:
    playerList = {}
    def __init__(self,event_controller:EventController):
        self.playerdao = UserQuery()
        self.event_controller = event_controller

    def playerGetWeapon(self,player_name,weapon):
        player = self.getPlayer(player_name)
        if player:
            player.weapons.append(weapon)
            player.auto_equip_weapon()
            return True
        return False
    
    def playerLoseWeapon(self,player_name,weapon):
        player = self.getPlayer(player_name)
        if player:
            if weapon not in player.weapons:
                return False
            weapon.is_equip = False
            player.weapons.remove(weapon)
            player.auto_equip_weapon()
            return True
        return False

    def delete_player(self,player):
        self.playerdao.delete_user(player)
        return True
   
    def build_player(self,**kargs):
        player = Player(self.event_controller)
        player.update_state(kargs)
        lastrowid = self.playerdao.add_user(player)
        player.id = lastrowid
        return player
    
    def update_player_byitem(self,player): 
        self.playerdao.update_user(player)
        return True  
    
    def update_player_bydict(self,**kargs):
        player = Player(self.event_controller)
        player.update_state(kargs)
        self.playerdao.update_user(player)
        return True
    
    def get_master(self):
        master_info= self.playerdao.get_master_user()
        master = Player(self.event_controller)
        master.update_state(master_info)
        return master
    
    def get_player_by_id(self,player_id):
        player_info = self.playerdao.get_user_by_id(player_id)
        player = Player(self.event_controller)
        player.update_state(player_info)
        return player
    
    def get_player_list(self):
        player_info_list = self.playerdao.get_all_users()
        player_list = []
        for player_info in player_info_list:
            player = Player(self.event_controller)
            player.update_state(player_info)
            player_list.append(player)
        return player_list

    def get_Disciples(self):
        """获取所有弟子名称（排除掌门）"""
        disciples = self.get_player_list()
        master = self.get_master()
        disciples.remove(master)
        return disciples
    
if __name__ == '__main__':
    event_controller = EventController()
    player_controller = PlayerController(event_controller)
    master = player_controller.get_master()
    print(master)