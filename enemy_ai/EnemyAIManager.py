import random

class EnemyAIManager():
    def decide_target(self, ai_hp, player_hp, bullet_remain, live_remain, bullet_array, cur_index):
        print(f"Lives: {live_remain} | Blanks: {bullet_remain - live_remain}")
        
        # Return 1 indicates shooting the player, return -1 indicates shooting self
        SHOOT_OPP = "1"
        SHOOT_SELF = "-1" 

        # AI properties - default numeric values of how AI evaluates actions
        # https://www.desmos.com/calculator/ndivsmalpq
        VALUE_OF_DAMAGING_PLAYER = 0.4
        VALUE_OF_FREE_TURN = 0.4
        COST_OF_WASTING_TURN = -0.1
        COST_OF_TAKING_DAMAGE = -0.1
        
        # SPECIAL CASES - override everything else
        # Only live round remains
        if live_remain == bullet_remain:
            return SHOOT_OPP

        # Only blank round remains -> always shoot self
        if live_remain == 0:
            return SHOOT_SELF

        # AGGRESSIVE MODE - triggers if meet any of the following conditions:
        if (
            ai_hp == 1 or player_hp == 1 # AI or Player is at 1 HP
            or abs(ai_hp - player_hp) >= 2 # any player has health advantage
            or bullet_array[cur_index - 2] == bullet_array[cur_index -1] == 0 # last 2 bullets was blank
        ):
            # Adjust numeric constants to skew towards shooting opponent
            # https://www.desmos.com/calculator/fauwf91wkk
            VALUE_OF_DAMAGING_PLAYER = 0.4
            VALUE_OF_FREE_TURN = 0.15
            COST_OF_WASTING_TURN = -0.05
            COST_OF_TAKING_DAMAGE = -0.05

        # DECISON FRAMEWORK
        # Calculate each bullet probability
        p_live = live_remain / bullet_remain
        p_blank = (bullet_remain - live_remain) / bullet_remain # p_blank = 1 - p_live
        print(f"p_live = {p_live:.2f} | p_blank = {p_blank:.2f}")

        # Calculate EV score of each action
        ev_shoot_opponent = (p_live * VALUE_OF_DAMAGING_PLAYER) + (p_blank * COST_OF_WASTING_TURN)
        ev_shoot_self = (p_blank * VALUE_OF_FREE_TURN) + (p_live * COST_OF_TAKING_DAMAGE)
        print(f"ev_shoot_opponent = {ev_shoot_opponent:.2f} | ev_shoot_self = {ev_shoot_self:.2f}")
        
        # Decide the action
        # If only one action is bad (only one EV score is negative), pick the positive option
        if ev_shoot_opponent < 0 or ev_shoot_self < 0:
            return SHOOT_OPP if ev_shoot_opponent > ev_shoot_self else SHOOT_SELF
        
        # If both actions are good (both EV scores are positive), roll the action using a weighted system
        else:
            shoot_opponent_weight = int(ev_shoot_opponent * 1000)
            shoot_self_weight = int(ev_shoot_self * 1000)
            total_weight = shoot_opponent_weight + shoot_self_weight
            print(f"shoot_opponent_weight = {shoot_opponent_weight} | shoot_self_weight = {shoot_self_weight}")
            
            roll = random.randint(0, total_weight)
            if roll < shoot_opponent_weight:
                return SHOOT_OPP
            else:
                return SHOOT_SELF