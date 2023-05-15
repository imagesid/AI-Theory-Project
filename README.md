# AI-Theory-Project
# Reinforcement Learning for SpriteGame - Q Learning

This project demonstrates the application of Q-Learning algorithm for solving games through reinforcement learning. The objective of the project is to showcase how an agent can learn to make optimal decisions by maximizing its rewards while interacting with the game environment.

## Game Description
The game environment used for this project is SpriteGame. The agent learns to play the game by observing its current state, taking an action based on its learned Q-values, and receiving a reward from the environment. The goal of the game is to get the highest score as possible without touching the enemy.
This game can be downloaded from:
```sh
https://github.com/Bereket-G/Python-simple-GUI-game-with-pygame-module
```
Please note that I tried to do Reinforcement Learning from that code so the game can be played by an agent to get best score.

## Q-Learning Algorithm
Q-Learning is a model-free, off-policy reinforcement learning algorithm used to find the optimal action-selection policy. In Q-Learning, the agent learns the Q-value of a state-action pair, which represents the expected cumulative reward the agent will receive by taking that action in that state and following the optimal policy thereafter. The Q-value is updated iteratively using the Bellman equation until convergence.


## Environtment
I developed this code in Conda Environtment with Python Version 3.10

## Getting Started
To run this project, first clone this repository. Then, install the required dependencies by running the following command:

```sh
pip install -r requirements.txt
```

Next, navigate to the game environment file and run the game using:

```sh
python sprite.py
```

The Q-Learning agent can be trained by running the following command:

```sh
python agent.py
```

Once the agent is trained, it can be tested by running:

```sh
python agent.py -t
```

To run the best model we've trained, run the following command:

```sh
python agent.py -t -b
```
## Model In Detail

### Reward & Punishment
- Eat Food = +10
- Hit Enemy = -10
- Else = 0

### Actions
These actions will be used by an agent to explore the game
```sh
[1,0,0,0] = Up
[0,1,0,0] = Right 
[0,0,1,0] = Left 
[0,0,0,1] = Down
```
### State
I put 14 states in this project.
```sh
[
    is_horizontal_movement(),
    is_vertical_movement(),

    is_enemy_in_front(),
    is_enemy_in_right(),
    is_enemy_in_left(),
    is_enemy_in_back(),

    is_direction_left(),
    is_direction_right(),
    is_direction_up(),
    is_direction_down(),

    is_food_left(),
    is_food_right(),
    is_food_up(),
    is_food_down(),
]
```
Example: 
```sh
[0,1, 1,0,0,0, 0,0,1,0, 1,0,1,0]
```

### Model
We use Q-Learning Algorithm with this detail:
- Input Layer = 14 
- Hidden Layer = 256
- Output Layer = 4

![alt text](https://github.com/imagesid/AI-Theory-Project/blob/main/result/mynn.png?raw=true)

And we get the biggest value of the output layer as an action.
Example: 
```sh
[2.6, 5.4, 1.5, 0.2] => [0, 1, 0, 0] #go right
```

## Results
The Q-Learning algorithm was able to learn an optimal policy for the game, achieving best score 6000 over 5000 episodes.


![alt text](https://github.com/imagesid/AI-Theory-Project/blob/main/result/Figure_77777.png?raw=true)


## Conclusion
Reinforcement Learning with Q-Learning is a powerful technique that can be used to solve a variety of problems, including game playing. This project demonstrates the effectiveness of Q-Learning for game playing and serves as a starting point for exploring other reinforcement learning algorithms and applications.
