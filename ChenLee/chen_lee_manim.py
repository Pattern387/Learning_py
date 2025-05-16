from manim import *

"""
定义Chen-Lee吸引子曲线类
"""


class ChenLeeAttractorCurve(VMobject):
    """
    a,b,c为吸引子参数
    delta: dt
    idle_time: 迭代空跑步数，用于初始化不同时间点
    dissipating_time: 路径保持时间
    """

    def __init__(
        self, position, color, scale, a, b, c, delta, idle_time, dissipating_time
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
        self.dot = Dot(point=position, radius=0.035, color=color)
        self.path = TracedPath(
            self.dot.get_center,
            dissipating_time=dissipating_time,
            stroke_width=0.5,
            stroke_color=color,
        )

    def chen_lee_attractor(self):
        x, y, z = self.position

        # Chen-Lee系统方程
        dx = (self.a * (y - x)) * self.delta
        dy = ((self.c - self.a) * x - x * z + self.c * y) * self.delta
        dz = (x * y - self.b * z) * self.delta

        x += dx
        y += dy
        z += dz

        return [x, y, z]

    def init(self):
        # 空跑迭代，跳过初始瞬态
        for _ in range(self.idle_time):
            self.position = self.chen_lee_attractor()

    def get_scale_point(self, x, y, z):
        # 适当缩放和平移，方便显示
        return np.array([x / self.scale, y / self.scale, z / self.scale - 3])

    def add_point(self):
        self.position = self.chen_lee_attractor()
        scaled_point = self.get_scale_point(*self.position)
        self.dot.move_to(scaled_point)


"""
Chen-Lee吸引子场景示例，单个粒子
"""


class ChenLeeAttractorScene(ThreeDScene):
    def construct(self):
        attractor_eq = (
            MathTex(
                r"\text{Chen-Lee Attractor} = \begin{cases}"
                r"\frac{dx}{dt} = a(y-x) \\"
                r"\frac{dy}{dt} = (c-a)x - xz + cy \\"
                r"\frac{dz}{dt} = xy - bz"
                r"\end{cases} (a=5, b=3, c=28)"
            )
            .scale(0.6)
            .to_edge(DOWN)
        )

        self.play(Create(attractor_eq), run_time=4)
        self.add_fixed_in_frame_mobjects(attractor_eq)

        # 初始化单个Chen-Lee吸引子粒子
        curve = ChenLeeAttractorCurve(
            position=[1, 1, 1],
            color=BLUE,
            scale=10,
            a=5,
            b=3,
            c=28,
            delta=0.01,
            idle_time=100,
            dissipating_time=5,
        )
        self.add(curve, curve.dot, curve.path)

        def update_dot(mob, dt):
            mob.add_point()

        curve.add_updater(update_dot)

        self.set_camera_orientation(phi=75 * DEGREES, theta=120 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2, about="theta")
        self.wait(30)
        self.stop_ambient_camera_rotation()

        curve.clear_updaters()
        self.play(FadeOut(curve.dot), FadeOut(curve.path), run_time=3)
