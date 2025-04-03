from manim import *
import numpy as np

COLOR_FG = BLACK

class QuadraticPlot(ThreeDScene):
    def construct(self):
        self.camera.background_color = WHITE

        axes = self.create_axes()
        grid = self.create_grid(axes)

        # Ensure axes are in front of the grid
        axes.set_z_index(2)
        grid.set_z_index(1)

        border = self.create_border(axes)
        title, equation, xlabel, ylabel = self.create_labels(axes)
        curve, dots = self.create_plot(axes)
        author_text = self.create_credit()

        self.apply_shift(
            axes, grid, border, curve, dots, xlabel, ylabel, author_text
        )

        # Group all chart elements
        chart_group = VGroup(axes, grid, border, curve, dots, xlabel, ylabel)

        self.play(Create(axes), Create(border))
        self.wait(1)

        self.play(Write(title), Write(equation))
        self.wait(1)

        self.play(Create(grid), Write(xlabel), Write(ylabel))
        self.wait(1)

        self.play(Create(curve))
        self.wait(1)

        self.play(FadeIn(dots))
        self.wait(2)

        # Call the separate camera animation
        self.animate_camera(chart_group)

        # Call the separate author credit animation
        self.animate_credit(author_text)

    def apply_shift(self, *mobjects):
        # Adjust this value as needed
        SHIFT_RIGHT = RIGHT * 0.5
        for mobject in mobjects:
            mobject.shift(SHIFT_RIGHT)

    def create_axes(self):
        # Define axes with strict range
        axes = Axes(
            x_range=[-10, 20, 2],    # X axis range
            y_range=[-120, 60, 20],  # Y axis range
            axis_config={
                "color": COLOR_FG,
                "include_numbers": True
            },
            tips=True  # Ensure tips are enabled
        )

        # Manually resize the arrow tips
        axes.x_axis.tip.set(width=0.2, height=0.2)
        axes.y_axis.tip.set(width=0.2, height=0.2)

        LABEL_CONFIG = {
            "font": "Source Sans Pro",
            "font_size": 20,
            "color": COLOR_FG
        }

        # Retrieve and resize the labels for both axes
        for label in axes.get_x_axis().numbers:
            label.set(**LABEL_CONFIG)

        for label in axes.get_y_axis().numbers:
            label.set(**LABEL_CONFIG)

        return axes

    def create_grid(self, axes):
        return NumberPlane(
            x_range=[-10, 20, 2],
            y_range=[-120, 60, 20],
            faded_line_ratio=2,
            x_length=axes.x_length,
            y_length=axes.y_length,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        )

    def create_border(self, axes):
        return SurroundingRectangle(
            axes,
            color=COLOR_FG,
            stroke_color=GRAY_E,
            stroke_width=2
        )

    def create_labels(self, axes):
        FONT_CONFIG = {
            "font": "Source Sans Pro",
            "color": TEAL_E
        }

        title = Text(
            "Easy Quadratic Chart",
            **FONT_CONFIG,
            font_size=28,
        ).to_edge(UP * 0.5)

        equation = MathTex(
            "y = x^2 - 12x - 64",
            color=BLUE_E,
            font_size=26
        ).next_to(title, DOWN, buff=0.5)

        xlabel = Text(
            "Just  X",
            **FONT_CONFIG,
            font_size=24
        ).next_to(axes, DOWN, buff=0.5)

        ylabel = Text(
            "Just  Y",
            **FONT_CONFIG,
            font_size=24
        ).rotate(90 * DEGREES).next_to(axes, LEFT, buff=0.3)

        return title, equation, xlabel, ylabel

    def create_plot(self, axes):
        def f(x):
            return x**2 - 12*x - 64

        x_vals = np.linspace(-10, 20, 100)
        y_vals = [f(x) for x in x_vals]

        trimmed_x = []
        trimmed_y = []
        for x, y in zip(x_vals, y_vals):
            if -120 <= y <= 60:
                trimmed_x.append(x)
                trimmed_y.append(y)

        curve = ParametricFunction(
            lambda t: axes.c2p(t, f(t)),
            t_range=[min(trimmed_x), max(trimmed_x)],
            color=COLOR_FG
        )

        xdot = np.arange(-10, 20, 2)
        dots = VGroup(*[
            Dot(axes.c2p(x, f(x)), color=RED_E)
            for x in xdot if -120 <= f(x) <= 60
        ])

        return curve, dots

    def create_credit(self):
        # Author Credit
        return Text(
            "Made by Epsi using Manim",
            font="Source Sans Pro",
            font_size=22,
            color=BLUE_E
        ).move_to(ORIGIN)  # Center the text


    def animate_credit(self, author_text):
        # Flash effect at the end
        self.play(Flash(
            author_text, color=TEAL_E, flash_radius=0.5))
        self.wait(1)

        # 2 seconds fade-in
        self.play(FadeIn(
            author_text, scale=1.2, run_time=2))
        # Keep the text visible for 2 seconds
        self.wait(2)

        # 2 seconds fade-out
        self.play(FadeOut(
            author_text, run_time=2))
        self.wait(1)

    def animate_camera(self, chart_group):
        # Zoom out
        self.play(
            chart_group.animate.scale(0.5),
            run_time=2
        )
        self.wait(2)

        # Rotate Camera for a 3D Effect
        self.move_camera(
            phi=75 * DEGREES, theta=45 * DEGREES,
            run_time=3)
        self.wait(2)

        # Zoom back in
        self.play(
            chart_group.animate.scale(2),
            run_time=2
        )
        self.wait(2)

        # Return to 2D View
        self.move_camera(
            phi=0 * DEGREES, theta=-90 * DEGREES,
            run_time=3)
        self.wait(2)
