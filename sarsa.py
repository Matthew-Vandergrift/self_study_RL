import numpy as np
from blackjack import BlackJack
import itertools
from random import choice

# This is a sarsa agent following the algorithm from RL: an introduction by Sutton and Bareto. 
# We (I) are designing this explicity for the poker env so it doesn't take in an arbitrary MDP, 
# could be made to do so easily just for simplicity.  
class Agent:

    def __init__(self, discount = 0.9, step = 1, eps = 0.01):
        # Setting up the agent's hyper parameters
        self.eps = eps
        self.step = step
        self.discount = discount
        # Cartesian Product of these Lists is the state space
        player_sums = [i for i in range(1, 22)]
        dealer_card = [i for i in range(1, 11)]
        usable_ace = [True, False]
        self.actions = ['hit', 'stick']
        #states = itertools.product(player_sums, dealer_card, usable_ace)
        state_actions = itertools.product(player_sums, dealer_card, usable_ace, self.actions)

        self.q_vals = {}
        for i in state_actions:
            print("State Action is represented as :", i)
            self.q_vals[i] = 0

    def control(self):
        for frw in range(0, 10000):
            # Init S
            env = BlackJack()
            S = env.get_state()
            # Choose A from S using 1-e greedy from Q
            rnd_num = np.random.uniform(0,1)
            if rnd_num < 1 - self.eps:
                options = [self.q_vals[S+(a,)] for a in self.actions]
                best_option_index = np.argmax(options)
                action = self.actions[best_option_index]
            else:
                action = choice(self.actions)
            # Looping while not at Terminal
            reward = None
            while reward == None:
                # Taking Action A
                reward = env.tick(action)
                s_p = env.get_state()
                is_terminal = (reward == 1 or reward == -1)
                # Choosing A` from S` via (1-e) greedy, with a clumsy way to handle terminal q(s,a)
                if is_terminal == True:
                    self.q_vals[S+(action,)] += self.step * (reward + (self.discount*0 - self.q_vals[S+(action,)]))
                else:
                    rnd_num = np.random.uniform(0,1)
                    if rnd_num < 1 - self.eps:
                        options = [self.q_vals[s_p+(a,)] for a in self.actions]
                        best_option_index = np.argmax(options)
                        a_p = self.actions[best_option_index]
                    else:
                        a_p = choice(self.actions)
                    # Doing Update to Q Values
                    if reward == None:
                        reward = 0
                    self.q_vals[S+(action,)] += self.step * (reward + (self.discount*self.q_vals[s_p + (a_p,)] - self.q_vals[S+(action,)]))
                    # Updating vars for future loops
                    S = s_p
                    action = a_p
        print("Q values are :", self.q_vals)

if __name__ == '__main__':
    print("Hello World")
    ag = Agent()
    ag.control()
        