from rlgym.utils.obs_builders import ObsBuilder
from rlgym.utils import CommonValues, Math
import numpy as np

class RhobotObs(ObsBuilder):
    def __init__(self):
        super().__init__()
        self.obs_size = 66

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
        ob.append(int(player.has_flip))
        ob.append(int(player.boost_amount))
        ob.append(int(player.on_ground))


        ob += player_car.position
        ob += player_car.orientation
        ob += [np.sin(arg) for arg in player_car.orientation]
        ob += [np.cos(arg) for arg in player_car.orientation]
        yaw =  player_car.orientation[2]
        angle_between_bot_and_target = np.arctan2(ball.position[1] - player_car.position[1],
                                                  ball.position[0] - player_car.position[0])
        
        angle_front_to_target = angle_between_bot_and_target - yaw
        ob.append(angle_front_to_target)
        ob += player_car.linear_velocity
        ob += player_car.angular_velocity

        ob += ball.position
        ob += ball.linear_velocity
        ob += ball.angular_velocity

        ob += CommonValues.ORANGE_GOAL_CENTER
        ob += CommonValues.BLUE_GOAL_CENTER

        pb_dist = Math.vecmag(Math.get_dist(player_car.position, ball.position))
        ob.append(pb_dist)

        pg_dist = Math.vecmag(Math.get_dist(player_car.position, CommonValues.ORANGE_GOAL_CENTER))
        ob.append(pg_dist)

        pog_dist = Math.vecmag(Math.get_dist(player_car.position, CommonValues.BLUE_GOAL_CENTER))
        ob.append(pog_dist)

        for other in players:
            if other.car_id == player.car_id:
                continue

            if other.team_num == CommonValues.BLUE_TEAM and player.team_num == other.team_num:
                car_data = other.car_data
            else:
                car_data = other.inverted_car_data

            # TODO: COMMENT THIS OUT
            #car_data = ObsBuilder.get_random_physics_state()

            ob += car_data.position
            ob += car_data.orientation
            ob += [np.sin(arg) for arg in car_data.orientation]
            ob += [np.cos(arg) for arg in car_data.orientation]
            ob += car_data.linear_velocity
            ob += car_data.angular_velocity

            pc_dist = Math.vecmag(Math.get_dist(player_car.position, car_data.position))
            ob.append(pc_dist)
            
            
        return ob