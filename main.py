import constant as c
from cfr import GameStart

def main():

    info_map = {}
    expected_value = 0

    for _ in range(c.N_ITERATIONS):
        expected_value += GameStart(info_map)

        for _,val in info_map.items():
            val.next_strategy()
    

    for _,val in info_map.items():
        
        val.calc_average_strategy()

    print("Player 1 strategies: ")
    for key,val in info_map.items():

        if len(key)%2 == 0:
            val.display_strategy()
    
    print("\nPlayer 2 strategies: ")
    for key,val in info_map.items():
        
        if len(key)%2 != 0:
            val.display_strategy()
        
    return expected_value/c.N_ITERATIONS

if __name__ == "__main__":
    EV = main()
    print("\nPlayer 1 EV: ",EV)
    print("Player 2 EV: ",-1*EV)