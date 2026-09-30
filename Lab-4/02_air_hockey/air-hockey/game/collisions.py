"""
Reliable puck-vs-paddle collision handling.

Uses swept-circle collision detection so a fast puck cannot tunnel through
a paddle between frames. The puck is also pushed back outside the paddle
after a collision to prevent sticking/vibration.
"""

import math


def handle_paddle_collision(puck, paddle, previous_x=None, previous_y=None):
    """
    Detect a puck/paddle collision using swept-circle collision detection.

    previous_x/previous_y are the puck's position before it moved this frame.
    Returns True if a collision was handled.
    """

    if previous_x is None:
        previous_x = puck.x
    if previous_y is None:
        previous_y = puck.y

    collision_radius = puck.radius + paddle.radius
    radius_sq = collision_radius * collision_radius

    start_x = previous_x - paddle.x
    start_y = previous_y - paddle.y

    end_x = puck.x - paddle.x
    end_y = puck.y - paddle.y

    start_dist_sq = start_x * start_x + start_y * start_y
    end_dist_sq = end_x * end_x + end_y * end_y

    # Already inside the paddle at the beginning of this frame.
    if start_dist_sq < radius_sq:
        distance = math.sqrt(end_dist_sq)

        if distance > 1e-9:
            nx = end_x / distance
            ny = end_y / distance
        else:
            speed = math.hypot(puck.vx, puck.vy)
            if speed > 1e-9:
                nx = -puck.vx / speed
                ny = -puck.vy / speed
            else:
                nx = 1.0
                ny = 0.0

        epsilon = 0.01
        puck.x = paddle.x + nx * (collision_radius + epsilon)
        puck.y = paddle.y + ny * (collision_radius + epsilon)

        velocity_into_surface = puck.vx * nx + puck.vy * ny

        if velocity_into_surface < 0:
            puck.vx -= 2.0 * velocity_into_surface * nx
            puck.vy -= 2.0 * velocity_into_surface * ny

        return True

    # Sweep the complete movement segment from the previous position
    # to the current position.
    dx = end_x - start_x
    dy = end_y - start_y
    movement_sq = dx * dx + dy * dy

    if movement_sq < 1e-12:
        return False

    # Solve:
    # |start + t * movement|^2 = collision_radius^2
    b = 2.0 * (start_x * dx + start_y * dy)
    c = start_x * start_x + start_y * start_y - radius_sq

    discriminant = b * b - 4.0 * movement_sq * c

    if discriminant < 0:
        return False

    sqrt_discriminant = math.sqrt(discriminant)

    t1 = (-b - sqrt_discriminant) / (2.0 * movement_sq)
    t2 = (-b + sqrt_discriminant) / (2.0 * movement_sq)

    hit_t = None

    for t in (t1, t2):
        if 0.0 <= t <= 1.0:
            hit_t = t
            break

    if hit_t is None:
        # Numerical fallback for a final overlapping position.
        if end_dist_sq < radius_sq:
            distance = math.sqrt(end_dist_sq)

            if distance > 1e-9:
                nx = end_x / distance
                ny = end_y / distance
            else:
                nx = 1.0
                ny = 0.0

            epsilon = 0.01
            puck.x = paddle.x + nx * (collision_radius + epsilon)
            puck.y = paddle.y + ny * (collision_radius + epsilon)

            velocity_into_surface = puck.vx * nx + puck.vy * ny

            if velocity_into_surface < 0:
                puck.vx -= 2.0 * velocity_into_surface * nx
                puck.vy -= 2.0 * velocity_into_surface * ny

            return True

        return False

    # Exact collision point.
    hit_x = previous_x + (puck.x - previous_x) * hit_t
    hit_y = previous_y + (puck.y - previous_y) * hit_t

    # Collision normal points from paddle centre toward puck.
    nx = hit_x - paddle.x
    ny = hit_y - paddle.y

    normal_length = math.hypot(nx, ny)

    if normal_length < 1e-9:
        speed = math.hypot(puck.vx, puck.vy)

        if speed > 1e-9:
            nx = -puck.vx / speed
            ny = -puck.vy / speed
        else:
            nx = 1.0
            ny = 0.0
    else:
        nx /= normal_length
        ny /= normal_length

    # Reflect only when travelling into the paddle.
    velocity_into_surface = puck.vx * nx + puck.vy * ny

    if velocity_into_surface >= 0:
        return False

    puck.vx -= 2.0 * velocity_into_surface * nx
    puck.vy -= 2.0 * velocity_into_surface * ny

    # Move outside the paddle so the next frame cannot immediately
    # detect the same collision again.
    epsilon = 0.01
    puck.x = paddle.x + nx * (collision_radius + epsilon)
    puck.y = paddle.y + ny * (collision_radius + epsilon)

    # Continue the puck through the remainder of this frame.
    remaining_time = 1.0 - hit_t
    puck.x += puck.vx * remaining_time
    puck.y += puck.vy * remaining_time

    return True
