
import torch
import random
import numpy as np
from collections import deque
from game import SpriteGame, Point
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.hor - 6, head.ver)
        point_r = Point(head.hor + 6, head.ver)
        point_u = Point(head.hor, head.ver - 6)
        point_d = Point(head.hor, head.ver + 6)
        
        # dir_l = game.direction == Direction.LEFT
        # dir_r = game.direction == Direction.RIGHT
        # dir_u = game.direction == Direction.UP
        # dir_d = game.direction == Direction.DOWN
        dir_l = False
        dir_r = False
        dir_u = False
        dir_d = False

        # left
        if game.direction == "horizontal" and game.b == -6:
            dir_l = True
        elif game.direction == "horizontal" and game.b == 6:
            dir_r = True
        elif game.direction == "vertical" and game.b == 6:
            dir_u = True
        elif game.direction == "vertical" and game.b == -6:
            dir_d = True
            
            
        state = [
            # Danger straight
            (dir_r and game.is_enemy(point_r)) or 
            (dir_l and game.is_enemy(point_l)) or 
            (dir_u and game.is_enemy(point_u)) or 
            (dir_d and game.is_enemy(point_d)),

            # Danger right
            (dir_u and game.is_enemy(point_r)) or 
            (dir_d and game.is_enemy(point_l)) or 
            (dir_l and game.is_enemy(point_u)) or 
            (dir_r and game.is_enemy(point_d)),

            # Danger left
            (dir_d and game.is_enemy(point_r)) or 
            (dir_u and game.is_enemy(point_l)) or 
            (dir_r and game.is_enemy(point_u)) or 
            (dir_l and game.is_enemy(point_d)),
            
            # Danger down
            (dir_l and game.is_enemy(point_r)) or 
            (dir_r and game.is_enemy(point_l)) or 
            (dir_d and game.is_enemy(point_u)) or 
            (dir_u and game.is_enemy(point_d)),
            
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

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SpriteGame()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.main(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()