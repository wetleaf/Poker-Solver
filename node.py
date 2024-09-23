import numpy as np
import constant as c

class InformationNode():

    def __init__(self,key) -> None:
        
        self.key = key
        self.strategy = np.repeat(1/c.N_ACTIONS, c.N_ACTIONS)
        self.regret_sum = np.zeros(c.N_ACTIONS)
        self.strategy_sum = np.zeros(c.N_ACTIONS)
        self.reach_pr = 0
        self.reach_pr_sum = 0

    
    def next_strategy(self):

        self.strategy_sum += self.reach_pr* self.strategy
        self.strategy = self.calc_strategy()
        self.reach_pr_sum += self.reach_pr
        self.reach_pr = 0

    
    def calc_strategy(self):

        strategy =  np.where(self.regret_sum > 0, self.regret_sum, 0)
        total = sum(strategy)

        if total > 0:
            return strategy/total
        else:
            return np.repeat(1/c.N_ACTIONS, c.N_ACTIONS)

    def calc_average_strategy(self):

        strategy = self.strategy_sum / self.reach_pr_sum

        # Purify to remove actions that are likely a mistake
        strategy = np.where(strategy < 0.001, 0, strategy)

        # Re-normalize
        total = sum(strategy)
        strategy /= total

        return strategy

    def display_strategy(self):

        strategy = self.calc_average_strategy()
        print("{} [{:03.2f},{:03.2f}]".format(self.key.ljust(6), strategy[0], strategy[1]))
        
    
    