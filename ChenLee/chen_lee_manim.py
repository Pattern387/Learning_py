from manim import *
import numpy as np
from scipy.integrate import odeint


class CustomTracedPath(TracedPath):
    def __init__(
        self,
        traced_point_func,
        stroke_width: float = 2,
        stroke_color=RED,
        dissipating_time=None,
        **kwargs
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


class ChenLeeCurve(ThreeDScene):
    def construct(self):
        # Chen-Lee parameters
        a, b, c = 5.0, 5.0, 28.0

        # Chen-Lee system of equations
        def chen_lee(state, t):
            x, y, z = state
            dx = a * (x - y)
            dy = (c - a) * x - x * z + c * y
            dz = x * y - b * z
            return [dx, dy, dz]

        # Time vector and integration
        t_vals = np.linspace(0, 50, 2000)
        initial_state = [1.0, 1.0, 1.0]
        trajectory = odeint(chen_lee, initial_state, t_vals)

        scale = 0.05  # Scale down to fit in Manim's coordinate space

        # Create a movable dot at the start of the trajectory (scaled)
        dot = Dot3D(point=trajectory[0] * scale, color=YELLOW, radius=0.07)
        trace = CustomTracedPath(dot.get_center, stroke_color=YELLOW, stroke_width=2)

        axes = ThreeDAxes()
        self.add(axes, dot, trace)

        index_tracker = ValueTracker(0)

        def update_dot(mob):
            index = int(index_tracker.get_value())
            if index < len(trajectory):
                pos = trajectory[index] * scale
                mob.move_to(pos)

        dot.add_updater(update_dot)

        # Set initial camera angle and rotate slowly
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        # Animate the dot moving along the trajectory
        self.play(
            index_tracker.animate.set_value(len(trajectory) - 1),
            run_time=30,
            rate_func=linear,
        )

        self.wait(1)
