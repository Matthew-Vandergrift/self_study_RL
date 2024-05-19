# Straightforward 10-armed banit simulator for my RL self-study. 
# Later on will use more advanced libraries for envs. 
import numpy as np

class ArmedBandit:
    # Arguments: mean_rewards = [q*(a_1), ... , q*(a_N)] where N is the number of bandits
    #          : std_rewards = [std_1, ... , std_N] defaults to 1 when nothing passed
    def __init__(self, mean_rewards, std_rewards=None):
        # Setting up the number of bandits
        self.n_bandits = len(mean_rewards)
        # Setting up the mean rewards
        self.means = mean_rewards
        # Setting up standard deviations 
        if std_rewards == None:
            self.std = [1] * self.n_bandits
        else:
            self.std = std_rewards
        # Setting up a tracker for number of actions taken
        self.action_counter = 0


    # Actions are indexed 0, ..., N-1 
    def act(self, action):    
        reward = np.random.normal(self.means[action], self.std[action], size=1)[0]
        self.action_counter += 1
        return reward

# This is described on page 33 of the RL book 
class ModArmedBandit(ArmedBandit):
    # Including a parameter for changed means by walk
    def __init__(self, generated_means, step=0):
        ArmedBandit.__init__(self,generated_means)
        self.step = step
        # It says that all means start equal 
        self.means= [self.means[1]] * self.n_bandits 
    
    def update(self):
        self.step += 1
        # Generating update to means via random walk
        incr = np.random.normal(0, 0.01, size=self.n_bandits)
        # Updating means
        self.means = np.add(self.means, incr)

    



if __name__ == '__main__':
    # Chosing number of bandits
    num_bandits = 10
    # Generating random means from N(0,1)
    generated_means = np.random.uniform(0, 1, size = num_bandits)
    # Creating 'environment' instance 
    env = ArmedBandit(generated_means)
    
    for i in range(0, 9):
        print(env.act(i))