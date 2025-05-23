from manim import *
import numpy as np


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
        # Parameters for Chen-Lee curve
        a, b, c, d = 2, 3, 4, 5

        # Parametric function for the Chen-Lee inspired curve
        def chen_lee(t):
            x = np.sin(a * t) - np.cos(b * t)
            y = np.sin(c * t) - np.sin(d * t)
            z = np.cos(a * t) + np.cos(d * t)
            return np.array([x, y, z])

        # Create the moving dot initially at t=0
        dot = Dot3D(point=chen_lee(0), color=YELLOW, radius=0.07)

        # Create the trace path attached to the dot
        trace = CustomTracedPath(
            dot.get_center, stroke_color=YELLOW, stroke_width=3, dissipating_time=5
        )

        self.add(dot, trace)

        # t parameter tracker
        t_tracker = ValueTracker(0)

        # Update function to move dot along the Chen-Lee curve
        def update_dot(mob, dt):
            t = t_tracker.get_value()
            t += dt * 0.8  # speed
            if t > 2 * PI:
                t = 0  # loop the animation
            t_tracker.set_value(t)
            new_pos = chen_lee(t)
            mob.move_to(new_pos)

        dot.add_updater(update_dot)

        # Set initial camera angle
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        self.begin_ambient_camera_rotation(rate=0.2, about="phi")

        self.wait(30)
