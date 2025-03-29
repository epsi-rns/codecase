from manim import *
import numpy as np
from itertools import chain

COLOR_FG = BLACK

class DynamicQuadraticPlot(ThreeDScene):
    def construct(self):
        self.camera.background_color = WHITE

        axes = self.create_axes()
        grid = self.create_grid(axes)

        # Ensure axes are in front of the grid
        axes.set_z_index(2)
        grid.set_z_index(1)

        border = self.create_border(axes)
        self.title, xlabel, ylabel = self.create_labels(axes)
        curve, dots, a_tracker, b_tracker, \
        c_tracker, equation_text = (
            self.create_dynamic_plot(axes)
        )
        author_text = self.create_credit()

        # Group elements for animation
        chart_group = VGroup(
            axes, grid, border, curve, dots, xlabel, ylabel
        )

        self.play(Create(axes), Create(border))
        self.wait(1)

        self.play(Write(self.title))
        self.wait(1)

        self.play(Create(grid), Write(xlabel), Write(ylabel))
        self.wait(1)

        self.play(Create(curve), Write(equation_text))
        self.wait(1)

        self.play(FadeIn(dots))
        self.wait(2)

        # Dynamic animation (quadratic transformation)
        self.animate_quadratic_transformation(
            a_tracker, b_tracker, c_tracker, axes)

        # Call the separate camera animation
        self.animate_camera(chart_group)

        # Call the separate author credit animation
        self.animate_credit(author_text)

    def create_axes(self):
        axes = Axes(
            x_range=[-6, 12, 2],    # Trimmed x-range
            y_range=[-80, 50, 20],  # Trimmed y-range
            axis_config={
                "color": COLOR_FG,
                "include_numbers": True
            },
            tips=True
        )

        axes.x_axis.tip.set(width=0.2, height=0.2)
        axes.y_axis.tip.set(width=0.2, height=0.2)

        LABEL_CONFIG = {
            "font": "Source Sans Pro",
            "font_size": 20,
            "color": COLOR_FG
        }

        for label in chain(
                axes.get_x_axis().numbers,
                axes.get_y_axis().numbers):
            label.set(**LABEL_CONFIG)

        return axes

    def create_grid(self, axes):
        return NumberPlane(
            x_range=axes.x_range,
            y_range=axes.y_range,
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
            "Dynamic Quadratic Plot",
            **FONT_CONFIG,
            font_size=28,
        ).to_edge(UP * 0.5)

        xlabel = Text(
            "X  Axis",
            **FONT_CONFIG,
            font_size=24
        ).next_to(axes, DOWN, buff=0.5)

        ylabel = Text(
            "Y  Axis",
            **FONT_CONFIG,
            font_size=24
        ).rotate(90 * DEGREES).next_to(axes, LEFT, buff=0.3)

        return title, xlabel, ylabel

    def create_dynamic_plot(self, axes):
        # Coefficient trackers with initial values
        a_tracker = ValueTracker(1)
        b_tracker = ValueTracker(-8)
        c_tracker = ValueTracker(20)

        def f(x, a, b, c):
            return a * x**2 + b * x + c

        # Get x-range from axes
        t_min, t_max = axes.x_range[:2]

        def get_trimmed_x_range():
            # Dynamically trim x-range to stay within y-bounds.
            a = a_tracker.get_value()
            b = b_tracker.get_value()
            c = c_tracker.get_value()

            valid_x = [
                x for x in np.linspace(t_min, t_max, 100)
                if axes.y_range[0] <= f(x, a, b, c)
                                   <= axes.y_range[1]
            ]

            if valid_x:
                return [min(valid_x), max(valid_x)]

            # Fallback if no valid x-values
            return [t_min, t_max]

        # Always redraw the curve with updated trimming
        curve = always_redraw(
            lambda: ParametricFunction(
                lambda t: axes.c2p(t, f(t,
                    a_tracker.get_value(),
                    b_tracker.get_value(),
                    c_tracker.get_value()
                )),
                t_range=get_trimmed_x_range(),
                color=COLOR_FG
            )
        )

        # Always redraw dots,
        # keeping them within the valid range
        dots = always_redraw(
            lambda: VGroup(*[
                Dot(axes.c2p(x, f(x,
                    a_tracker.get_value(),
                    b_tracker.get_value(),
                    c_tracker.get_value()
                )), color=RED_E)
                for x in range(int(t_min), int(t_max) + 1, 2)
                if axes.y_range[0] <= f(x,
                    a_tracker.get_value(),
                    b_tracker.get_value(),
                    c_tracker.get_value()
                ) <= axes.y_range[1]
            ])
        )

        # Dynamically update equation text
        equation_text = always_redraw(
            lambda: MathTex(
                f"y = {a_tracker.get_value():.1f}x^2 "
                f"+ {b_tracker.get_value():.1f}x "
                f"+ {c_tracker.get_value():.1f}",
                color=BLUE_E,
                font_size=26
            ).next_to(self.title, DOWN, buff=0.5)
        )

        return curve, dots, \
            a_tracker, b_tracker, c_tracker, equation_text

    def animate_quadratic_transformation(
            self, a_tracker, b_tracker, c_tracker, axes):

        # Handles the animation of coefficient changes
        # while keeping the plot inside bounds.

        transitions = [
            (1, -12, 32, 3),
            (1, -12, -32, 3),
            (1, 12, -32, 3),
            (-1, 12, -32, 3),
            (1, -12, 32, 3),
        ]

        for a, b, c, duration in transitions:
            self.play(
                a_tracker.animate.set_value(a),
                b_tracker.animate.set_value(b),
                c_tracker.animate.set_value(c),
                run_time=duration
            )
            # Pause between transitions
            self.wait(2)

    def create_credit(self):
        return Text(
            "Made by Epsi using Manim",
            font="Source Sans Pro",
            font_size=22,
            color=BLUE_E
        ).move_to(ORIGIN)

    def animate_credit(self, author_text):
        # Handles the flashing and
        # fade-in/out animation of the credit text.

        self.play(Flash(
            author_text, color=TEAL_E, flash_radius=0.5))
        self.wait(1)

        self.play(FadeIn(
            author_text, scale=1.2, run_time=2))
        self.wait(2)

        self.play(
            FadeOut(author_text, run_time=2))

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
