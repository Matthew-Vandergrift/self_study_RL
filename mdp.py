import random
# Class for a state in an MDP. Assumes that each state has set of actions 
# and that each state gives some reward
class State:
    def __init__(self, next_states, reward, name='state'):
        self.actions = next_states
        self.name = name
        self.reward = reward

    def __str__(self):
        return str(self.name)

# Class for N by N Gridworld with State 0-0 being at the top left, N-N being bottom right. 
# Both are terminal states
class NxNGrid: 
    def __init__(self, n, reward_non_terminal, final_reward=0):
        states = []
        for i in range(1, n+1):
            for j in range(1, n+1):
                if (i != 1 or j !=1) and (i != n or j!= n):
                    states.append(State(next_states=[], reward=reward_non_terminal, name='State'+str(i)+str(j)))
                else:
                    states.append(State(next_states=[], reward=final_reward, name='Terminal'+str(i)))
            
        # Using row-major ordering to add the cardinal directions as successor states.
        for index in range(0, len(states)):
            i = (int) (index / n)
            j = index - i*(n)

            up = min(max(j-1, 0),n-1)
            down = min(max(j+1, 0),n-1)
            left = min(max(i-1, 0),n-1)
            right = min(max(i+1, 0),n-1)

            states[index].actions = [states[i * n + up], states[i*n + down], states[left*n + j], states[right*n + j]]

            self.states = states

    def get_start(self):
        starter = random.choice(self.states)
        if 'Terminal' not in starter.name:
            return starter
        else:
            return self.get_start()

if __name__ == '__main__':
    # Creating the world
    four_grid = NxNGrid(4, -1, 0)
    # Getting Starting State
    start = four_grid.get_start()
    print("Starting State :", start)
    # Viewing Actions from a state 
    curr_actions = start.actions
    print("Current Actions")
    for i in curr_actions:
        print(i)
