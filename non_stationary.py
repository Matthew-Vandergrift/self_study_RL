# Solution to Exercise 2.5 in RL book by Sutton.
import numpy as np
# In Bandit.py, I have implemented the modified version of the 10-armed testbed.
import bandit 
# In incremental_agent I have implemented a sample average agent
import incremental_agent


# Constants for experiment 
EPSILSON = 0.1
STEP_SIZE = 0.1
NUM_STEPS = 10000

if __name__ == '__main__':
    # Creating Environment
    generated_means = np.random.uniform(0, 1, size = 10)
    env = bandit.ModArmedBandit(generated_means)
    # Creating the sample-avergae based agent
    avg_agent = incremental_agent.Agent(10, 0, EPSILSON)
    # Creating the fixed step size based agent
    fix_agent = incremental_agent.ConstStepAgent(10, 0, EPSILSON,STEP_SIZE)
    # Creating Statistics
    total_reward_av = 0
    total_reward_fix = 0
    optimal_action = np.argmax(env.means)
    optimal_action_counts = [0, 0]
    # Experimental Loop
    for s in range(0, NUM_STEPS):
        # Finding Actions
        action_av = avg_agent.act()
        action_fix = fix_agent.act()
        # Taking Actions
        reward_av = env.act(action_av)
        reward_fix = env.act(action_fix)
        # Updating Q values 
        avg_agent.update_q(action_av, reward_av)
        fix_agent.update_q(action_fix, reward_fix)
        # Updating the environment 
        env.update()
        # Updating Stats
        total_reward_av += reward_av
        total_reward_fix += reward_fix 
        if action_av == optimal_action:
            optimal_action_counts[0] += 1
        if action_fix == optimal_action:
            optimal_action_counts[1] += 1 
        optimal_action = np.argmax(env.means)
        
    print("Averaged Reward for Fixed Step Size :", total_reward_fix/NUM_STEPS)
    print("Averaged Reward for Sample Average  :", total_reward_av/NUM_STEPS)
    print("Whole Run percentage of optimal actions for sample average :", optimal_action_counts[0] / NUM_STEPS)
    print("Whole Run percentage of optimal actions for fixed :", optimal_action_counts[1] / NUM_STEPS)
    # Need to make the nice graphs, will do later tonight.