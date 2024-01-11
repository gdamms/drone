import math


def rotate_vector(x: float, y: float, angle: float) -> tuple:
    """Rotate vector (x, y) by angle.

    Args:
        x (float): Vector x.
        y (float): Vector y.
        angle (float): Angle in radians.
    return:
        tuple: Rotated vector (x, y).
    """
    return (x * math.cos(angle) - y * math.sin(angle),
            x * math.sin(angle) + y * math.cos(angle))


def split_force(fx: float, fy: float, x: float, y: float) -> tuple:
    """Split force (fx, fy) into force and torque.

    Args:
        fx (float): Force x.
        fy (float): Force y.
        x (float): Position x.
        y (float): Position y.
    return:
        tuple: Force and torque (fx, fy, torque).
    """
    # d = math.sqrt(x**2 + y**2)
    # f = math.sqrt(fx**2 + fy**2)
    # if d == 0 or f == 0:
    #     return (fx, fy, 0)

    # dot = fx * x + fy * y
    cross = fx * y - fy * x
    # cos = dot / (d * f)

    return fx, fy, cross


def sign(x):
    return math.copysign(1, x)


def clip(x, a, b):
    return min(max(x, a), b)
