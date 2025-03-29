from manim import *
import numpy as np

COLOR_FG = BLACK

class QuadraticSurface(ThreeDScene):
    def construct(self):
        self.camera.background_color = WHITE
        self.set_camera_orientation(
            phi=75 * DEGREES, theta=45 * DEGREES)

        axes = self.create_axes()
        surface = self.create_surface(axes)
        xlabel, ylabel, zlabel = self.create_labels(axes)
        plane_vectors = self.create_plane_vectors(axes)
        axis_vectors = self.create_axis_vectors(axes)

        # Group all chart elements
        chart_group = VGroup(
            axes, surface, xlabel, ylabel, zlabel,
            plane_vectors, axis_vectors)

        title, equation = self.create_titles()
        author_text = self.create_credit()

        # Fix in 2D frame
        self.add_fixed_in_frame_mobjects(title, equation, author_text)

        self.play(Create(axes))
        self.wait(1)

        self.play(Write(equation),
            Write(xlabel), Write(ylabel), Write(zlabel))
        self.wait(1)

        self.play(Create(plane_vectors), Create(axis_vectors))
        self.wait(2)

        self.play(Create(surface))
        self.wait(2)

        # Call the separate camera animation
        self.animate_camera(chart_group)

        # Call the separate author credit animation
        self.animate_credit(author_text)

    def create_axes(self):
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-150, 75, 25],
            axis_config={
                "color": COLOR_FG,
                "include_numbers": True
            },
            # Ensure tips are enabled
            tips=True
        )

        # Manually resize the arrow tips
        axes.x_axis.tip.set(width=0.2, height=0.2)
        axes.y_axis.tip.set(width=0.2, height=0.2)
        # axes.z_axis.tip.set(width=0.2, height=0.2)

        FONT_CONFIG = {
            "font": "Source Sans Pro",
            "font_size": 20,
            "color": COLOR_FG
        }

        # Retrieve and resize the labels for both axes
        for label in axes.get_x_axis().numbers:
            label.set(**FONT_CONFIG)
            label.rotate(180 * DEGREES, axis=IN)

        for label in axes.get_y_axis().numbers:
            label.set(**FONT_CONFIG)
            label.rotate(180 * DEGREES, axis=IN)

        for label in axes.get_z_axis().numbers:
            label.set(**FONT_CONFIG)
            label.rotate(90 * DEGREES, axis=RIGHT)

        return axes

    def create_surface(self, axes):
        def f(x, y):
            return x**2 + y**2 - 12*x + 12*y + x*y - 64

        surface = Surface(
            lambda u, v: axes.c2p(u, v, f(u, v)),
            u_range=[-5, 5],
            v_range=[-5, 5],
            resolution=(20, 20),
            fill_opacity=0.8,
            checkerboard_colors=[BLUE_E, BLUE_B]
        )
        return surface

    def create_titles(self):
        # Title
        title = Text(
            "Easy Quadratic Surface",
            font="Source Sans Pro",
            font_size=28,
            color=TEAL_E
        ).to_edge(UP * 0.5)

        equation = MathTex(
            "z = x^2 + y^2 - 12x + 12y + xy - 64",
            color=BLUE_E, font_size=26
        ).next_to(title, DOWN, buff=0.5)

        return title, equation

    def create_labels(self, axes):
        FONT_CONFIG = {
            "font": "Source Sans Pro",
            "font_size": 24,
            "color": TEAL_E
        }

        xlabel = Text("Just  X", **FONT_CONFIG)
        ylabel = Text("Just  Y", **FONT_CONFIG)
        zlabel = Text("Just  Z", **FONT_CONFIG)

        xlabel.\
            rotate(180 * DEGREES, axis=IN).\
            next_to(axes.get_x_axis(), DOWN, buff=2.2)
        ylabel.\
            rotate(90 * DEGREES).\
            next_to(axes.get_y_axis(), LEFT, buff=1.5)

        zlabel.\
            rotate(90 * DEGREES, axis=RIGHT).\
            rotate(180 * DEGREES, axis=IN).\
            next_to(axes.get_z_axis(), UP, buff=0.3)

        return xlabel, ylabel, zlabel

    def create_plane_vectors(self, axes):
        vectors = VGroup(
            # Vector along the XY plane
            Arrow3D(
                start=axes.c2p(0, 0, 0),
                end=axes.c2p(1, 1, 0),
                color=RED_E),
            # Vector moving along XZ plane
            Arrow3D(
                start=axes.c2p(0, 0, 0),
                end=axes.c2p(1, 0, 1),
                color=RED_E),
            # Vector moving along YZ plane
            Arrow3D(
                start=axes.c2p(0, 0, 0),
                end=axes.c2p(0, 1, 1),
                color=RED_E)
        )
        return vectors

    def create_axis_vectors(self, axes):
        vectors = VGroup(
            # Vector along the X axis
            Arrow3D(
                start=axes.c2p(0, 0, 0),
                end=axes.c2p(2, 0, 0),
                color=BLUE_E),
            # Vector moving along Y axis
            Arrow3D(
                start=axes.c2p(0, 0, 0),
                end=axes.c2p(0, 2, 0),
                color=BLUE_E),
            # Vector moving along Z axis
            Arrow3D(
                start=axes.c2p(0, 0, 0),
                end=axes.c2p(0, 0, 2),
                color=BLUE_E)
        )
        return vectors


    def create_credit(self):
        credit = Text(
            "Made by Epsi using Manim",
            font="Source Sans Pro",
            font_size=22,
            color=BLUE_E
        ).to_corner(UL)  # UL = Upper Left

        # Initially invisible
        credit.set_opacity(0)
        return credit

    def animate_credit(self, author_text):
        # Handles the flashing and
        # fade-in/out animation of the credit text.

        author_text.set_opacity(1)

        self.play(FadeIn(
            author_text, scale=1.2, run_time=2))
        self.wait(2)

        # Fades out again
        self.play(
            FadeOut(author_text, run_time=2))
        self.wait(1)

    def animate_camera(self, chart_group):
        # Zoom out
        self.play(
            chart_group.animate.scale(0.5),
            run_time=2
        )
        self.wait(2)

        # Return to 2D View
        self.move_camera(
            phi=0 * DEGREES, theta=-90 * DEGREES,
            run_time=3)
        self.wait(2)

        # Zoom back in
        self.play(
            chart_group.animate.scale(2),
            run_time=2
        )
        self.wait(2)

        # Rotate Camera for a 3D Effect
        self.move_camera(
            phi=75 * DEGREES, theta=45 * DEGREES,
            run_time=3)
        self.wait(2)

