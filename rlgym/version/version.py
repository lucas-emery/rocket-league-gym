
__version__ = '2.0.0'


# TODO consume subpackages instead?
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
    - Added rl-rlviser install recipe
    - Removed rl-game install recipe
    API changes:
        - Updated docstrings
    Rocket League changes:
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
    API changes:
        - Added SharedInfoProvider API
        - DoneConditions are now optional
        - Now every config object also receives the AgentID list during reset
        - ObsBuilder and ActionParser now have unique types for their SpaceTypes
    Rocket League changes:
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
    - Fixed Python <3.9 install
    API changes:
        - Added shared_info param to TransitionEngine and Renderer
        - Move rlgym.api.engine to rlgym.api.config
    RocketLeague changes:
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
