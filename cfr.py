import numpy as np
import constant as c
from node import InformationNode

def GameStart(info_map: dict):

    expected = 0

    for card_1 in range(c.N_CARDS):
        for card_2 in range(c.N_CARDS):

            if card_1 != card_2:
                history = "rr"

                expected += CounterFactualRM(info_map, history, card_1, card_2, 1, 1, 1/c.N_POSSIBILITIES)

    return expected/c.N_POSSIBILITIES 

def is_terminal(history: str):

    if history in ["rrpp","rrpbp","rrpbb","rrbp","rrbb"]:
        return True
    return False

def terminal_util(history, card_1, card_2):

    player_card = card_1 if len(history)%2 == 0 else card_2
    opponent_card = card_2 if len(history)%2 == 0 else card_1

    if history in ["rrpbb", "rrbb"]:

        return 2 if player_card > opponent_card else -2
    
    elif history == "rrpp":

        return 1 if player_card > opponent_card else -1

    return 1

def get_key(history, card_1, card_2):

    player_card = card_1 if len(history)%2 == 0 else card_2
    key = "{} ".format(c.CARDS[player_card]) + history
    return key

def CounterFactualRM(info_map, history, card_1, card_2, pr_1, pr_2, pr_c):

    if is_terminal(history):
        return terminal_util(history, card_1, card_2)
    
    key = get_key(history,card_1,card_2)

    if key not in info_map.keys():
        info_map[key] = InformationNode(key)
        
    is_player_1 = 1 if len(history)%2 == 0 else 0

    if is_player_1:
        info_map[key].reach_pr += pr_1

    else:
        info_map[key].reach_pr += pr_2
 

    actions_util = np.zeros(c.N_ACTIONS)
    strategy = info_map[key].strategy

    for idx,act in enumerate(c.ACTIONS):

        new_history = history + act

        if is_player_1:
            actions_util[idx] = -1* CounterFactualRM(info_map, new_history, card_1, card_2, pr_1* strategy[idx], pr_2, pr_c)
        
        else:
            actions_util[idx] = -1* CounterFactualRM(info_map, new_history, card_1, card_2, pr_1, pr_2* strategy[idx], pr_c)


    util = sum(actions_util * strategy)
    regret = actions_util - util

    if is_player_1:
        info_map[key].regret_sum += pr_2 * pr_c * regret

    else:
        info_map[key].regret_sum += pr_1 * pr_c * regret

    return util