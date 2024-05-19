# A simple increment agent from page 32 of RL Book
import bandit
from random import uniform, randint
import numpy as np

class Agent:
    # Num_actions is the number of bandit arms, and init_guess is the first guess for 
    # the q values. epsilon is 1-eps greedy action.  
    def __init__(self, num_actions, init_guess=0, epsilon=0.01):
        self.n_acts = num_actions
        self.q_values = [init_guess] * num_actions
        self.action_counts = [0] * num_actions
        self.eps = epsilon

    # This performs 1-eps greedy action returns the action to be taken
    def act(self):
        r = uniform(0,1)
        if r <= 1-self.eps:
            return np.argmax(self.q_values)
        else:
            return randint(0, self.n_acts-1)
    
    # Updates the q values based on the result of an action
    def update_q(self, action, reward):
        self.action_counts[action] += 1
        self.q_values[action] += 1/self.action_counts[action] * (reward-self.q_values[action])

# This does not assume that the step size if 1/n
class ConstStepAgent(Agent):
    # Adding step size parameter
    def __init__(self,num_actions, init_guess, epsilon, step_size=0.1):
        self.alpha = step_size
        Agent.__init__(self, num_actions, init_guess, epsilon)
    
    def update_q(self, action, reward):
        # Action count is not directly needed, but might be neat to track
        self.action_counts[action] += 1
        self.q_values[action] += self.alpha * (reward-self.q_values[action])


# In main we have the agent interact for 1000 steps with the environment. 
if __name__ == '__main__':
    # Generating means from N(0,1)
    generated_means = np.random.uniform(0, 1, size = 10)
    # Creating 'environment' instance 
    env = bandit.ArmedBandit(generated_means)
    num_steps = 1000
    # Creating the 'agent' instance
    ag = Agent(10, 0, 0.1)
    # Statistics being Set-Up
    total_reward = 0
    optimal_action_index = np.argmax(generated_means)
    optimal_action = 0 
    last_five = []
    # Interaction Loop
    for s in range(0, num_steps):
        # Taking action
        action = ag.act()
        reward = env.act(action)
        # Updating q value
        ag.update_q(action, reward)
        # Updating Stats
        total_reward += reward
        if action == optimal_action_index:
            optimal_action += 1
        if s >= num_steps - 5:
            last_five.append(action)
    
    # Averaged over the course of a single run. 
    print("Percentage of times optimal action taken: ", str(optimal_action/num_steps * 100)+"%")
    print("Average Reward after 1000 Steps: ", total_reward/num_steps)
    print("Last 5 Actions taken: ", last_five, " optimal action :", optimal_action_index)