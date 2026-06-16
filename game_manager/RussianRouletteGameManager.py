import random
from DefaultGameConfig import DefaultGameConfig

class RussianRouletteGameManager():
    # Set up game properties at the start
    def __init__(self, **kwargs):
        # Get attribute values from kwargs, otherwise use default attributes
        self.player_hp: int = kwargs.get("player_hp", DefaultGameConfig.player_hp)
        self.ai_hp: int = kwargs.get("ai_hp", DefaultGameConfig.ai_hp)
        
        self.total_bullet_count: int = kwargs.get("total_bullet_count", DefaultGameConfig.total_bullet_count)
        self.live_bullet_count: int = kwargs.get("live_bullet_count", DefaultGameConfig.live_bullet_count)
        self.bullet_dmg: int = kwargs.get("bullet_dmg", DefaultGameConfig.bullet_dmg)

        self.gun_chamber: GunChamber = self.generate_chamber()
        self.cur_round: int = kwargs.get("cur_round", DefaultGameConfig.cur_round)
        self.cur_bullet_index: int = kwargs.get("cur_bullet_index", DefaultGameConfig.cur_bullet_index)
        self.is_player_turn: int = kwargs.get("is_player_turn", DefaultGameConfig.is_player_turn)

    # Generate new chamber
    def generate_chamber(self):
        # Add the live bullets to the chamber and fill the rest with blank bullets
        # (live = 1, blank = 0)
        array = [1] * self.live_bullet_count
        array.extend([0] * (self.total_bullet_count - self.live_bullet_count))
        
        # Shuffle the bullets in the chamber and create an object to store the array
        random.shuffle(array)
        chamber = GunChamber(bullet_array=array)
        
        return chamber
    
    # Looping the game until any player reach 0 HP
    def run_game():
        ...

    def _display_game_status(self):
        ...

    def _get_player_action(self):
        ...
        
    def _get_ai_action(self):
        ...

    def _reset_round(self):
        ...
    
    # Function handling the action of shooting the opponent (by either the player or AI)
    def shoot_opponent(self):
        # Check if the bullet is a live bullet
        is_live_bullet = self.gun_chamber.get_bullet_at_index(self.cur_bullet_index)
        
        # Get the bullet damage and decrement the live bullet count
        hp_loss = 0
        if is_live_bullet:
            hp_loss = self.bullet_dmg
            self.live_bullet_count -= 1
            
        # Decide which target to remove HP from
        if self.is_player_turn:
            self.ai_hp -= hp_loss
        else:
            self.player_hp -= hp_loss

        # Change the turn to the other player
        self.is_player_turn = not self.is_player_turn
    
    # Function handling the action of shooting oneself (by either the player or AI)
    def shoot_self(self):
        # Check if the bullet is a live bullet
        is_live_bullet = self.gun_chamber.get_bullet_at_index(self.cur_bullet_index)
        
        # Get the bullet damage and decrement the live bullet count
        hp_loss = 0
        if is_live_bullet:
            hp_loss = self.bullet_dmg
            self.live_bullet_count -= 1
            
        # Decide which target to remove HP from
        if self.is_player_turn:
            self.ai_hp -= hp_loss
        else:
            self.player_hp -= hp_loss

        # Change the turn to the other player only if the bullet was live
        if is_live_bullet:
            self.is_player_turn = not self.is_player_turn
        
class GunChamber():
    def __init__(self, bullet_array):
        self.bullet_array = bullet_array
        
    def get_bullet_at_index(self, index):
        return self.bullet_array[index]