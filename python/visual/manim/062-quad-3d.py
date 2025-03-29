from manim import *
import numpy as np

COLOR_FG = BLACK

class DynamicQuadraticSurface(ThreeDScene):
    def construct(self):
        self.camera.background_color = WHITE
        self.set_camera_orientation(
            phi=75 * DEGREES, theta=45 * DEGREES)

        axes = self.create_axes()

        # Create and animate the surface
        surface, a_tracker, b_tracker, c_tracker, \
            d_tracker, e_tracker, f_tracker, equation_text = (
                self.create_dynamic_surface(axes)
            )

        # Ensure axes are in front of the grid
        axes.set_z_index(2)
        surface.set_z_index(1)

        xlabel, ylabel, zlabel = self.create_labels(axes)
        plane_vectors = self.create_plane_vectors(axes)
        axis_vectors = self.create_axis_vectors(axes)

        # Group all chart elements
        chart_group = VGroup(
            surface, axes, plane_vectors, axis_vectors,
            xlabel, ylabel, zlabel)

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

        # Animate the transformation dynamically
        self.animate_surface_transformation(
            a_tracker, b_tracker, c_tracker,
            d_tracker, e_tracker, f_tracker, surface
        )

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
            fill_opacity=0.5,  # Semi-transparent
            stroke_width=1,    # Wireframe edges
            color=BLUE_E
        )
        # surface.set_depth_test(False)

        # Render behind other objects
        surface.render_priority = -1
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

    def create_dynamic_surface(self, axes):
        """Creates a dynamic quadratic surface with coefficient trackers."""
        # Coefficient trackers
        a_tracker = ValueTracker(1)
        b_tracker = ValueTracker(1)
        c_tracker = ValueTracker(0)
        d_tracker = ValueTracker(-6)
        e_tracker = ValueTracker(6)
        f_tracker = ValueTracker(-64)

        def f(x, y, a, b, c, d, e, f):
            """Quadratic surface equation."""
            return a * x**2 + b * y**2 + c * x * y + d * x + e * y + f

        # Surface update function
        def get_surface():
            surface = Surface(
                lambda u, v: axes.c2p(
                    u, v, f(
                        u, v,
                        a_tracker.get_value(),
                        b_tracker.get_value(),
                        c_tracker.get_value(),
                        d_tracker.get_value(),
                        e_tracker.get_value(),
                        f_tracker.get_value()
                    )
                ),
                u_range=axes.x_range[:2],
                v_range=axes.y_range[:2],
                resolution=(30, 30),
                color=BLUE_E,
            )

            # surface.set_depth_test(False)
            surface.render_priority = -1
            return surface

        # Always redraw the surface
        surface = always_redraw(get_surface)

        # Dynamic equation text
        equation_text = always_redraw(
            lambda: MathTex(
                f"z = {a_tracker.get_value():.1f}x^2 "
                f"+ {b_tracker.get_value():.1f}y^2 "
                f"+ {c_tracker.get_value():.1f}xy "
                f"+ {d_tracker.get_value():.1f}x "
                f"+ {e_tracker.get_value():.1f}y "
                f"+ {f_tracker.get_value():.1f}",
                color=BLUE_E,
                font_size=26
            ).to_corner(UL)
        )

        return surface, a_tracker, b_tracker, c_tracker, \
               d_tracker, e_tracker, f_tracker, equation_text

    def animate_surface_transformation(
            self, a_tracker, b_tracker, c_tracker,
            d_tracker, e_tracker, f_tracker, surface):
        """Animates the transformation of the surface coefficients."""

        # Transitions for coefficient changes
        transitions = [
            (1, 1, 0, -6, 6, -64, 3),
            (2, 1, 1, -6, 6, -64, 3),
            (2, -1, 1, -6, 6, -64, 3),
            (-1, 1, 0, 6, -6, 64, 3),
            (1, 1, 0, -6, 6, -64, 3),  # Return to initial state
        ]

        for a, b, c, d, e, f, duration in transitions:
            self.play(
                a_tracker.animate.set_value(a),
                b_tracker.animate.set_value(b),
                c_tracker.animate.set_value(c),
                d_tracker.animate.set_value(d),
                e_tracker.animate.set_value(e),
                f_tracker.animate.set_value(f),
                run_time=duration
            )
            self.wait(2)

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

