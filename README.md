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

### Bellman Equation

NewQ(s,a)

Simplification:

### Deep Q Learning

### Pseudocode of agent
```

Set the "run_only" variable to False

If the "test" argument was received (args.test is True), set "run_only" to True

Initialize empty lists for "plot_scores" and "plot_mean_scores"
Initialize "total_score" to 0
Initialize "record" to 0

Create an instance of the Agent class and store it in the "agent" variable
Create an instance of the SpriteGame class and store it in the "game" variable
Call the "speed()" method of the "game" object with the "run_only" variable as an argument

If "run_only" is False, set debugging to False and sleeping time to 0.00005 using the "debuging()" and "sleeping()" methods of the "game" object

Enter an infinite loop:
    Call the "get_state()" method of the "agent" object with the "game" object as an argument and store the result in "state_old"
    
    Call the "get_action()" method of the "agent" object with "state_old" and "run_only" as arguments and store the result in "final_move"
    
    Call the "play_step()" method of the "game" object with "final_move" as an argument and store the result in "reward", "done", and "score"
    Call the "get_state()" method of the "agent" object with the "game" object as an argument and store the result in "state_new"
    
    If "reward" is greater than 0, print "Reward" and "Score"
    
    Call the "train_short_memory()" method of the "agent" object with "state_old", "final_move", "reward", "state_new", and "done" as arguments
    
    Call the "remember()" method of the "agent" object with "state_old", "final_move", "reward", "state_new", and "done" as arguments
    
    If "done" is True:
        Print "Punish" and "Score"
        Call the "reset()" method of the "game" object
        Increment "n_games" attribute of the "agent" object by 1
        Call the "train_long_memory()" method of the "agent" object
        
        If "score" is greater than "record":
            Set "record" to "score"
            If "run_only" is False, call the "save()" method of the "model" attribute of the "agent" object
        
        Print the current game number, score, and record
        Append "score" to "plot_scores" and update "total_score" by adding "score"
        Calculate the mean score by dividing "total_score" by "n_games" and append it to "plot_mean_scores"
        Call the "plot()" function with "plot_scores" and "plot_mean_scores" as arguments

```

## Results
The Q-Learning algorithm was able to learn an optimal policy for the game, achieving best score 6000 over 5000 episodes.


![alt text](https://github.com/imagesid/AI-Theory-Project/blob/main/result/Figure_77777.png?raw=true)

## Chalenges
- Without boundary, the actor can go everywhere without punishment. It made the state wider. That's why the score wasn't good enough
- There were loop go straight action.
- Too much steps

## Fixing
- Add more exploration epsilon
- Add custom policy to punish loop go straight action
- Add custom policy to punish if the step bigger than 100 steps times by success step (score/100)

## Future work
- Add boundary to the game
- Add more exponents if possible

## Conclusion
Reinforcement Learning with Q-Learning is a powerful technique that can be used to solve a variety of problems, including game playing. This project demonstrates the effectiveness of Q-Learning for game playing and serves as a starting point for exploring other reinforcement learning algorithms and applications.

- Name : Ramadhan Agung Rahmat (아궁라마단)
- Student Number: 72221781

## Images
### Original Game
![alt text](https://github.com/imagesid/AI-Theory-Project/blob/main/result/original-game.png?raw=true)

### Agent Player
[![Watch the video](https://img.youtube.com/vi/T-D1KVIuvjA/maxresdefault.jpg)](https://youtu.be/T-D1KVIuvjA)