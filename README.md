# The Rocket League Gym
This is a python API that can be used to treat the game [Rocket League](https://www.rocketleague.com) as though it were an [Openai Gym](https://gym.openai.com)-style environment for Reinforcement Learning projects. This API must be used with the accompanying Bakkesmod plugin.

## Requirements
* A Windows 10 PC
* The Steam version of Rocket League
* [Bakkesmod](https://www.bakkesmod.com)
* The RLGym plugin for Bakkesmod
* Python >= 3.7

## Installation
Install the dependencies via the following pip commands:
```
pip3 install gym==0.17.2
pip3 install pywin32==228
pip3 install pywinauto==0.6.8
pip3 install numpy==1.19.2
```
Then simply clone this repository and run ```example.py``` to ensure everything works.

## Usage
To run a premade environment, call ```rlgym.make``` with the name of the environment you would like to create.
For example, the following code will create an instance of the Duels environment:
```python
import rlgym
env = rlgym.make("Duel")
```
If you would like to build any environment with self-play enabled, include the keyword "self" (not case sensitive) in the name of the environment, like so:
```python
import rlgym
env = rlgym.make("DuelSelf")
```
RLGym comes with 4 pre-made environments:
* Rhobot
* Duels
* Doubles
* Standard

Each can be instantiated by calling ```rlgym.make``` with the name of the environment you would like to create. However, RLGym provides you the ability to create your own environments with a number of potential configurations. For more information on how to build a custom RLGym environment, please visit our Wiki.
