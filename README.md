# The Rocket League Gym
This is a python API that can be used to treat the game [Rocket League](https://www.rocketleague.com) as though it were an 
[Gym](https://gymnasium.farama.org/)-style environment for Reinforcement Learning projects. 


## Installation
Install the library via pip:
```
pip install rlgym[all]  // Installs every rlgym component

pip install rlgym  // Installs only the api

pip install rlgym[rl]  // Installs all rocket league packages

pip install rlgym[rl-sim]  // Installs only RocketSim rocket league packages

pip install rlgym[rl-rlviser]  // Installs RLViser and RocketSim rocket league packages
```

### Testing everything works
RLGym is now installed! simply run ```example.py``` from our repo to ensure everything works.

## Dependency Management
**DO NOT** specify this package as a dependency, this is an **installation only** package.

You should depend directly on the package you're consuming and its corresponding extras, e.g.
`rlgym-rocket-league[sim]`, `rlgym-api` or whichever of our libraries your project is using.

## Usage
For tutorials and documentation, please visit our [Wiki](https://rlgym.org/).

We also provide the base RLGym API in its own [standalone package](https://pypi.org/project/rlgym-api/) with no dependencies.
