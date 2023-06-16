# AI-Theory-Project [REVISION VERSION]
<em><b>Please note</b> that I <b>download the original game</b> and <b>do Reinforcement Learning</b> with it.</em> 



## Updates
- Give a limit to an agent to pass the border. It will die as soon as touching outline
- Add more 4 environtment status such: border in stright, right, left and backward.
- Total, I put 18 states in this project. Detail in below segment
- Set Punishment -10 If Actor Touching Border

## Environment
I developed this code in Conda Environtment with Python Version 3.10

To create conda environment you can run the following command:
```sh
conda create --name agungenv python=3.10
```
After that you can activate the environment with this command:
```sh
conda activate agungenv
```

## Getting Started
To run this project, first clone this repository.
```sh
git clone https://github.com/imagesid/AI-Theory-Project.git
```

Go to the directory by running this command:
```sh
cd AI-Theory-Project
```

Then, install the required dependencies by running the following command:

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
- Hit Border = -10
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
Previously, I put only 14 states, but in this version I put 18 states in this project.
```sh
[
    is_horizontal_movement(),
    is_vertical_movement(),

    is_enemy_in_front(),
    is_enemy_in_right(),
    is_enemy_in_left(),
    is_enemy_in_back(),

    is_border_in_front(),
    is_border_in_right(),
    is_border_in_left(),
    is_border_in_back(),

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
[0,1, 1,0,0,0, 0,1,0,0, 0,0,1,0, 1,0,1,0]
```

### Model
We use Q-Learning Algorithm with this detail:
- Input Layer = 18 
- Hidden Layer = 256
- Output Layer = 4


And we get the biggest value of the output layer as an action.

Example: 
```sh
[2.6, 5.4, 1.5, 0.2] => [0, 1, 0, 0] #go right
```

### Bellman Equation
<p align="center">
<img src='https://www.simplilearn.com/ice9/free_resources_article_thumb/6-bellman.JPG'>
</p>

Simplified rule:

```sh
Q = model.predict(state_0)
Q_new = R + λ . max(Q(state_1))
```

### Pseudocode of Train
Majority of the code will be inside: agent.py and game.py
```

Enter an infinite loop:
    Get current game state

    Get action based on the current game state

    Do a movement in the game based on the action
        Return the reward, game over and score
    
    Get current game state after movement

    If get reward:
        Print the reward and the score
    
    Train short memory for the Agent
    Agent Remember the details of first state, movement, reward, game over status, and new state

    If game over / touching enemy:
        Print the punishment and the score
        Reset the game
        Increase the number of played game
        Train long memory for the Agent
        
        If the score is bigger then the record:
            Set new record
            Save the model

        Append the plot
        Show the plot

```

### Pseudocode of get_state() method
```
Initialize 14 state variables with these values and put it inside a list:
    Set to 1 if current movement is horizontal movement
    Set to 1 if current movement is vertical movement

    Set to 1 if enemy is in the front side
    Set to 1 if enemy is in the right side
    Set to 1 if enemy is in the left side
    Set to 1 if enemy is in the back side

    Set to 1 if border is in the front side
    Set to 1 if border is in the right side
    Set to 1 if border is in the left side
    Set to 1 if border is in the back side

    Set to 1 if current direction is to the left
    Set to 1 if current direction is to the right
    Set to 1 if current direction is to the top
    Set to 1 if current direction is to the bottom

    Set to 1 if food is in the left side
    Set to 1 if food is in the right side
    Set to 1 if food is in the top side
    Set to 1 if food is in the bottom side

Return the values of the state variables

```

### Pseudocode of get_action() method
```
Initialize final_move as a list with 4 values: "[0, 0, 0, 0]"

# Set epsilon for exploration vs exploitation
Initialize epsilon with 1000 minus the number of played games

# If in test mode
If test mode is True:
    # Load model
    If best mode is True:
        Load best model
    Else:
        Load last model

    # Call Torch Prediction
    Call Torch Prediction with current state

    # Change biggest return value index to 1
    Change the index of the biggest return value to 1

    # Return final_move
    Return final_move

# Set and return Random Move
If a random integer between 0 and 200 is lower than epsilon:
    Set final_move to a random move

# Call Torch Prediction
Call Torch Prediction with current state

# Change biggest return value index to 1
Change the index of the biggest return value to 1

# Return final_move
Return final_move

```

### Pseudocode of play_step() method
```
Initialize action from parameter
Set Punishment -10 If Actor Touching Enemy
Set Punishment -10 If Actor Touching Border
Set Punishment -10 If Step more than 100 steps times by success step (score/100)
Set Punishment -10 if There are loop go straight action.
Set Reward +10 If Actor Touching Food

Go Up if action equal [1,0,0,0]
Go Right if action equal [0,1,0,0]
Go Left if action equal [0,0,1,0]
Go Down if action equal [0,0,0,1]

```

### Pseudocode of train_short_memory() method
```
Call the train method with the arguments states, actions, rewards, next_states, and dones
```

### Pseudocode of train_long_memory() method
```
If the length of the memory is greater than BATCH_SIZE:
    Set mini sample as a random sample of size BATCH_SIZE from the memory (a list of tuples)
Else:
    Set mini sample as a copy of the memory

Extract states, actions, rewards, next_states, and dones by unpacking the mini sample tuple

Call the train method with the arguments states, actions, rewards, next_states, and dones
```

### Pseudocode of train_step() method
```
Initialize state as a torch tensor with a float data type
Initialize next_state as a torch tensor with a float data type
Initialize action as a torch tensor with a long data type
Initialize reward as a torch tensor with a float data type

If the length of the shape of state is 1:
    Expand the dimensions of state, next_state, action, reward, and done tensors by adding an additional dimension with value 1

Initialize done as a tuple with a single boolean value

Initialize prediction as the output of the model method called with the argument state

Create a deep copy of prediction and store it in target variable

Iterate over the range of the length of done (game over):
    Set Q_new to the value of reward at the current index
    If not game over at the current index:
        Set Q_new to the sum of reward at the current index and the gamma multiplied by the maximum value of the model method called with next state at the current index
    Set the value of the target tensor at the current index and the index with the maximum value of action at the current index to Q_new

Zero the gradients of the the optimizer

Calculate the loss by calling the criterion method with the arguments target and prediction

Compute gradients of the loss tensor by calling the backward method on the loss tensor

Update the weights of the optimizer by calling the step method on the optimizer.

```

## Results
The previous scheme achieving 3000 best score  in first 2500 episode. In this version we can already get 3000 score in only 1800 episode.

<p align="center">
  <img src="https://github.com/imagesid/AI-Theory-Project/blob/revision/result/yyyyy.png?raw=true" />
</p>


## Conclusion
Reinforcement Learning with Q-Learning is a powerful technique that can be used to solve a variety of problems, including game playing. This project demonstrates the effectiveness of Q-Learning for game playing and serves as a starting point for exploring other reinforcement learning algorithms and applications.

- Name : Ramadhan Agung Rahmat (아궁라마단)
- Student Number: 72221781


