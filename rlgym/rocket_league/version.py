
__version__ = '2.0.0'


def get_current_release_notes():
    if __version__ in release_notes:
        return release_notes[__version__]
    return ''


def print_current_release_notes():
    print(f"Version {__version__}")
    print(get_current_release_notes())
    print("")


release_notes = {
    '2.0.0':
    """
    - Renamed timeout parameter of default DoneConditions to timeout_seconds
    - Added Car.wheels_with_contact
    - Added Car.has_flip
    - Changed Car.boost_amount range from [0, 1] to [0, 100]
    - Added boost_coef to DefaultObs
    - Added rlbot_delay parameter to RocketSimEngine which emulates RLBot's 1-tick action delay, default is True!!
        - rlbot_delay can be updated during runtime via RocketSimEngine.config
    - Updated RocketSimEngine to use new flip_rel_torque
    - Updated RocketSimEngine to set is_demoed and is_flipping as well
    - Updated RocketSimEngine's goal threshold (still only supports Soccar)
    - Updated docstrings
    - Updated KickoffMutator's ball resting position to the correct value
    - Renamed some stuff in rlgym.rocket_league.math [Rolv]
    - Removed rocket-league game package
    """,
    '2.0.0-rc':
    """
    - Updated RocketSim and RLViser dependencies [Virx]
    - Added Ball RotMtx to RocketSim engine and RLViser renderer [Virx]
    - Fixed bump victim ID in RocketSim engine [Lamp]
    - Added more useful constants to common_values
    - Removed RLViser dependency from sim install
    - Improved RepeatAction, it now doesn't expect your ActionParser to handle multiple ticks
    - Improved default ObsSpace and ActionSpace definitions
    """,
    '2.0.0-alpha-3':
    """
    - This version contains numerous untested and breaking changes. Run at your own risk.
    - Added shared_info param to TransitionEngine and Renderer
    - Fixed Python <3.9 install
    - Update imports to rlgym.api
    - Rename rlgym.rocket_league.engine to rlgym.rocket_league.api
    - Improve exports so imports are more consolidated
    """,
    '2.0.0-alpha-2':
    """
    - This version contains numerous untested and potentially breaking changes. Run at your own risk.
    - Fixed rlviser-py dependency version
    """,
    '2.0.0-alpha-1':
    """
    - This version contains numerous untested and potentially breaking changes. Run at your own risk.
    - Lifted Python <3.10 restriction
    """,
    '2.0.0-alpha':
    """
    - This version contains numerous untested and breaking changes. Run at your own risk.
    """
}
