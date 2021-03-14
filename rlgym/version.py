# From https://github.com/RLBot/RLBot/blob/master/src/main/python/rlbot/version.py
# Store the version here so:
# 1) we don't load dependencies by storing it in __init__.py
# 2) we can import it in setup.py for the same reason
# 3) we can import it into your module module
# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package

__version__ = '0.1.4'

release_notes = {
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
