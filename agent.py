
import torch
import random
import numpy as np
from collections import deque
from game import SpriteGame, Point
from model import Linear_QNet, QTrainer
from helper import plot
import argparse

#MAX_MEMORY = 100_000
#BATCH_SIZE = 1000
MAX_MEMORY = 10_000_000
BATCH_SIZE = 10000
LR = 0.001

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", dest="test", action="store_true") # Test actor
parser.add_argument("-b", "--best", dest="best", action="store_true") # Load best trained model
args = parser.parse_args()

class Agent:

    def __init__(self):
        self.size = 50
        self.n_games = 0
        self.epsilon = 0 # randomness
        #self.gamma = 0.9 # discount rate
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        #self.model = Linear_QNet(12, 256, 4)
        #fine
        # self.model = Linear_QNet(18, 256, 4)
        self.model = Linear_QNet(14, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        


    def get_state(self, game):
        head = game
        point_l = Point(head.hor - self.size, head.ver)
        point_r = Point(head.hor + self.size, head.ver)
        point_u = Point(head.hor, head.ver - self.size)
        point_d = Point(head.hor, head.ver + self.size)
        
        # dir_l = game.direction == Direction.LEFT
        # dir_r = game.direction == Direction.RIGHT
        # dir_u = game.direction == Direction.UP
        # dir_d = game.direction == Direction.DOWN
        
        
        
        dir_l = False
        dir_r = False
        dir_u = False
        dir_d = False

        # left
        if game.direction == "horizontal" and game.b == -self.size:
            dir_l = True
        elif game.direction == "horizontal" and game.b == self.size:
            dir_r = True
        elif game.direction == "vertical" and game.b == -self.size:
            dir_u = True
        elif game.direction == "vertical" and game.b == self.size:
            dir_d = True
            
        # print("Point r", point_r)    
        # print("game.is_enemy(point_r))", game.is_enemy(point_r))  
        
        # print("Point d", point_d)    
        # print("game.is_enemy(point_d))", game.is_enemy(point_d))   
        # print("game.is_enemy(point_u))", game.is_enemy(point_u))   
        # print("game.is_enemy(point_l))", game.is_enemy(point_l))   
        state = [
            
            # # dir hor
            (game.direction == "horizontal"),
            (game.direction == "vertical"),
            
            # # dir compass (positive, negative)
            # (game.b == self.size),
            # (game.b == -self.size),
            
            # # simple position of enemy
            # game.ene_pos_hor < game.hor,  # food left
            # game.ene_pos_hor > game.hor,  # food right
            # game.ene_pos_ver < game.ver,  # food up
            # game.ene_pos_ver > game.ver,  # food down
            
            # # Danger straight direction
            (dir_r and game.is_enemy(point_r)) or 
            (dir_l and game.is_enemy(point_l)) or 
            (dir_u and game.is_enemy(point_u)) or 
            (dir_d and game.is_enemy(point_d)),

            # Danger right direction
            (dir_u and game.is_enemy(point_r)) or 
            (dir_d and game.is_enemy(point_l)) or 
            (dir_l and game.is_enemy(point_u)) or 
            (dir_r and game.is_enemy(point_d)),

            # Danger left direction
            (dir_d and game.is_enemy(point_r)) or 
            (dir_u and game.is_enemy(point_l)) or 
            (dir_r and game.is_enemy(point_u)) or 
            (dir_l and game.is_enemy(point_d)),
            
            # Danger oposite direction
            (dir_l and game.is_enemy(point_r)) or 
            (dir_r and game.is_enemy(point_l)) or 
            (dir_d and game.is_enemy(point_u)) or 
            (dir_u and game.is_enemy(point_d)),
            
            # ## border
            # # # Danger straight direction
            # (dir_r and game.is_collision(point_r)) or 
            # (dir_l and game.is_collision(point_l)) or 
            # (dir_u and game.is_collision(point_u)) or 
            # (dir_d and game.is_collision(point_d)),

            # # Danger right direction
            # (dir_u and game.is_collision(point_r)) or 
            # (dir_d and game.is_collision(point_l)) or 
            # (dir_l and game.is_collision(point_u)) or 
            # (dir_r and game.is_collision(point_d)),

            # # Danger left direction
            # (dir_d and game.is_collision(point_r)) or 
            # (dir_u and game.is_collision(point_l)) or 
            # (dir_r and game.is_collision(point_u)) or 
            # (dir_l and game.is_collision(point_d)),
            
            # # Danger oposite direction
            # (dir_l and game.is_collision(point_r)) or 
            # (dir_r and game.is_collision(point_l)) or 
            # (dir_d and game.is_collision(point_u)) or 
            # (dir_u and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.ye_hor < game.hor,  # food left
            game.ye_hor > game.hor,  # food right
            game.ye_ver < game.ver,  # food up
            game.ye_ver > game.ver  # food down
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, run_only=False):
        final_move = [0,0,0,0]
        if run_only:
            #current trained
            filename = '2023-05-15.pth'
            if args.best:
                #best trained
                # filename = '14-05-2023-16 copy 2.pth'
                filename = '14-05-2023-16 copy 11.pth'
                
            state0 = torch.tensor(state, dtype=torch.float)
            self.model.load(filename)
            prediction = self.model(state0)
            
            move = torch.argmax(prediction).item()
            final_move[move] = 1

            return final_move
        # random moves: tradeoff exploration / exploitation
        #self.epsilon = 80 - self.n_games
        # working fine
        #self.epsilon = 200 - self.n_games
        self.epsilon = 1000 - self.n_games
        
        if random.randint(0, 200) < self.epsilon:
        #if random.randint(0, 400) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
            #print("Random move")
        else:
            #print("Current best move")
            state0 = torch.tensor(state, dtype=torch.float)
            # print("state0", state0)
            #prediction = self.model(state0)
            prediction = self.model(state0)
            # print("Pred", prediction)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    run_only = False
    if args.test:
        run_only = True
    
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SpriteGame()
    game.speed(run_only)
    
    #add outline
    game.outline=True
    
    if not run_only:
        game.debuging(False)
        game.sleeping(0.00005)
    # game.hor=100
    # game.ver=120
    # game.ene_pos_hor=100
    # game.ene_pos_ver=100
    # state_old = agent.get_state(game)
    # print("Old State", state_old)
    # game.check_display()
    # return 0
    while True:
        # get old state
        state_old = agent.get_state(game)
        #print("Old State", state_old)

        # get move
        final_move = agent.get_action(state_old, run_only)
        #print("Final Move", final_move)
        
        # # check manually
        # reward, game_over, score = game.play_step([0, 1, 0, 0])
        # if game_over == True:
        #     game.showGameOverScreen()
        #     break
        # continue
        
        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        #print("New State", state_new)

        if reward > 0:
            #print("Old State", state_old)
            print("++++++++++ Reward ++++++++++")
            #print(" reward, done, score",  reward, done, score)
            print("Reward", reward)
            print("Score", score)

        
        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            print("---------- Punish -----------")
            #print(" reward, done, score",  reward, done, score)
            print("Punish", reward)
            print("Score", score)
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                if not run_only:
                    # agent.model.save("14-05-2023-16.pth")
                    agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()