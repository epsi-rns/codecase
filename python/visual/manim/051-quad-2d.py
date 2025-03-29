from manim import *
import numpy as np

class QuadraticPlot(Scene):
    def construct(self):
        # Define axes
        axes = Axes(
            x_range=[-10, 20, 2],
            y_range=[-120, 60, 20],
            axis_config={"color": WHITE}
        )
        
        # Define quadratic function y = x^2 - 12x - 64
        def f(x):
            return x**2 - 12*x - 64
        
        # Plot function
        curve = axes.plot(lambda x: f(x), color=WHITE)
        
        # Plot discrete points
        xdot = np.arange(-6, 16, 1)
        dots = VGroup(*[Dot(axes.c2p(x, f(x)), color=BLUE) for x in xdot])
        
        # Add horizontal and vertical axis lines
        hline = axes.get_horizontal_line(axes.c2p(0, 0), color=WHITE)
        vline = axes.get_vertical_line(axes.c2p(0, -120), color=WHITE)
        
        # Titles and labels
        title = Text("Easy Quadratic Chart", font_size=36).to_edge(UP)
        equation = MathTex("y = x^2 - 12x - 64", color=BLUE).next_to(title, DOWN)
        xlabel = Text("Just X").next_to(axes, DOWN)
        ylabel = Text("Just Y").rotate(90 * DEGREES).next_to(axes, LEFT)
        
        # Show elements
        self.play(Create(axes), Write(title), Write(equation))
        self.wait(1)
        self.play(Create(curve), Create(hline), Create(vline))
        self.play(FadeIn(dots))
        self.wait(1)
        self.play(Write(xlabel), Write(ylabel))
        self.wait(2)
