import numpy as np

def get_dist(x,y):
    return np.subtract(x,y)

def vector_projection(vec, dest_vec):
    """Compute the vector projection of vec on to dest_vec."""
    norm = vecnorm(dest_vec)

    #The only case in which the magnitude of a vector could be 0 is if each component is 0, so the multiplication performed
    #as the final operation in a vector projection would always yield a vector with 0 in each component. Because we know
    #that dest_vec must only contain zeros if its magnitude is zero, we can just skip the computation and immediately return
    #dest_vec.
    if norm == 0:
        return dest_vec

    dot = np.dot(vec, dest_vec)

    projection = np.multiply(np.divide(dot, norm*norm), dest_vec)
    return projection

def scalar_projection(vec, dest_vec):
    """Compute the scalar projection of vec on to dest_vec."""
    norm = vecnorm(dest_vec)

    #Same logic used in vector projection.
    if norm == 0:
        return 0

    dot = np.dot(vec, dest_vec) / norm
    return dot

def vecnorm(vec):
    norm = np.linalg.norm(vec)
    return norm

def unitvec(vec):
    return np.divide(vec, vecnorm(vec))
