from manim import *
import random


class CustomTracedPath(TracedPath):  # 跟踪啥
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
        )  # dissipating_time 是消失的时间
        self.trace_enable = True

    def update_path(self, mob, dt):  # 画线
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

    def stop_trace(self):  # 停止跟踪
        self.trace_enable = False

    def start_trace(self):  # 开始跟踪
        self.trace_enable = True
        self.time = 1


class GewellterTorusIntroduce(Scene):  # 介绍
    def construct(self):
        title = Text("Corrugated Torus (波纹曲面)", font_size=45)
        title.move_to(UP * 3)
        self.play(FadeIn(title), run_time=2)  # fadein
        surface_equation1 = MathTex(
            r"\text{Corrugated Torus=}\begin{cases} x=(R1+R2\cos(nu)+r\cos(v))\cos(u) \\ y = 2r\sin(v) \\ z = (R1+R2\cos(nu)+r\cos(v))\sin(u) \end{cases} "
        ).scale(0.6)
        surface_equation2 = MathTex(
            r"0 \leq u,v \leq 2\pi, R1=3,R2=0.5,r=3,n=[4,6,8,10]"
        ).scale(
            0.6
        )  # 公式
        surface_equation1.next_to(title, DOWN * 2)
        surface_equation2.next_to(surface_equation1, DOWN)
        introduce1 = Text(
            "Wave Torus是一种结合了传统环面结构与周期性波动调制的复杂数学曲面",
            font_size=24,
        )
        introduce2 = Text(
            "其参数化的灵活性使其成为研究复杂曲面几何、计算机图形渲染及艺术创作的理想模型",
            font_size=24,
        )
        introduce1.next_to(surface_equation2, DOWN * 2)
        introduce2.next_to(introduce1, DOWN)
        self.play(FadeIn(surface_equation1), FadeIn(surface_equation2), run_time=2)
        self.play(FadeIn(introduce1), FadeIn(introduce2), run_time=2)
        self.wait(2)
        self.play(
            FadeOut(
                title, surface_equation1, surface_equation2, introduce1, introduce2
            ),
            run_time=2,
        )


class GewellterTorus(ThreeDScene):
    def construct(self):
        def param_gauss(u, v, R1, R2, r, n):
            x = (R1 + R2 * np.cos(n * u) + r * np.cos(v)) * np.cos(u)
            y = 1.5 * r * np.sin(v)
            z = (R1 + R2 * np.cos(n * u) + r * np.cos(v)) * np.sin(u)

            return np.array([x, y, z])

        # dot_num = 280
        dot_num1 = 30  # 30
        dot_num2 = 25  # 40
        dots = VGroup()
        # 定义x,y,z坐标的缩放倍数
        scale_x = 1
        scale_y = 1
        scale_z = 1
        # 定义渐变颜色
        colors = color_gradient(
            (RED, ORANGE, YELLOW, GREEN, ManimColor("#008080"), BLUE, PURPLE),
            dot_num1 * dot_num2,
        )
        line_colors = color_gradient(
            (RED, ORANGE, YELLOW, GREEN, ManimColor("#008080"), BLUE, PURPLE), dot_num2
        )
        step1 = TAU / dot_num1  # TAU = 2pi
        step2 = TAU / dot_num2
        """
        R1 = 3.5
        R2 = 0.5
        r = 2
        n = 4
        """
        R1 = 3
        R2 = 0.5
        r = 2.6
        n = 6

        # 所有的点都生成
        for i in range(0, dot_num1):  # 经度
            u = i * step1
            for j in range(0, dot_num2):  # 纬度
                v = j * step2
                # v = 0
                # v = random.uniform(0, TAU)
                point = param_gauss(u, v, R1, R2, r, n)
                # print(u, v, point)
                point[0] /= scale_x
                point[1] /= scale_y
                point[2] /= scale_z
                # dot开始画点
                dot = Dot(point, 0.028, color=colors[i * dot_num2 + j])
                # 位置   半径   颜色
                dot.ori_u = u
                dot.ori_v = v
                dot.u = u
                dot.v = v
                dot.R1 = R1
                dot.R2 = R2
                dot.r = r
                dot.n = n
                dot.speed = 0.28
                # random.shuffle(line_colors)
                path = CustomTracedPath(
                    dot.get_center,
                    stroke_color=line_colors[j],
                    stroke_width=0.93,
                    dissipating_time=5.5,
                )
                dot.path = path
                dot.trace_enable = True
                self.add_fixed_orientation_mobjects(dot)  # 加入点
                dots.add(dot)
                # path需要add在dot之后，这样刷新的顺序是path在前，dot在后；如果顺序掉反了，会出现path有小部分连不上dot的情况
                # self.add(path)

        # self.add_fixed_orientation_mobjects(dots)

        # 更新dot运动位置
        start = False
        change_n = 0

        def update_dot(mob, dt):  # update——dot
            nonlocal start
            if start:
                # if mob.u - mob.ori_u < 0.3:
                #    mob.u += dt*mob.speed/10
                mob.u += dt * mob.speed
                mob.v += dt * mob.speed

                if change_n == 1:
                    if mob.n >= 8:
                        mob.n = 8
                    else:
                        mob.n += dt * mob.speed
                elif change_n == 2:
                    if mob.n >= 10:
                        mob.n = 10
                    else:
                        mob.n += dt * mob.speed
                elif change_n == 3:
                    if mob.n >= 12:
                        mob.n = 12
                    else:
                        mob.n += dt * mob.speed

                new_point = param_gauss(mob.u, mob.v, mob.R1, mob.R2, mob.r, mob.n)
                new_point[0] /= scale_x
                new_point[1] /= scale_y
                new_point[2] /= scale_z
                # 路径跑完了，停止路径跟踪
                """
                if mob.v - mob.ori_v > 2*PI+0.01 and mob.trace_enable:
                    mob.trace_enable = False
                    #print("Go to next path")
                    mob.path.clear_updaters()
                """

                # print(new_point)
                mob.move_to(new_point)

        # 是否实时跟踪angle值
        observe_angle = False
        # 是否跟踪dot
        track_new_point = False
        # 定义角度跟踪值 如果跟踪
        phi_value = ValueTracker(PI / 2)
        theta_value = ValueTracker(PI / 2)
        gamma_value = ValueTracker(0)

        def update_dot_position(mob, dt):
            if observe_angle:
                phi_value.set_value(self.camera.get_phi())
                theta_value.set_value(self.camera.get_theta())
            if track_new_point:
                position = mob.get_center()
                self.set_camera_orientation(frame_center=position)

        # 显示角度值
        # phi_text = always_redraw(lambda: Text(f"φ={phi_value.get_value():.2f}", font_size=18).move_to(DOWN*6))
        # theta_text = always_redraw(lambda: Text(f"θ={theta_value.get_value():.2f}", font_size=18).next_to(phi_text, RIGHT, buff=0.3))
        # gamma_text = always_redraw(lambda: Text(f"g={gamma_value.get_value():.2f}", font_size=18).next_to(theta_text, RIGHT, buff=0.3))
        # self.add_fixed_in_frame_mobjects(phi_text, theta_text, gamma_text)
        surface_equation = (
            MathTex(
                r"\text{Gewellter Torus=}\begin{cases} x=(R1+R2\cos(nu)+r\cos(v))\cos(u) \\ y = 2r\sin(v) \\ z = (R1+R2\cos(nu)+r\cos(v))\sin(u) \end{cases}  (0 \leq u,v \leq 2\pi R1=3,R2=0.5,r=3,n=[4,6,8,10])"
            )
            .scale(0.53)
            .move_to(DOWN * 6.6)
        )
        self.add_fixed_in_frame_mobjects(surface_equation)
        self.set_camera_orientation(
            phi=phi_value.get_value(),
            theta=theta_value.get_value(),
            gamma=gamma_value.get_value(),
        )

        for dot in dots:
            dot.add_updater(update_dot)

        # 定义跟踪dot
        tracked_dot_index = dot_num1 * dot_num2 // 3
        dots[tracked_dot_index].add_updater(update_dot_position)

        # self.add(dots)
        start = True
        for dot in dots:
            self.add(dot.path)
        self.wait(3)

        self.move_camera(
            phi=self.camera.get_phi() - PI / 2,
            theta=self.camera.get_theta() - PI / 2,
            gamma=self.camera.get_gamma() + PI / 2,
            run_time=15,
        )

        # 设置镜头焦距
        print(self.camera.focal_distance)
        original_focal_distance = self.camera.focal_distance
        # 镜头开始围绕某个角度旋转
        self.begin_ambient_camera_rotation(rate=0.3, about="phi")
        self.begin_ambient_camera_rotation(rate=0.3, about="theta")
        # 画面压缩的效果
        self.move_camera(focal_distance=4, run_time=3)
        self.wait(TAU / 0.3 - 6)
        self.move_camera(focal_distance=original_focal_distance, run_time=3)
        self.stop_ambient_camera_rotation(about="phi")
        self.stop_ambient_camera_rotation(about="theta")

        self.wait(1)
        self.move_camera(
            phi=self.camera.get_phi() + PI / 2,
            theta=self.camera.get_theta() + PI / 2,
            gamma=self.camera.get_gamma() - PI / 2,
            run_time=10,
        )

        # 变化n的值，并且在曲面一直旋转
        print(self.camera.get_phi(), self.camera.get_theta(), self.camera.get_gamma())
        self.wait(1)
        change_n = 1
        # n_latex = MathTex(r'n=8')
        # n_latex.moveto
        # animations = [Write]
        print(self.camera.get_phi(), self.camera.get_theta(), self.camera.get_gamma())
        self.move_camera(
            phi=self.camera.get_phi() + TAU,
            theta=self.camera.get_theta() + TAU,
            gamma=self.camera.get_gamma() + PI,
            run_time=25,
        )
        self.move_camera(gamma=self.camera.get_gamma() + PI, run_time=15)

        change_n = 2
        n_latex = MathTex(r"n=10")
        self.move_camera(
            phi=self.camera.get_phi() + TAU,
            theta=self.camera.get_theta() + TAU,
            gamma=self.camera.get_gamma() + PI / 2,
            run_time=25,
        )
        self.move_camera(gamma=self.camera.get_gamma() + PI * 3 / 2, run_time=15)

        change_n = 3
        n_latex = MathTex(r"n=12")
        self.move_camera(
            phi=self.camera.get_phi() + TAU,
            theta=self.camera.get_theta() + TAU,
            gamma=self.camera.get_gamma() + PI,
            run_time=25,
        )
        self.move_camera(gamma=self.camera.get_gamma() + PI, run_time=15)

        print(self.camera.get_phi(), self.camera.get_theta(), self.camera.get_gamma())
        print(dots[0].n)
