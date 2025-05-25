from manim import *


class ChenAttractorCurve(VMobject):
    def __init__(
        self, position, colors, scale, a, b, c, delta, idle_time, dissipating_time
    ):
        super().__init__()
        self.position = position
        self.scale = scale
        self.a = a
        self.b = b
        self.c = c
        self.delta = delta
        self.idle_time = idle_time
        self.init()
        self.dot = Dot(point=position, radius=0.03, color=WHITE)
        self.path = TracedPath(
            self.dot.get_center,
            dissipating_time=dissipating_time,
            stroke_width=1,
            stroke_color=colors,
        )

    def chen_attractor(self):
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]

        dx = self.a * (y - x) * self.delta
        dy = ((self.c - self.a) * x - x * z + self.c * y) * self.delta
        dz = (x * y - self.b * z) * self.delta

        x += dx
        y += dy
        z += dz

        return x, y, z

    def init(self):
        for _ in range(self.idle_time):
            x, y, z = self.chen_attractor()
            self.position = [x, y, z]

    def get_scale_point(self, x, y, z):
        return np.array([x / self.scale, y / self.scale, z / self.scale - 3])

    def add_point(self):
        x, y, z = self.chen_attractor()
        self.position = [x, y, z]
        print(f"x: {x:.4f}, y: {y:.4f}, z: {z:.4f}")  # Print coordinates each step
        scaled_x, scaled_y, scaled_z = self.get_scale_point(x, y, z)
        self.dot.move_to(np.array([scaled_x, scaled_y, scaled_z]))


class ChenLeeAttracterScene1(ThreeDScene):
    def construct(self):

        # Create and animate the attractor curve
        curves = VGroup()
        num = 5
        for i in range(num):
            curve = ChenAttractorCurve(
                [1 + 0.2 * i, 1, 0.5], BLUE, 3, 0.2, 0.3, 0.4, 0.02, 300, 1
            )
            curves.add(curve)
            self.add(curve, curve.dot, curve.path)

        def update_dot(mob, dt):
            mob.add_point()

        for i in range(num):
            curves[i].add_updater(update_dot)

        # Set camera view
        self.move_camera(phi=70 * DEGREES, theta=45 * DEGREES, distance=15)
        self.begin_ambient_camera_rotation(rate=0.2, about="theta")
        self.wait(30)
        self.stop_ambient_camera_rotation()

        for curve in curves:
            curve.clear_updaters()
            self.play(FadeOut(curve.dot), FadeOut(curve.path), run_time=6)
