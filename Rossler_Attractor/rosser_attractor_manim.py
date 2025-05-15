from manim import *

'''
定义粒子对象
'''
class RosslerAttractorCurve(VMobject):
    '''
    a,b,c为吸引子参数
    delta: dt
    idle_time：因为我们要绘制多个粒子，每个粒子不要再相同时间点上(dt相同)，所以设置idle_time，通过init来设置空跑迭代数，让粒子随机分步在不同时间点上
    '''
    def __init__(self, position, colors, scale, a, b, c, delta, idle_time, dissipating_time):
        super().__init__()
        self.position = position
        self.scale = scale
        self.a = a
        self.b = b
        self.c = c
        self.idle_time = idle_time
        print(self.a, self.b, self.c)
        self.delta = delta
        self.init()
        self.dot = Dot(point=position, radius=0.035, color=WHITE)
        self.path = TracedPath(self.dot.get_center, dissipating_time=dissipating_time, stroke_width=0.5, stroke_color=colors)

    def rossler_attractor(self):
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]

        # Rossler公式
        dx = (-y - z) * self.delta
        dy = (self.a*y + x) * self.delta
        dz = (self.b + z*(-self.c+x)) * self.delta

        x += dx
        y += dy
        z += dz
        
        return x, y, z
    
    def init(self):
        # 让粒子空转，图形到达理想的状态
        for _ in range(self.idle_time):
            x, y, z = self.rossler_attractor()
            #print(x, y, z)
            #_, _, _ = self.get_scale_point(x, y, z)
            self.position = [x, y, z]


    def get_scale_point(self, x, y, z):
        return np.array([x/self.scale, y/self.scale, z/self.scale-3])

    def add_point(self):
        x, y, z = self.rossler_attractor()
        self.position = [x, y, z]
        scaled_x, scaled_y, scaled_z = self.get_scale_point(x, y, z)
        self.dot.move_to(np.array([scaled_x, scaled_y, scaled_z]))

'''
场景一，一个场景是1个粒子
'''
class RosserAttractorScene1(ThreeDScene):
    def construct(self):
        enneper_surface_equation = MathTex(r"\text{Rosser Attractor=}\begin{cases} \frac{dx}{dt} = -y-z \\ \frac{dy}{dt} = x+ay \\ \frac{dz}{dt} = b+z*(x-c) \end{cases} (a=0.2,b=0.2,c=5.7)").scale(0.6)
        enneper_surface_equation.move_to(DOWN*5)
        self.play(Create(enneper_surface_equation), run_time=4)
        self.add_fixed_in_frame_mobjects(enneper_surface_equation)

        # 一个粒子的运行情况
        curves = VGroup()
        num = 1
        for i in range(num):
            curve = RosslerAttractorCurve([1+0.2*i, 1, 0.5], BLUE, 3, 0.2, 0.2, 5.7, 0.02, 300, 1)
            curves.add(curve)
            self.add(curve, curve.dot, curve.path)

        def update_dot(mob, dt):
            mob.add_point()


        for i in range(num):
            curves[i].add_updater(update_dot)
        
        self.set_camera_orientation(phi= 88*DEGREES, theta=90 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2, about="theta")
        self.wait(30)
        self.stop_ambient_camera_rotation()
        
        for curve in curves:
            curve.clear_updaters()
            self.play(FadeOut(curve.dot), FadeOut(curve.path), run_time=3)

'''
场景二：50个粒子，形成对比
'''
class RosserAttractorScene2(ThreeDScene):
    def construct(self):
        # 混沌系统公式
        enneper_surface_equation = MathTex(r"\text{Rosser Attractor=}\begin{cases} \frac{dx}{dt} = -y-z \\ \frac{dy}{dt} = x+ay \\ \frac{dz}{dt} = b+z*(x-c) \end{cases} (a=0.2,b=0.2,c=5.7)").scale(0.6)
        enneper_surface_equation.move_to(DOWN*5)
        self.play(Create(enneper_surface_equation), run_time=4)
        self.add_fixed_in_frame_mobjects(enneper_surface_equation)
        
        # 构建50个粒子
        curves = VGroup()
        num = 50
        for i in range(num):
            curve = RosslerAttractorCurve([1+0.2*i, 1, 0.5], BLUE, 3, 0.2, 0.2, 5.7, 0.015, 30*i, 7)
            curves.add(curve)
            self.add(curve, curve.dot, curve.path)

        # 粒子更新函数
        def update_dot(mob, dt):
            mob.add_point()

        # 为每个粒子添加更新函数
        for i in range(num):
            curves[i].add_updater(update_dot)
        
        # 控制相机视角
        self.set_camera_orientation(phi= 88*DEGREES, theta=90 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2, about="theta")
        self.wait(100)
        self.stop_ambient_camera_rotation()
        