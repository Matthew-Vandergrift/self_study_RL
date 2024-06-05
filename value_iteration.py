# Implementing Value Iteration for GridWorld
from grid_world import *
import math
import numpy as np
import random 
class Agent:
    def __init__(self, states, discount=1):
        self.states = states
        self.dis = discount
        self.num_states = len(states)
        self.n = int(math.sqrt(self.num_states))
        self.policy = [j for j in states] # First Action at all non terminal states
        for j in range(1, len(states)-1):
            self.policy[j] = random.choice(states[j].actions)
        self.values = [0 for i in states] # 0 for all states. 

    def value_iterate(self, eps=0.01):
        delta = math.inf
        while(delta > eps):
            delta=0
            for s in range(0, self.num_states):
                v = self.values[s]
                #print("At State :", self.states[s], "current value :", self.values[s])
                # Computing new Value
                all_actions_vals = []
                for sp in self.states[s].actions:
                    #print("Considering Action :", sp, end="")
                    r = sp.reward
                    gamVal = self.dis * self.values[(sp.x-1)*self.n + (sp.y-1)]
                    #print(" has value :", r+gamVal)
                    all_actions_vals.append((r + gamVal))
                if all_actions_vals == []:
                    self.values[s] = 0
                else:
                    self.values[s] = max(all_actions_vals)
                    delta = max(delta, abs(v - self.values[s]))
        # Printing the Value function for curiosity 
        counter = 0
        for i in self.values:
            print(i, end=" | ")
            counter += 1
            if counter == 4:
                print()
                counter = 0

        # Returning deterministic policy 
        for s in range(0, self.num_states):
            #print("Computing Policy for State :", self.states[s], 'has current policy :', self.policy[s])
            best_action = None
            best_result = -math.inf

            for a in self.states[s].actions:
                #print("Considering Action : ", a, end="")
                r = a.reward
                gamVal = self.dis * self.values[(a.x-1)*self.n + (a.y-1)]
                #print(" has value :", r+gamVal)
                if r+gamVal > best_result:
                    best_result = r+gamVal
                    best_action = a
            #print("Chosen best actions is :", best_action)
            self.policy[s] = best_action
        
        return self.policy, self.values
            



if __name__ == '__main__':
    print("Hello World")
    # Creating Environment
    env = NxNGrid(4, -1, 0)
    # Creating Agent
    ag1 = Agent(env.states)
    # Running Value Iteration
    policy, values = ag1.value_iterate()
    #policy = ag1.policy
    # Outputting Policy in slightly pretty fashion
    counter = 0
    for i in policy:
        print(i, end=" ")
        counter += 1 
        if counter == 4:
            counter = 0     
            print(' ')