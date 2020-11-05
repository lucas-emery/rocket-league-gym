import numpy as np

def get_dist(x,y):
    return np.subtract(x,y)

def vector_projection(vec, dest_vec, mag_squared=None):
    """Compute the vector projection of vec on to dest_vec."""
    if mag_squared is None:
        norm = vecmag(dest_vec)
        if norm == 0:
            return dest_vec
        mag_squared = norm * norm

    if mag_squared == 0:
        return dest_vec

    dot = np.dot(vec, dest_vec)
    projection = np.multiply(np.divide(dot, mag_squared), dest_vec)
    return projection

def scalar_projection(vec, dest_vec):
    """Compute the scalar projection of vec on to dest_vec."""
    norm = vecmag(dest_vec)

    if norm == 0:
        return 0

    dot = np.dot(vec, dest_vec) / norm
    return dot

def squared_vecmag(vec):
    x = np.linalg.norm(vec)
    return x*x

def vecmag(vec):
    norm = np.linalg.norm(vec)
    return norm

def unitvec(vec):
    return np.divide(vec, vecmag(vec))
