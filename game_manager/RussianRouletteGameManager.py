import random, math
from game_manager.DefaultGameConfig import DefaultGameConfig

default = DefaultGameConfig()

class RussianRouletteGameManager():
    # Set up game properties at the start
    def __init__(self, **kwargs):
        # Get attribute values from kwargs, otherwise use default attributes
        self.player_hp: int = kwargs.get("player_hp", default.player_hp)
        self.ai_hp: int = kwargs.get("ai_hp", default.ai_hp)
        
        self.total_bullet_count: int = kwargs.get("total_bullet_count", default.total_bullet_count)
        self.live_bullet_count: int = kwargs.get("live_bullet_count", default.live_bullet_count)
        self.bullet_dmg: int = kwargs.get("bullet_dmg", default.bullet_dmg)

        self.gun_chamber: GunChamber = self._generate_chamber()
        self.cur_round: int = kwargs.get("cur_round", default.cur_round)
        self.cur_bullet_index: int = kwargs.get("cur_bullet_index", default.cur_bullet_index)
        self.is_player_turn: int = kwargs.get("is_player_turn", default.is_player_turn)
    
    # Looping the game until any player reach 0 HP
    def run_game(self):
        self._print_round_header()
        
        # TODO: add delays
        while self.ai_hp > 0 and self.player_hp > 0:
            # Reset the round if there are no more bullet
            if self.cur_bullet_index >= self.total_bullet_count:
                self._reset_round()
                
            self._display_game_status()
            self._get_action()
            
            # Increment bullet index
            self.cur_bullet_index += 1
        
        self._end_game()

    def _get_action(self):
        while True:
            # Check whose turn it is currently
            if self.is_player_turn:
                choice = input("Choose action - [1] Shoot opponent / [-1] Shoot self: ")
            else:
                choice = self._get_ai_decision()
            
            # Handle the shooting target
            if choice == "1":
                print("Shoot opponent selected")
                self._shoot_opponent()
                return
            elif choice == "-1":
                print("Shoot self selected")
                self._shoot_self()
                return
            
            print("Invalid input. Enter 1 or -1")
    
    def _get_ai_decision(self):
        # TODO: write AI algorithm
        return "1"

    def _reset_round(self):
        self.cur_round += 1
        self.cur_bullet_index = 0
        
        self._randomize_bullet_counts()
        self.gun_chamber = self._generate_chamber()
        
        self._print_round_header()
        
    def _randomize_bullet_counts(self):
        # Random total bullet count
        self.total_bullet_count = random.randint(2, 8)

        # Some rules to make sure live bullet count is not too imbalance
        min_lives = max(math.floor(self.total_bullet_count * 0.45), 1) # floor(2 * 0.45) == 0 so include 1 to make sure there is always live bullet
        max_lives = math.floor(self.total_bullet_count * 0.65)
        
        # Random live bullet count
        self.live_bullet_count = random.randint(min_lives, max_lives)

    # Generate new chamber
    def _generate_chamber(self):
        # Add the live bullets to the chamber and fill the rest with blank bullets
        # (live = 1, blank = 0)
        array = [1] * self.live_bullet_count
        array.extend([0] * (self.total_bullet_count - self.live_bullet_count))
        
        # Shuffle the bullets in the chamber and create an object to store the array
        random.shuffle(array)
        chamber = GunChamber(bullet_array=array)
        
        return chamber

    def _print_round_header(self):
        print(f"\n=== ROUND {self.cur_round} ===")
        print(f"Chamber: {self.live_bullet_count} lives - {self.total_bullet_count - self.live_bullet_count} blank")

    def _display_game_status(self):
        print(f"\nPlayer HP: {self.player_hp} | AI HP: {self.ai_hp}")
        print(f"Turn: {'Player' if self.is_player_turn else 'AI'}")
        print(f"Known bullets: {self.gun_chamber.bullet_array[:self.cur_bullet_index]}")

    def _end_game(self):
        status = "win" if self.ai_hp == 0 else "lose"
        print(f"You {status}!")

    # Function handling the action of shooting the opponent (by either the player or AI)
    def _shoot_opponent(self):
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
    def _shoot_self(self):
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