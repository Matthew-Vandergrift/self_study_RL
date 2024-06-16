import numpy as np 
from blackjack import BlackJack
import itertools
from math import inf

# This is a tabular method 

class Agent:

    def __init__(self):
        # Cartesian Product of these Lists is the state space
        player_sums = [i for i in range(1, 22)]
        dealer_card = [i for i in range(1, 11)]
        usable_ace = [True, False]
        actions = ['hit', 'stick']
        states = itertools.product(player_sums, dealer_card, usable_ace)
        state_actions = itertools.product(player_sums, dealer_card, usable_ace, actions)
        # Initializing all State-Action Pairs to 0 
        self.q_vals = {}
        self.returns = {}
        for i in state_actions:
            self.q_vals[i] = 0
            self.returns[i] = [] # Rewards are init to be an empty list

        # Initailizing Policy. We are starting with the policy to stick only on 20/21
        self.pi = {}
        for i in states:
            if i[0] >= 20:
                self.pi[i] = 'stick'
            else:
                self.pi[i] = 'hit'
        

    def generate_episode(self, env):
        '''Returns an epsisode as two lists [(s,a)] and [r]'''
        # Using the self pi variable for the policy followed
        episode = []
        return_sequence = []
        states = set([])
        returns = None
        while returns == None:
            state = env.get_state()
            states.add(state)
            action_to_take = self.pi[state]
            # Taking Action
            returns = env.tick(action_to_take)
            episode.append(state + (action_to_take,))
            if returns == None:
                return_sequence.append(0)
            else:
                return_sequence.append(returns)

        return episode, return_sequence, states


    def control(self):
        # Since we obviously cannot go forever
        for frv in range(0, 1000):
            # Step a)
            env = BlackJack() 
            sa_pairs, returns, states = self.generate_episode(env)
            sa_pairs_unique =  list(set(sa_pairs))
            # Step b) 
            for sa in sa_pairs_unique:
                first_visit_index = sa_pairs.index(sa)
                returns_following_sa = returns[first_visit_index:]
                self.returns[sa] += returns_following_sa
                self.q_vals[sa] = np.average(self.returns[sa])
            # Step c)
            for s in states:
                max_action = self.pi[s]
                max_q = self.q_vals[s + (max_action,)]
                for a in ['hit', 'stick']:
                    if self.q_vals[s + (a,)] > max_q:
                        max_action = a
                        max_q = self.q_vals[s + (a,)]
                self.pi[s] = max_action
                     
        return None




if __name__ == '__main__':
    print("Hello World")
    # Creating the Environment
    env = BlackJack()
    # Creating the Agent 
    ag = Agent()
    
    # Testing the control algorithm 
    ag.control()
    print(ag.pi)

    # # Testing the generation of an episode
    # np.random.seed(1) 
    # print(env)
    # sa, r, s = ag.generate_episode()
    # print(sa)
    # print(r)
    # print(s)
    # sa, r, s = ag.generate_episode()