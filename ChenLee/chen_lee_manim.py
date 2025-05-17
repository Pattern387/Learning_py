from manim import *
import numpy as np


class CustomTracedPath(TracedPath):
    def __init__(
        self,
        traced_point_func,
        stroke_width: float = 2,
        stroke_color=YELLOW,
        dissipating_time=None,
        **kwargs,
    ):
        super().__init__(
            traced_point_func, stroke_width, stroke_color, dissipating_time, **kwargs
        )
        self.trace_enable = True
        self.time = 0

    def update_path(self, mob, dt):
        if self.trace_enable:
            new_point = self.traced_point_func()
            if not self.has_points():
                self.start_new_path(new_point)
            self.add_line_to(new_point)
        if self.dissipating_time:
            self.time += dt
            if self.time - 1 > self.dissipating_time:
                nppcc = self.n_points_per_curve
                self.set_points(self.points[nppcc:])

    def stop_trace(self):
        self.trace_enable = False

    def start_trace(self):
        self.trace_enable = True
        self.time = 1


def chen_lee(x, y, z, a=3.0, b=2.7, c=1.7):
    dx = a * (y - x)
    dy = (c - a) * x - x * z + c * y
    dz = x * y - b * z
    return np.array([dx, dy, dz])


class ChenLeeAttractor(ThreeDScene):
    def construct(self):
        dot = Dot3D(point=ORIGIN, radius=0.05, color=YELLOW)

        # Store initial parameters explicitly
        dot.x, dot.y, dot.z = 0.1, 0.2, 0.3
        speed = 2.5
        max_bound = 50
        path = CustomTracedPath(
            dot.get_center,
            stroke_color=YELLOW,
            stroke_width=0.93,
            dissipating_time=5.5,
        )
        self.add(dot, path)

        def update_dot(mob, dt):
            dx, dy, dz = chen_lee(mob.x, mob.y, mob.z)

            # Euler integration
            mob.x += dx * dt * speed
            mob.y += dy * dt * speed
            mob.z += dz * dt * speed

            # Clamp to prevent explosion
            mob.x = np.clip(mob.x, -max_bound, max_bound)
            mob.y = np.clip(mob.y, -max_bound, max_bound)
            mob.z = np.clip(mob.z, -max_bound, max_bound)

            new_pos = np.array([mob.x, mob.y, mob.z])

            # Skip invalid positions
            if np.any(np.isnan(new_pos)) or np.any(np.isinf(new_pos)):
                print(f"Invalid position encountered: {new_pos} — skipping frame")
                return

            scale_factor = 5  # try 5 or 10 for bigger size
            scaled_pos = new_pos * scale_factor
            mob.move_to(scaled_pos)

            # DEBUG: Print position every frame
            print(f"dt={dt:.4f} | Position: {new_pos}")

        dot.add_updater(update_dot)

        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        self.wait(15)
