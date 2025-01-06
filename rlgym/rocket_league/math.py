"""
A set of useful mathematical operations.
"""

import numpy as np


def euclidean_distance(x: np.ndarray, y: np.ndarray) -> float:
    """
    Returns the Euclidean distance between two vectors.

    :param x: A numpy array of size n.
    :param y: A numpy array of size n.

    :return: A float representing the distance between the two vectors.
    """
    return np.linalg.norm(x - y)


def vector_projection(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Returns the vector projection of a vector `a` onto another vector `b`.

    :param a: A numpy array of size n.
    :param b: A numpy array of size n.

    :return: A numpy array of size n representing the vector projection.
    """
    norm = magnitude(b)

    if norm == 0:
        return np.zeros_like(b)

    sp = np.dot(a, b) / norm  # scalar projection
    return np.multiply(sp, b / norm)


def scalar_projection(a: np.ndarray, b: np.ndarray) -> float:
    """
    Returns the scalar projection of a vector `a` onto another vector `b`.

    :param a: A numpy array of size n.
    :param b: A numpy array of size n.

    :return: A float representing the scalar projection.
    """
    norm = magnitude(b)

    if norm == 0:
        return 0

    dot = np.dot(a, b) / norm
    return dot


def magnitude(vec: np.ndarray) -> float:
    """
    Returns the magnitude of a vector.

    :param vec: A numpy array of size n.

    :return: A float representing the magnitude of the vector.
    """
    norm = np.linalg.norm(vec)
    return norm


def normalize(vec: np.ndarray):
    """
    Returns a unit vector with the same direction as the input vector.

    :param vec: A numpy array of size n.

    :return: A numpy array of size n.
    """
    return np.divide(vec, magnitude(vec))


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Computes the cosine similarity between two vectors.

    :param a: A numpy array of size n.
    :param b: A numpy array of size n.

    :return: A float representing the cosine similarity.
    """
    return np.dot(a / np.linalg.norm(a), b / np.linalg.norm(b))


def quat_to_euler(quat: np.ndarray) -> np.ndarray:
    """
    Converts a quaternion to Euler angles.

    :param quat: A numpy array of size 4 representing the quaternion.

    :return: A numpy array of size 3 representing the pitch, yaw, and roll angles.
    """
    w, x, y, z = quat
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    sinp = 2 * (w * y - z * x)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)

    roll = np.arctan2(sinr_cosp, cosr_cosp)
    if abs(sinp) > 1:
        pitch = np.pi / 2
    else:
        pitch = np.arcsin(sinp)
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return np.array([-pitch, yaw, -roll])


# From RLUtilities
def quat_to_rot_mtx(quat: np.ndarray) -> np.ndarray:
    """
    Converts a quaternion to a rotation matrix.

    :param quat: A numpy array of size 4 representing the quaternion.

    :return: A numpy array of size 3x3 representing the rotation matrix.
    """
    w = -quat[0]
    x = -quat[1]
    y = -quat[2]
    z = -quat[3]

    theta = np.zeros((3, 3))

    norm = np.dot(quat, quat)
    if norm != 0:
        s = 1.0 / norm

        # front direction
        theta[0, 0] = 1.0 - 2.0 * s * (y * y + z * z)
        theta[1, 0] = 2.0 * s * (x * y + z * w)
        theta[2, 0] = 2.0 * s * (x * z - y * w)

        # left direction
        theta[0, 1] = 2.0 * s * (x * y - z * w)
        theta[1, 1] = 1.0 - 2.0 * s * (x * x + z * z)
        theta[2, 1] = 2.0 * s * (y * z + x * w)

        # up direction
        theta[0, 2] = 2.0 * s * (x * z + y * w)
        theta[1, 2] = 2.0 * s * (y * z - x * w)
        theta[2, 2] = 1.0 - 2.0 * s * (x * x + y * y)

    return theta


def rotation_to_quaternion(m: np.ndarray) -> np.ndarray:
    """
    Converts a rotation matrix to a quaternion.

    :param m: A numpy array of size 3x3 representing the rotation matrix.

    :return: A numpy array of size 4 representing the quaternion.
    """
    trace = np.trace(m)
    q = np.zeros(4)

    if trace > 0:
        s = (trace + 1) ** 0.5
        q[0] = s * 0.5
        s = 0.5 / s
        q[1] = (m[2, 1] - m[1, 2]) * s
        q[2] = (m[0, 2] - m[2, 0]) * s
        q[3] = (m[1, 0] - m[0, 1]) * s
    else:
        if m[0, 0] >= m[1, 1] and m[0, 0] >= m[2, 2]:
            s = (1 + m[0, 0] - m[1, 1] - m[2, 2]) ** 0.5
            inv_s = 0.5 / s
            q[1] = 0.5 * s
            q[2] = (m[1, 0] + m[0, 1]) * inv_s
            q[3] = (m[2, 0] + m[0, 2]) * inv_s
            q[0] = (m[2, 1] - m[1, 2]) * inv_s
        elif m[1, 1] > m[2, 2]:
            s = (1 + m[1, 1] - m[0, 0] - m[2, 2]) ** 0.5
            inv_s = 0.5 / s
            q[1] = (m[0, 1] + m[1, 0]) * inv_s
            q[2] = 0.5 * s
            q[3] = (m[1, 2] + m[2, 1]) * inv_s
            q[0] = (m[0, 2] - m[2, 0]) * inv_s
        else:
            s = (1 + m[2, 2] - m[0, 0] - m[1, 1]) ** 0.5
            inv_s = 0.5 / s
            q[1] = (m[0, 2] + m[2, 0]) * inv_s
            q[2] = (m[1, 2] + m[2, 1]) * inv_s
            q[3] = 0.5 * s
            q[0] = (m[1, 0] - m[0, 1]) * inv_s

    # q[[0, 1, 2, 3]] = q[[3, 0, 1, 2]]

    return -q


def euler_to_rotation(pyr: np.ndarray) -> np.ndarray:
    """
    Converts Euler angles to a rotation.

    :param pyr: A numpy array of size 3 representing the pitch, yaw, and roll angles.

    :return: A numpy array of size 3x3 representing the rotation matrix.
    """
    cp, cy, cr = np.cos(pyr)
    sp, sy, sr = np.sin(pyr)

    theta = np.zeros((3, 3))

    # front
    theta[0, 0] = cp * cy
    theta[1, 0] = cp * sy
    theta[2, 0] = sp

    # left
    theta[0, 1] = cy * sp * sr - cr * sy
    theta[1, 1] = sy * sp * sr + cr * cy
    theta[2, 1] = -cp * sr

    # up
    theta[0, 2] = -cr * cy * sp - sr * sy
    theta[1, 2] = -cr * sy * sp + sr * cy
    theta[2, 2] = cp * cr

    return theta


def rand_uvec3(rng: np.random.Generator = np.random) -> np.ndarray:
    """
    Generates a random 3-dimensional unit vector.

    :param rng: The random number generator to use.

    :return: A numpy array of size 3.
    """
    vec = rng.random(3) - 0.5
    return vec / np.linalg.norm(vec)


def rand_vec3(max_norm: float, rng: np.random.Generator = np.random) -> np.ndarray:
    """
    Generates a random 3-dimensional vector with a size between 0 and max_norm.

    :param max_norm: The maximum norm of the vector.
    :param rng: The random number generator to use.

    :return: A numpy array of size 3.
    """
    return rand_uvec3(rng) * (rng.random() * max_norm)
