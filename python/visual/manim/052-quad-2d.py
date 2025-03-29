from manim import *
import numpy as np

COLOR_FG = BLACK

class QuadraticPlot(Scene):
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
