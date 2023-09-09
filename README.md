# The Rocket League Gym
This is a python API that can be used to treat the game [Rocket League](https://www.rocketleague.com) as though it were an [OpenAI Gym](https://gym.openai.com)-style environment for Reinforcement Learning projects. This API must be used with the accompanying Bakkesmod plugin.

## Requirements
* A Windows 10 PC
* Rocket League (Both Steam and Epic are supported)
* [Bakkesmod](https://www.bakkesmod.com)
* The RLGym plugin for Bakkesmod (It's installed automatically by pip)
* Python between versions 3.7 and 3.9 (3.10 not supported).

## Installation
Install the library via pip:
```
pip install rlgym[all]  // Installs every rlgym component

pip install rlgym  // Installs only the api

pip install rlgym[rl]  // Installs all rocket league packages

pip install rlgym[rl-sim]  // Installs only RocketSim rocket league packages
```

### If you installed the Rocket League game distribution
Once the API is installed, you will need to enable the RLGym plugin from inside the Bakkesmod plugin manager. To do this, first launch the game, then press F2 to open the Bakkesmod menu. Navigate to the `plugins` tab and open the `Plugin Manager`. From there, scroll down until you find the RLGym plugin, and enable it. Close the game when this is done.


### Testing everything works
RLGym is now installed! simply run ```example.py``` from our repo to ensure everything works.

## Dependency Management
**DO NOT** specify this package as a dependency, this is an **installation only** package.

You should depend directly on the package you're consuming and its corresponding extras, e.g.
`rlgym-rocket-league[sim]`, `rlgym-api` or whichever of our libraries your project is using.

## Usage
For tutorials and documentation, please visit our [Wiki](https://rlgym.org/).

We also provide the base RLGym API in its own [standalone package](https://pypi.org/project/rlgym-api/) with no dependencies.
