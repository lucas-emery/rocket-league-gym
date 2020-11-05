from rlgym.utils.obs_builders import ObsBuilder
from rlgym.utils import CommonValues


class RhobotObs(ObsBuilder):
    def __init__(self):
        super().__init__()
        self.obs_size = 52

    def reset(self, optional_data=None):
        pass

    #Not supported.
    def build_obs(self, state, optional_data=None):
        return None

    def build_obs_for_player(self, player, state, optional_data=None):
        prev_actions = optional_data
        if prev_actions is None:
            print("ATTEMPTED TO BUILD RHOBOT OBS WITH NO PREV ACTIONS ARGUMENT!")
            raise ArithmeticError

        players = state.players
        if player.team_num == CommonValues.ORANGE_TEAM:
            player_car = player.inverted_car_data
            ball = state.inv_ball
        else:
            player_car = player.car_data
            ball = state.ball

        ob = [arg for arg in prev_actions]
        ob.append(player.has_flip)
        ob.append(player.boost_amount)
        ob.append(player.on_ground)

        ob += player_car.serialize()
        ob += ball.position
        ob += ball.linear_velocity
        ob += ball.angular_velocity

        ob += CommonValues.ORANGE_GOAL_CENTER
        ob += CommonValues.BLUE_GOAL_CENTER

        for other in players:
            if other.car_id == player.car_id:
                continue

            if other.team_num == CommonValues.BLUE_TEAM and player.team_num == other.team_num:
                car_data = other.car_data
            else:
                car_data = other.inverted_car_data

            # TODO: COMMENT THIS OUT
            #car_data = ObsBuilder.get_random_physics_state()

            ob += car_data.serialize()

        return ob