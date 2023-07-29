# From https://github.com/RLBot/RLBot/blob/master/src/main/python/rlbot/version.py
# Store the version here so:
# 1) we don't load dependencies by storing it in __init__.py
# 2) we can import it in setup.py for the same reason
# 3) we can import it into your module module
# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package

__version__ = '1.2.2'

release_notes = {
    'beta':
    """
    - This version contains numerous untested and potentially breaking changes. Run at your own risk.
    """,
    '1.2.2':
    """
    - Fixed max python version
    """,
    '1.2.1':
    """
    - Fixed epic version crashing instantly - Bakkes
    - Added max python version
    - Added ActionParser to utils submodule
    - Updated default reward, it now minimizes linear velocity instead of angular
    - RIP RhobotObs
    """,
    '1.2.0': """
    - Deprecated self_play flag, playing against Psyonix agents is no longer supported
    - Added has_jump to PlayerData, which is useful to detect when a flip won't run out
    - Added pre_step() function to ObsBuilder and RewardFunction, useful for pre-calculating stuff each step
    - Added support for changing gamemode without restarting RLGym, see StateSetter.build_wrapper()
    - Added gravity and boost_consumption configuration to rlgym.make()
    - Added update_settings() method to gym, for updating some parts of the config without restarting
    - Added get_obs_space() to ObsBuilder, enables overriding RLGym's automatic obs size detection
    - Added raise_on_crash option to rlgym.make()
    - Added auto_minimize option to rlgym.make()
    - Added boost pickups to event reward - yadaraf
    - Fixed custom bin support in DiscreteAction - Kaiyotech
    - Fixed bug in VelocityBallToGoalReward and VelocityPlayerToBallReward
    - Fixed PlayerData string representation - Carrot
    """,
    '1.1.0': """
    - Added ActionParsers, which allow you to define custom action spaces - Lolaapk3
    - Fixed quaternion to euler angle conversion - Darxeal
    - Improved DefaultObs, it now has all the state information
    - Added optional parameter to return initial info object on env.reset()
    - Fixed rand_vec3 so the magnitude is actually random
    """,
    '1.0.2': """
    - Fixed state setting issues (boost setting and precision)
    """,
    '1.0.1': """
    - Minor fix for RandomState
    """,
    '1.0.0': """
    - Added state setting, you can now specify the initial state of episodes via a StateSetter object - aiTan
    - Added launch_preference to make()
    - Fixed Epic launch bug introduced with the Season 4 update
    - Communication code refactored to increase performance with low tick_skip
    - Fixed boost pad reset bug on episode reset
    - Added detection mechanism for ghost ball bug
    - Decreased required access rights by the MultiInjector
    """,
    '0.6.0': """
    - Moved wrappers and replay converter to rlgym-tools package
    - Added the optional ability to forcefully page the spawned Rocket League instances upon creation - 416c616e
    - The path_to_rl param is no longer required for use_injector
    """,
    '0.5.0': """
    - Removed string based configurations in rlgym.make(), everything is passed by kwargs now - Soren
    - Added StableBaselines3 compatibility - Rolv
    - Refactored and expanded reward functions - Rolv
    - Added replay converter - Rolv
    - Fixed TouchBallReward bug - Kevin

    NOTE: Some of these new tools (wrappers, replay converter, etc) will be moved to a different package in the next release
    """,
    '0.4.1': """
    - Updated euler angles to match rlbot [pitch, yaw, roll] and added accessor functions
    - Bugfix: player.is_alive renamed to is_demoed
    - Added common rewards - Rolv
    - Added a reward combiner - Chainso
    - Added missing kickoff spawn
    - Fixed 2v2 and 3v3 action delivery
    - Fixed issue in 2v2 and 3v3 where blue bots would disappear over time
    - Added multi injector
    """,
    '0.4.0': """
    - Major API refactor
    - Added boostpad boolean array to GameState
    - RLGym is now baselines compatible
    - Added improved Default configuration
    """,
    '0.3.0': """
    - Pass initial state to env components on gym.reset()
    - Pass prev action to reward fn
    - info returned from gym.step() is now a Dict
    - Fixed obs size bug in RhobotObs
    """,
    '0.2.0': """
    - Switched from custom_args dict to keyword args in rlgym.make()
    """,
    '0.1.4': """
    - Gym now inherits openai.gym.Env - Chainso
    - Fixed bug where rlgym crashed trying to parse the state string in some scenarios
    """,
    '0.1.3': """
    - Renamed PhysicsObject.orientation to euler_angles
    - euler_angles is now a function so they aren't calculated if not needed
    - Added rotation_mtx, forward, right and up vectors to PhysicsObject (only usable for the car)
    - Removed conversion to np array for rewards and observations
    - Fixed bug in RhobotObs
    """,
    '0.1.2': """
    - Obs are now numpy arrays
    - Added types to core classes to make customization easier
    - Fixed bakkesmod bug
    """,
    '0.1.1': """
    Added missing scipy dependency
    """,
    '0.1.0': """
    Initial Release
    """
}


def get_current_release_notes():
    if __version__ in release_notes:
        return release_notes[__version__]
    return ''


def print_current_release_notes():
    print(f"Version {__version__}")
    print(get_current_release_notes())
    print("")