# From https://github.com/RLBot/RLBot/blob/master/src/main/python/rlbot/version.py
# Store the version here so:
# 1) we don't load dependencies by storing it in __init__.py
# 2) we can import it in setup.py for the same reason
# 3) we can import it into your module module
# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package

__version__ = '0.6.0'

release_notes = {
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
    - Fixed issue in 2v2 and 3v3 were blue bots would disappear over time
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
