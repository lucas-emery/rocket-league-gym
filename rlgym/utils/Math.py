import numpy as np

def get_dist(x,y):
    return np.linalg.norm(np.subtract(x,y))

def get_distance_to_ball_2d(car_data, ball_data):
    return get_dist(car_data[:2], ball_data[:2])

def get_distance_to_ball_3d(car_data, ball_data):
    return get_dist(car_data[:3], ball_data[:3])
