# Implementing Simple Policy Iteration
from mdp import *
import math
class Agent:
    # Our Agent requires a list of states

    def __init__(self, states, discount = 1):
        self.num_states = len(states)
        self.values = [0 for i in states] # Assuming inital guess of 0 for all states
        self.policy = [j for j in states] # First Action at all non terminal states
        for j in range(1, len(states)-1):
            self.policy[j] = states[j].actions[0]
        self.dis = discount
        self.states = states

    def policy_eval(self):
        n = int(math.sqrt(self.num_states))
        delta = 0
        while delta < 0.1:    
            for s in range(0, self.num_states):
                v = self.values[s]
                # Next Value Calc
                next_val = 0
                for sp in [self.policy[s]]: # This assumes non-stochastic policy
                    r = sp.reward
                    gamV = self.dis * self.values[(sp.x-1) * n  + (sp.y-1)]
                    next_val += r + gamV
                # Updating value
                self.values[s] = next_val
                # Checking for dist
                delta = max(delta, abs(v - next_val))
           
    def policy_improv(self):
        n = int(math.sqrt(self.num_states))
        policy_stable = True
        for s in range(1, self.num_states-1):
            old_action = self.policy[s]
            # Computing New Action
            max_val_action = -math.inf
            best_action = old_action
            for a in self.states[s].actions:
                r = a.reward
                gamV = self.dis * self.values[(a.x-1) * n + (a.y-1)] 
                if r + gamV > max_val_action:
                    max_val_action = r + gamV
                    best_action = a
            
            self.policy[s] = best_action
            if best_action != old_action:
                policy_stable = False 
       
        return policy_stable
    
    def policy_iteration(self):
        # Agent does init by itself
        self.policy_eval()
        policy_stable = False 
        while policy_stable == False:
            self.policy_eval()
            policy_stable = self.policy_improv()
        
        return self.policy, self.values


if __name__ == '__main__':
    print("Hello World")
    # Creating Environment
    env = NxNGrid(5, -1, 0)
    # Creating Agent
    ag1 = Agent(env.states)
    # Running Policy Iteration
    opt_policy, opt_values = ag1.policy_iteration()
    # Outputting Policy and Values Nicely 
    counter = 0
    for i in opt_values:
        print(i, end=" | ")
        counter += 1
        if counter == 5:
            print()
            counter = 0