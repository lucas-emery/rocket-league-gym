import numpy as np

def get_dist(x,y):
    return np.subtract(x,y)

def get_distance_to_ball_2d(car_data, ball_data):
    return get_dist(car_data[:2], ball_data[:2])

def get_distance_to_ball_3d(car_data, ball_data):
    return get_dist(car_data[:3], ball_data[:3])

def project_vec(vec, destVec):
    projection = np.dot(vecnorm(vec), destVec)
    return projection

def vecnorm(vec):
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return np.divide(vec, norm)
