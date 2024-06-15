import numpy as np
# Blackjack Environment as Described on Page 112 on RL: an intro 1st Edition

class BlackJack:
    def __init__(self):
        # Observable Traits for Player
        self.dealer_showing = None
        self.player_sum = 0
        self.player_ace = False
        # Hidden Traits of Env
        self.dealer_sum = None 
        self.player_bust = False
        self.dealer_bust = False
        # Setting up Game
        self.dealer_showing = self.draw()
        self.dealer_sum = self.dealer_showing + self.draw()
        self.player_sum = self.draw() + self.draw()

    # Utility Functions
    def draw(self):
        return min(np.random.randint(1, 14), 10) # Since suits are only worth 10 we take min with 10.

    def dealer_action(self):
        # Assuming Dealer follows the fixed startegy from the book
        dealer_hit = False
        if self.dealer_sum < 17:
            dealer_hit = True
            self.dealer_sum += self.draw()
            if self.dealer_sum > 21:
                self.dealer_bust = True
        return dealer_hit
    
    def __str__(self):
        return "Player Sum is :" + str(self.player_sum) + " Dealer Sum is :" + str(self.dealer_sum)
    # Action Functions 
    def hit(self):
        # Drawing the Card
        card = self.draw()   
        # Adjusting Game State
        if card == 1:
            self.player_ace = True
        self.player_sum += card
        if self.player_sum > 21:
            self.player_bust = True
        return None 
    
    def stick(self):
        return None
    
    def tick(self, action=['hit', 'stick'][0]):
        '''Takes in an action, returns None if game is to be continued and integer reward if game is done'''
        # 'Actions' Occuring
        player_hit = False
        if action == 'hit':
            self.hit()
            player_hit = True 
        else:
            self.stick()
        dealer_hit = self.dealer_action()
        # Calculating Results 
        if self.player_bust == True:
            return -1
        if self.dealer_bust == True:
            return 1 
        if dealer_hit == True or player_hit == True:
            return None
        else:
            if self.player_sum > self.dealer_sum:
                return 1
            elif self.player_sum == self.dealer_sum:
                return 0
            else:
                return -1 

# Testing the Environmnt
if __name__ == '__main__':
    print("Hello World")
    # Setting Seed for Reproducibility (debugging in my case)
    np.random.seed(2)
    # Creating the environment
    env = BlackJack()
    print(env)
    # Trying the actions 
    reward = env.tick('hit')
    print(env)
    print("Reward is :", reward)
    reward = env.tick('stand')
    print(env)
    print("Reward is :", reward)

